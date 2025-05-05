from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registering the webhook route
    from .webhook import webhook_blueprint
    app.register_blueprint(webhook_blueprint, url_prefix='/')

    return app
