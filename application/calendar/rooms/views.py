from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
  
from application import db, app, login_required
from application.calendar.rooms.models import Room
from application.calendar.rooms.forms import *
from sqlalchemy.exc import IntegrityError

@app.route("/calendar/rooms/index.html", methods=["GET"])
@login_required(role="SUPERADMIN")
def rooms_index():
    return render_template("calendar/rooms/index.html", rooms = Room.query.all())

@app.route("/calendar/rooms/list.html", methods=["GET"])
@login_required(role="SUPERADMIN")
def rooms_list():
    return render_template("calendar/rooms/list.html", rooms = Room.query.all())

@app.route("/calendar/rooms/new/")
@login_required(role="SUPERADMIN")
def rooms_new():
    return render_template("calendar/rooms/new.html", form = AddRoomForm())

@app.route("/calendar/rooms/", methods=["POST"])
@login_required(role="SUPERADMIN")
def rooms_create():
    form = AddRoomForm(request.form)
    if not form.validate():
        return render_template("calendar/rooms/new.html", form = form)
    r = Room(form.name.data, form.description.data)
    db.session().add(r)
    try:
        db.session().commit()
    except IntegrityError:  # Unique constaint error?
        flash('Name is not unique !')
        db.session.rollback()
        return render_template("calendar/rooms/new.html", form = form)
    return redirect(url_for("rooms_index"))

@app.route('/calendar/rooms/<room_id>', methods = ['GET','POST'])
@login_required(role="SUPERADMIN")
def rooms_edit(room_id):
    form = EditRoomForm(request.form)
    if request.method == "POST" and form.validate():
        form = EditRoomForm(request.form)
        if not form.validate():
            return redirect(url_for("rooms_edit"))
        r = Room.query.get(room_id)
        r.name = form.name.data
        r.hidden = form.hidden.data
        r.description = form.description.data
        try:
            db.session().commit()
        except IntegrityError:  # Unique constaint error?
            flash('Username is not unique !')
            db.session.rollback()
            return redirect(url_for("rooms_edit"))
        return redirect(url_for("rooms_index"))
    else:
        return render_template("calendar/rooms/edit.html", form = EditRoomForm(), r = Room.query.get(room_id))