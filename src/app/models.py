#coding=utf-8
'''
Created on 2016年12月14日

@author: huangning
'''
from flask_sqlalchemy import SQLAlchemy
from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager



class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    category_id = db.Column(db.Integer, db.ForeignKey('category_or_tags.id'))
    tags = db.Column(db.String(256))
    
    @property
    def category_name(self):
        id = self.category_id
        obj = Category_or_Tag.query.filter_by(id=id).first()
        return  obj.name
    
    @property
    def length(self):
        return  len(self.body)
    
    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        for i in range(count):
            u = User.query.first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(40, 50)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()  
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    
    
class Category_or_Tag(db.Model):
    __tablename__ = 'category_or_tags'
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(64), unique=True, index=True)
    istag = db.Column(db.Boolean,default=True)
    
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


