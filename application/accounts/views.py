from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
  
from application import db, app, login_required
from application.accounts.models import Account
from application.accounts.forms import *
from sqlalchemy.exc import IntegrityError

@app.route("/accounts/index.html", methods=["GET"])
@login_required(role="SUPERADMIN")
def accounts_index():
    return render_template("accounts/index.html", accounts = Account.query.all())

@app.route("/accounts/list.html", methods=["GET"])
@login_required(role="SUPERADMIN")
def accounts_list():
    return render_template("accounts/list.html", accounts = Account.query.all())

@app.route("/accounts/new/")
@login_required(role="SUPERADMIN")
def accounts_new():
    return render_template("accounts/new.html", form = AddAccountForm())

@app.route("/accounts/", methods=["POST"])
@login_required(role="SUPERADMIN")
def accounts_create():
    form = AddAccountForm(request.form)
    if not form.validate():
        return render_template("accounts/new.html", form = form)
    a = Account(form.username.data, form.password.data)
    db.session().add(a)
    try:
        db.session().commit()
    except IntegrityError:  # Unique constaint error?
        flash('Username is not unique !')
        db.session.rollback()
        return render_template("accounts/new.html", form = form)
    return redirect(url_for("accounts_index"))

@app.route('/accounts/<account_id>', methods = ['GET','POST'])
@login_required(role="SUPERADMIN")
def accounts_edit(account_id):
    if request.method == "POST" and form.validate():
        form = EditAccountForm(request.form)
        if not form.validate():
            return redirect(url_for("accounts_edit"))
        a = Account.query.get(account_id)
        a.username = form.username.data
        a.hidden = form.hidden.data
        if form.password.data is not "":
            a.password = form.password.data
        try:
            db.session().commit()
        except IntegrityError:  # Unique constaint error?
            flash('Username is not unique !')
            db.session.rollback()
            return redirect(url_for("accounts_edit"))
        return redirect(url_for("accounts_index"))
    else:
        return render_template("accounts/edit.html", form = EditAccountForm(), a = Account.query.get(account_id))