from app import app, db, bcrypt, slugify, JWT, jwt_required, current_identity, safe_str_cmp
from sqlalchemy import Column, Integer, DateTime, func
from app import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import datetime


class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255), unique=True)
    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password, 9)
       
 
    def is_authenticated(self):
        return True
        
    
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return  (self.id)
        
    def __repr__(self):
        return '<User %r>' % self.username
        
    
    
class Post(db.Model):
    __tablename__ = "posts"
            
    id = db.Column(db.Integer,  primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    slug = db.Column(db.String(80), index=True, nullable=True)
    author = db.relationship("User",backref=db.backref("posts",lazy="dynamic"))
    
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
                    
    def __init__(self, title, body, slug,author):
        self.title = title
        self.body = body
        self.slug = slugify(title).lower()
        self.author = author
 
