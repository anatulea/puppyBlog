from puppyblog import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin



class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    user_email = db.Column(db.String(64), unique=True, index=True)
    user_name = db.Column(db.String(64), unique=True, index=True)
    user_password = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def check_password(self,password):
        return bcrypt.check_password_hash(self.user_password, password)
    
    @classmethod # used in run.py
    def create_user(cls, user, email, password):
        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return user

# is a login Manager function that sets a callback for reloading a user from the session.
# it takes a user id and returns 'none' if user does not exist.
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class BlogPost(db.Model):
    __tablename__ = 'blogs'
    
    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    # Setup the relationship to the User table
    users = db.relationship(User)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id =user_id


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"