from json import dumps
import logging
import os
from flask import Blueprint, request, jsonify, Response, send_file, after_this_request
from app.services.github import get_raw_file_content
from app.services.gist import create_gist
from app.services.pastebin import create_pastebin
from app.services.carbon import create_carbon_image

snippet_bp = Blueprint('snippet_bp', __name__)

ACTIONS = {
    'script': create_gist,
    'iframe': create_pastebin,
    'image': create_carbon_image,
}

@snippet_bp.route('/snippet', methods=['GET'])
async def get_snippet():
    try:
        raw_url = request.args.get('raw_url')
        start_line = int(request.args.get('start', 1))
        end_line = int(request.args.get('end', -1))
        file_path = request.args.get('path', 'snippet.py') # Gist 생성 파일명, Carbon API를 위한 파일명
        format = request.args.get('format', 'script')

        if not raw_url:
            return jsonify({"error": "Missing required parameter: raw_url"}), 400

        full_content = get_raw_file_content(raw_url)
        if full_content is None:
            return jsonify({"error": "Unable to fetch content from the provided URL"}), 404

        lines = full_content.splitlines()
        start_index = start_line - 1
        end_index = end_line if end_line != -1 and end_line <= len(lines) else len(lines)
        snippet = '\n'.join(lines[start_index:end_index])
        print(f'snippet: {snippet}')
        method = ACTIONS.get(format, None)

        if method != None:
            result = method(snippet, file_path) if format != 'image' else await method(snippet, file_path)
            print(f'result: {result}')
            if result:
                if format != 'image' :
                    return jsonify({"result": result}), 200 
                else:
                    @after_this_request
                    def remove_file(response):
                        try:
                            os.remove(result)
                            logging.info(f"File {result} successfully deleted.")
                        except Exception as e:
                            logging.error(f"Error removing file {result}: {e}")
                        return response

                    return send_file(result, mimetype='image/png', as_attachment=True, download_name='snippet.png')
            return jsonify({"error": f"Failed to create {format}"}), 500

        return jsonify({"error": "Unsupported format"}), 400

    except ValueError:
        return jsonify({"error": "Invalid start or end line number"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
