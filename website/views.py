from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    jsonify,
    send_file,
    redirect,
    url_for,
)
from flask_login import login_required, current_user

from .models import User
from .forms import UserForm
from . import db

import json

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    # form = AircraftForm()
    # aircrafts = Aircraft.query.order_by(Aircraft.id).all()

    return render_template(
        "home.html", user=current_user
    )  # "home.html", aircrafts=aircrafts, user=current_user, form=form,


@login_required
@views.route("/users")
def users():
    all_users = User.query.order_by(User.id).all()
    form = UserForm()

    return render_template(
        "users.html", user=current_user, all_users=all_users, form=form
    )


@login_required
@views.route("/survey")
def survey():
    return render_template("survey.html", user=current_user)


@login_required
@views.route("/edit-user", methods=["GET", "POST"])
def edit_user():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        user_it = User.query.filter_by(id=user_id).first()

    form = UserForm()

    return render_template(
        "edit_user.html", user_it=user_it, form=form, user=current_user
    )


@login_required
@views.route("/delete-user", methods=["POST"])
def delete_user():

    user = json.loads(request.data)
    userId = user["userId"]
    user_to_delete = User.query.get(userId)
    print(user_to_delete)
    if user_to_delete:
        if user_to_delete.id == current_user.id:
            flash("You cannot delete your self at this moment!", category="error")
        else:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash(f"User {user_to_delete.id} is removed", category="success")

    return jsonify({})
