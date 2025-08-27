import asyncio
from app.app import app

if __name__ == '__main__':
    # Flask를 비동기 모드로 실행(개발용)
    asyncio.run(app.run(host='0.0.0.0', port=5000, debug=True))
    # 실제 운영 환경에서는 Gunicorn과 같은 WSGI 서버를 사용하는 것이 좋음
    # 예: gunicorn -k uvicorn.workers.UvicornWorker run:app --bind
    # 참고: https://flask.palletsprojects.com/en/2.3.x/deploying/wsgi-standalone/
    # 참고: https://flask.palletsprojects.com/en/2.3.x/deploying/async-await/
    # 참고: https://www.uvicorn.org/deployment/
    # 참고: https://docs.gunicorn.org/en/stable/design.html#async
    # 참고: https://docs.gunicorn.org/en/stable/settings.html#worker-class
    # 참고:
    #   - sync: 기본 동기 워커, 요청을 순차적으로 처리
    #   - eventlet/gevent: 비동기 워커, 많은 수의 동시 연결을 처리하는 데 적합
    #   - uvicorn.workers.UvicornWorker: ASGI 애플리케이션을 위한 비동기 워커
    #   - tornado: 비동기 워커, 높은 동시성을 제공
    #   - meinheld: 비동기 워커, 빠른 성능 제공
    # 운영 환경에서는 다음과 같이 실행:
    # gunicorn -k uvicorn.workers.UvicornWorker run:app --bind
    # 또는
    # gunicorn -k gevent run:app --bind
