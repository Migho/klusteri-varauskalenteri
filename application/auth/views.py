from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user
  
from application import app
from application.accounts.models import Account
from application.auth.forms import LoginForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    account = Account.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not account:
        return render_template("auth/loginform.html", form = form, error = "No such username or password")


    login_user(account)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index")) 