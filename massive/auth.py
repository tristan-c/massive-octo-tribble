from flask import request, Response, render_template, g, redirect, url_for
from flask.ext.login import LoginManager, logout_user, login_user

from massive import login_manager, app, bcrypt
from massive.forms import *
from massive.models import Users

from pony.orm import get, db_session


@login_manager.user_loader
def load_user(userid):
    with db_session:
        return Users.get(id=userid)


@login_manager.unauthorized_handler
def unauthorized():
    return "unauthorized", 405

@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    error = []
    if form.validate_on_submit():
        try:
            with db_session:
                user = Users.get(login=form.login.data)
            if not user:
                raise ValueError("Unkown user")
        except Exception as e:
            return render_template("security/login_user.html", login_user_form=form, error=[e])

        if not bcrypt.check_password_hash(user.password, form.password.data):
            error.append("bad password")
        else:
            login_user(user)
            return redirect(request.args.get("next") or url_for("index"))

    return render_template("security/login_user.html", login_user_form=form, error=error)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
