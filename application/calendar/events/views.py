from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user

from application import db, app, login_required
from application.calendar.events.models import Event
from application.calendar.events.forms import *
from application.calendar.rooms.models import Room
from application.calendar.event_room.models import EventRoom
from sqlalchemy.exc import IntegrityError

@app.route("/calendar/events/index.html", methods=["GET"])
def events_index():
    return render_template("calendar/events/index.html", events = Event.query.all())

@app.route("/calendar/events/list.html", methods=["GET"])
def events_list():
    return render_template("calendar/events/list.html", events = Event.query.all())

@app.route("/calendar/events/new/")
#@login_required()
def events_new():
    return render_template("calendar/events/new.html", form = EventForm(), rooms = Room.query.all())


@app.route("/calendar/events/", methods=["POST"])
#@login_required()
def events_create():
    form = EventForm(request.form)
    if not form.validate():
        return render_template("calendar/events/new.html", form = form, rooms = Room.query.all())
    e = Event(form.name.data, form.startTime.data, form.endTime.data, form.responsible.data, form.description.data, current_user.id)
    db.session().add(e)
    db.session.flush()
    for roomId in form.roomsBooked.data:
        er = EventRoom(roomId, e.id, 0)
        db.session().add(er)
    try:
        db.session().commit()
    except IntegrityError:  # Unique constaint error?
        flash('There is something wrong ! Please check the form !')
        db.session.rollback()
        return render_template("calendar/events/new.html", form = form)
    return redirect(url_for("events_index"))

@app.route('/calendar/events/<event_id>', methods = ['GET','POST'])
@login_required()
def events_edit(event_id):
    form = EventForm(request.form)
    if request.method == "POST" and form.validate():
        form = EventForm(request.form)
        if not form.validate():
            return redirect(url_for("events_edit"))
        r = Event.query.get(event_id)
        r.name = form.name.data
        r.hidden = form.hidden.data
        r.description = form.description.data
        try:
            db.session().commit()
        except IntegrityError:  # Unique constaint error?
            flash('Username is not unique !')
            db.session.rollback()
            return redirect(url_for("events_edit"))
        return redirect(url_for("events_index"))
    else:
        return render_template("calendar/events/edit.html", form = EventForm(), r = Event.query.get(event_id))