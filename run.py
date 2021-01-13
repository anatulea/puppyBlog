from puppyblog import create_app, db
from puppyblog.models import User

if __name__ == "__main__":
    flask_app = create_app('dev')
    with flask_app.app_context(): # to ensure that the SQLAlchemy binds with my application(there may be multiple apps)
        db.create_all()
        
        # create a default user if there is no user(create_user() from app/auth/models.py)
        if not User.query.filter_by(user_name='harry').first():
            User.create_user(user='harry',
                             email='harry@potters.com',
                             password='secret')
    flask_app.run(debug=True)	  