# 실행 방법

```bash
# Dockerfile 빌드(이미지명은 dev-snippet, 개발용)
docker build -t dev-snippet -f Dockerfiles/dev/Dockerfile.dev .
# Dockerfile 빌드(이미지명은 dev-snippet, 운영용)
docker build -t prd-snippet -f Dockerfiles/prd/Dockerfile.prd .

# Docker Container 개발 실행(dev-snippet 이미지로 dev-snippet 컨테이너 백그라운드로 실행, 컨테이너 종료 시 컨테이너와 관련된 파일 시스템 삭제(일회성 작업), 컨테이너-로컬 22:1222, 5000:5000으로 포트 포워딩)
docker run -d --rm -p 1222:22 -p 5000:5000 -v /Users/mac/workspace:/workspace --name dev-snippet dev-snippet

# Docker Container 실행 확인
docker ps

# Docker Container 접속
docker exec -it dev-snippet bash

# Visual Studio Code Remote Explorer 설정
Host dev-snippet
  HostName localhost
  Port 1222
  User root
  IdentityFile ~/.ssh/id_rsa

# 컨테이너 dev-snippet에 SSH로 접속
ssh root@localhost -p 1222

# Flask 실행
cd /workspace/snippet && python3 run.py
```

# 소스

```
/snippet/
├── Dockerfiles/
│   ├── dev/
│   │   └── Dockerfile.dev # 서비스 컨테이너 도커 파일(개발용)
│   ├── prd/
│   │   └── Dockerfile.prd # 서비스 컨테이너 도커 파일(운영용)
├── app/
│   ├── __init__.py
│   ├── app.py                # Flask 애플리케이션 객체와 메인 로직
│   ├── routes/
│   │   ├── __init__.py
│   │   └── router.py         # 라우트 파일
│   └── services/
│       ├── __init__.py
│       ├── carbon.py         # 이미지 생성 로직(https://carbon.now.sh/)
│       ├── github.py         # 소스 raw 파일 수집 로직
│       └── gist.py           # Gist 생성 로직
├── run.py                    # Flask 실행 파일
└── requirements.txt          # 프로젝트 파이썬 종속성 패키지 목록
```

# 서비스 사용 방법
### API 사용 방법
* HTTP Method: `GET`
* Endpoint: `/snippet`
* Parameters:
    * `raw_url`: 가져올 파일의 원시(raw) URL
    * `start`: 스니펫을 시작할 라인 번호
    * `end`: 스니펫을 끝낼 라인 번호
    * `format`: 반환 형식으로 `script`, `image`의 3가지를 지원.
    * `path`: `GIST` 생성 파일명
* Call Example:
    ```
    #인터넷 브라우저 주소창에서
    http://localhost:5000/snippet?raw_url=https://raw.githubusercontent.com/gouwon/loti/bcd5311027c578d5ceb5c4fbcd9b50dc0494b2f5/Dockerfiles/dev/Dockerfile.python&start=24&end=28&format=script&path=snippet.js
    ```
* Response Example:
    ```
    {"result": "<script src=\"https://gist.github.com/gouwon/039c9fd32d51e0694a2273f4370d3a7d.js\"></script>"}
    ```
    위에서 역슬래쉬(`\`)<sup>[1](#JSON)</sup>를 빼고 복사해서 사용하면 됨.  
    <U>`format`이 `image`인 경우, 앞에 공백이 생기는 문제가 있는 데, 이는 좀 더 살펴봐야 함...</U>

<a name="JSON">1</a>: 웹 통신의 `JSON` 규칙에 따라 자동으로 이스케이프 처리되기 때문에, 이를 무리하게 피하게 하는 것이 어려워서 일단 이렇게 사용함.
