from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,login_required
from .forms import LoginForm,RegistrationForm
from ..models import Users,Blogs,Comments
from .. import db
from . import auth
from ..email import mail_message

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        users = Users(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(users)
        db.session.commit()

        mail_message('Welcome to Blog','email/welcome_users',users.email,users=users)
        return redirect(url_for('auth.login'))
        # title = "New Account"
    return render_template('auth/register.html',registration_form = form)

# @auth.route('/verify',methods=['GET','POST'])
# def verify():
#     v_form = ValidForm()
#     if v_form.validate_on_submit():
#         v_code = User.query.filter_by(code = v_form.code.data).first()
#         if v_code is not None and v_form.code.data:
#             return redirect(request.args.get('next') or url_for('auth.login'))
#         flash('Wrong code')
#     title = 'Account verification'
#     return render_template('auth/verify.html', v_form = v_form,title = title)


@auth.route('/login',methods=['GET','POST'])
def login():
    login_form =LoginForm()
    if login_form.validate_on_submit():
        users = Users.query.filter_by(username = login_form.username.data).first()
        if users is not None and users.verify_password(login_form.password.data):
            login_user(users,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    title = 'Login'
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
