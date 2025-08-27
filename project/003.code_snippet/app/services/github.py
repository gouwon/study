from urllib.parse import urljoin
import requests

GITHUB_API_BASE_URL = 'https://raw.githubusercontent.com'

def get_raw_file_content(raw_url):
    """
    GitHub raw URL을 통해 파일 내용을 직접 가져옵니다.
    """
    try:
        url = urljoin(GITHUB_API_BASE_URL, raw_url)
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 200 OK가 아닌 경우 예외 발생
        return response.text
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Error 404: File not found at {url}")
        else:
            print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
