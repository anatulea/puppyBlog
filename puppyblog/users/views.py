from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from puppyblog.models import User
from puppyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from puppyblog.users.picture_handler import add_profile_pic
from flask_login import login_user, logout_user
from puppyblog import db

authentication = Blueprint('authentication', __name__, template_folder='templates')


@authentication.route('/register', methods=['GET','POST'])
def register_user():
    if current_user.is_authenticated:
        flash('You are already logged-in !')
        return redirect(url_for('core.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data)
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('authentication.do_the_login'))
    return render_template('register.html', form=form)


@authentication.route('/login', methods=['GET', 'POST'])
def do_the_login():
    if current_user.is_authenticated:
        flash('You are already logged-in')
        return redirect(url_for('core.index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if not user or not user.check_password(form.password.data):  # check_password() from /auth/models.py
            flash('Invalid Credentials, Please try again')
            return redirect(url_for('authentication.do_the_login'))

        login_user(user, form.stay_loggedin.data)
        return redirect(url_for('core.index'))

    return render_template('login.html', form=form)


@authentication.route('/logout')
@login_required
def log_out_user():
    logout_user()
    flash('Logged out Successfully')
    return redirect(url_for('core.index'))


@authentication.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()
    # print(f'form.email.data: {form.email.data}')
    # print(f'current_user.user_email: {current_user.user_email}')
    if form.validate_on_submit():
        # print(f"where is this: {form.picture.data}")
        if form.picture.data:
            username = current_user.user_name
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.user_name = form.name.data
        current_user.user_email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('authentication.account'))

    elif request.method == 'GET':
        form.name.data = current_user.user_name
        form.email.data = current_user.user_email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

@authentication.route("/<user_name>")
def user_posts(user_name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(user_name=user_name).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
