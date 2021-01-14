from puppyblog import create_app, db
from puppyblog.models import User
from sqlalchemy import exc


flask_app = create_app('prod')
with flask_app.app_context():  # to ensure that the SQLAlchemy binds with my application(there may be multiple apps)
    db.create_all()
    try:
        # create a default user if there is no user(create_user() from app/auth/models.py)
        if not User.query.filter_by(user_name='harry').first():
            User.create_user(user='harry',
                             email='harry@potters.com',
                             password='secret')
    except exc.IntegrityError:
        flask_app.run()