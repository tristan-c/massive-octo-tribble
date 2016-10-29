from flask import request, Response, render_template, g, redirect, url_for
from flask_login import LoginManager, logout_user, login_user, current_user

from massive import login_manager, app
from massive.forms import *
from massive.models import User

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@login_manager.unauthorized_handler
def unauthorized():
    return "unauthorized", 405

@app.before_request
def before_request():
    g.user = current_user

# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('index'))

#     form = LoginForm()
#     error = []
#     if form.validate_on_submit():
#         try:
#             user = User.query.filter_by(email=form.login.data).first()
#             if not user:
#                 raise ValueError("Unkown user")
#         except Exception as e:
#             return render_template("security/login_user.html", login_user_form=form, error=[e])

#         if not bcrypt.check_password_hash(user.password, form.password.data):
#             error.append("bad password")
#         else:
#             login_user(user)
#             return redirect(request.args.get("next") or url_for("index"))

#     return render_template("security/login_user.html", login_user_form=form, error=error)


# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))
