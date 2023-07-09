from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    cohort = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    instagram = db.Column(db.String, nullable=False)
    twitter = db.Column(db.String, nullable=False)
    facebook = db.Column(db.String, nullable=False)
    github = db.Column(db.String, nullable=False)
    cohort = db.Column(db.String, nullable=False)
    website= db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, nullable=False)
    tslug = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False)
    body = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, nullable=False)
    body = db.Column(db.String(200), nullable=False)
    code = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
