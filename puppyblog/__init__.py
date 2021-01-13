from flask import Flask
import os
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_type):
    
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')
    app.config.from_pyfile(configuration)
    db.init_app(app)
    bootstrap.init_app(app)  # initialize bootstrap
    login_manager.init_app(app)  # initialize login_manager
    bcrypt.init_app(app)

    from puppyblog.core.views import core
    from puppyblog.error_pages.handlers import error_pages
    from puppyblog.users.views import authentication
    from puppyblog.blog_posts.views import blog_posts

    app.register_blueprint(core) 
    app.register_blueprint(error_pages)
    app.register_blueprint(authentication)
    app.register_blueprint(blog_posts)

    return app