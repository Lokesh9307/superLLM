from flask import Flask
from app.routes.chat_routes import chat_blueprint
from app.routes.youtube_routes import youtube_blueprint
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(chat_blueprint, url_prefix='/api/pdf')
    app.register_blueprint(youtube_blueprint, url_prefix='/api/youtube')
    return app