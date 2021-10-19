from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

# Base model
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


# Model for users
class User(Base, UserMixin):
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    admin = db.Column(db.Boolean)


# Model for poll topics
class Topics(Base):
    title = db.Column(db.String(500))

    def __repr__(self):
        return self.title

    def to_json(self):
        return {
            "title": self.title,
            "options": [
                {"name": option.option.name, "vote_count": option.vote_count}
                for option in self.options.all()
            ],
            "status": self.status,
        }


# Model for poll options
class Options(Base):
    name = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return self.name

    def to_json(self):
        return {"id": uuid.uuid4(), "name": self.name}


# Model for polls
class Polls(Base):
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"))
    option_id = db.Column(db.Integer, db.ForeignKey("options.id"))
    vote_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean)

    # Create relationships
    topic = db.relationship(
        "Topics", foreign_keys=[topic_id], backref=db.backref("options", lazy="dynamic")
    )
    option = db.relationship("Options", foreign_keys=[option_id])

    def __repr__(self):
        return self.option.name

