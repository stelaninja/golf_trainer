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

from .models import User, Topics, Polls
from .forms import UserForm
from . import db

import json

views = Blueprint("views", __name__)


# @login_required
@views.route("/", methods=["GET", "POST"])
def home():

    return render_template("home.html", user=current_user)


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
    print(current_user.admin)
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


@login_required
@views.route("/api/polls", methods=["GET", "POST"])
def api_polls():
    if request.method == "POST":
        poll = request.get_json()

        for k, v in poll.items():
            if not v:
                return jsonify({"error": f"Value for {k} is empty"})

        title = poll["title"]
        options_query = lambda option: Options.query.filter(Options.name.like(option))

        options = [
            Polls(option=Options(name=option))
            if options_query(option).count() == 0
            else Polls(option=options_query(option).first())
            for option in poll["options"]
        ]

        new_topic = Topics(title=title, options=options)

        db.session.add(new_topic)
        db.session.commit()

        return jsonify({"message": "Poll was created successfully"})

    else:
        polls = Topics.query.join(Polls).all()
        all_polls = {"Polls": [poll.to_json() for poll in polls]}

        return jsonify(all_polls)


@login_required
@views.route("api/polls/options")
def api_polls_options():
    all_options = [option.to_json() for option in Options.query.all()]

    return jsonify(all_options)


@login_required
@views.route("/api/polls/vote", methods=["PATCH"])
def api_poll_vote():
    poll = request.get_json()

    poll_title, option = (poll["poll_title"], poll["option"])

    join_tables = Polls.query.join(Topics).join(Options)

    option = (
        join_tables.filter(Topics.title.like(poll_title))
        .filter(Options.name.like(option))
        .first()
    )

    if option:
        option.vote_count += 1
        db.session.commit()

        return jsonify({"message": "Thank you for voting"})

    return jsonify({"message": "Option or poll was not found. Please try again!"})
