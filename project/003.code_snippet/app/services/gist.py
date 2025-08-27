import requests
import json
import os

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

def get_github_headers():
    """GitHub API 요청에 필요한 공통 헤더를 반환합니다."""
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set in environment variables.")
        return None
    return {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }

def create_gist(content: str, file_path: str) -> str:
    """
    코드를 Gist로 생성하고 script URL을 반환합니다.
    """
    headers = get_github_headers()
    if not headers:
        return None

    try:
        # 1. 사용자 ID 가져오기
        user_response = requests.get('https://api.github.com/user', headers=headers)
        user_response.raise_for_status()
        user_id = user_response.json().get('login')
        print(f"계정 아이디: {user_id}")
        
        # 2. Gist 생성 요청 데이터 준비
        data = {
            'description': 'Generated code snippet',
            'public': True,
            'files': {
                file_path: {
                    'content': content
                }
            }
        }
        
        # Gist 생성 시에는 'Content-Type': 'application/json' 헤더를 추가해야 함
        gist_headers = headers.copy()
        gist_headers['Content-Type'] = 'application/json'

        # 3. Gist 생성 요청
        gist_response = requests.post(
            'https://api.github.com/gists',
            headers=gist_headers,
            data=json.dumps(data)
        )
        gist_response.raise_for_status()
        
        gist_data = gist_response.json()
        gist_id = gist_data['id']
        
        # 4. script URL 반환
        script_url = f'https://gist.github.com/{user_id}/{gist_id}.js'
        result = f'<script src="{script_url}"></script>'
        return result

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
