from flask import Flask
from app.routes.router import snippet_bp

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# 라우터 블루프린트 등록
app.register_blueprint(snippet_bp)