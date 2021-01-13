from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_type):
    
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')
    app.config.from_pyfile(configuration)
    db.init_app(app)

    from puppyblog.core.views import core
    from puppyblog.error_pages.handlers import error_pages

    app.register_blueprint(core) 
    app.register_blueprint(error_pages)

    return app