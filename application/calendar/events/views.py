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

@app.route("/calendar/events/list.html", methods=['GET', 'POST'])
def events_list():
    if request.method == "POST":
        form = EventForm(request.form)
        if form.roomsBooked.data is not None:
            events = Event.query.join((EventRoom, Event.id==EventRoom.event_id)).filter(EventRoom.room_id.in_((form.roomsBooked.data))).all()
            return render_template("calendar/events/list.html", events=events, rooms = Room.query.all())
    return render_template("calendar/events/list.html", events = Event.query.all(), rooms = Room.query.all())

@app.route("/calendar/events/new/")
@login_required()
def events_new():
    return render_template("calendar/events/new.html", form = EventForm(), rooms = Room.query.all())


@app.route("/calendar/events/", methods=["POST"])
@login_required()
def events_create():
    form = EventForm(request.form)
    if not form.validate():
        flash('Validation error: please check all fields')
        return render_template("calendar/events/new.html", form = form, rooms = Room.query.all())
    e = Event(form.name.data, form.startTime.data, form.endTime.data, form.responsible.data, form.description.data, current_user.id)
    db.session().add(e)
    db.session.flush()
    for roomId in form.roomsBooked.data:
        if roomId in form.privateReserve.data:
            er = EventRoom(e.id, roomId, 1)
        else:
            er = EventRoom(e.id, roomId, 0)
        db.session().add(er)
    try:
        db.session().commit()
    except IntegrityError:
        flash('There is something wrong ! Please check the form !')
        db.session.rollback()
        return render_template("calendar/events/new.html", form = form)
    return redirect(url_for("events_index"))

@app.route('/calendar/events/<event_id>/delete', methods = ['POST'])
@login_required()
def events_delete(event_id):
    e = Event.query.get(event_id)
    if e.accountId != current_user.id and 'ADMIN' not in current_user.roles():
        flash("You are not authorized to remove others events.")
        return redirect(url_for("events_list"))
    EventRoom.query.filter_by(event_id=event_id).delete()
    Event.query.filter_by(id=event_id).delete()
    db.session().commit()
    return redirect(url_for("events_list"))


@app.route('/calendar/events/<event_id>', methods = ['GET','POST'])
@login_required()
def events_edit(event_id):
    e = Event.query.get(event_id)
    if e.accountId != current_user.id and 'ADMIN' not in current_user.roles():
        flash("You are not authorized to remove others events.")
        return redirect(url_for("events_list"))
    form = EventForm(request.form)
    if request.method == "POST":
        if not form.validate():
            flash('Validation error: please check all fields')
            return render_template("calendar/events/edit.html", form = EventForm(), e = Event.query.get(event_id), rooms = Room.query.all())
        EventRoom.query.filter_by(event_id=event_id).delete()
        e.id = form.event_id.data
        e.name = form.name.data
        e.startTime = form.startTime.data
        e.endTime = form.endTime.data
        e.desctiption = form.description.data
        e.responsible = form.responsible.data
        e.accountId = current_user.id # TODO use the original user ID
        for roomId in form.roomsBooked.data:
            if roomId in form.privateReserve.data:
                er = EventRoom(e.id, roomId, 1)
            else:
                er = EventRoom(e.id, roomId, 0)
            db.session().add(er)
        try:
            db.session().commit()
        except IntegrityError:
            flash('There is something wrong ! Please check the form !')
            db.session.rollback()
            return render_template("calendar/events/edit.html", form = EventForm(), e = Event.query.get(event_id), rooms = Room.query.all())
        return redirect(url_for("events_index"))
    else:
        return render_template("calendar/events/edit.html", form = EventForm(), e = Event.query.get(event_id), rooms = Room.query.all())