from app import db,login
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5

followers= db.Table('followers', 
    db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('followed_id',db.Integer, db.ForeignKey('user.id'))                   
                    )
class User(UserMixin,db.Model):
    id= db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(100),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    about_me=db.Column(db.String(200))
    last_seen=db.Column(db.DateTime,default=datetime.utcnow)
    quizess= db.relationship('Quiz', backref='author', lazy='dynamic')
    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0


    
class Quiz(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    number=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    questions= db.relationship('Quiz_ques', backref='group', lazy='dynamic')

class Quiz_ques(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    question=db.Column(db.String(200))
    op1=db.Column(db.String(100))
    op2=db.Column(db.String(100))
    op3=db.Column(db.String(100))
    op4=db.Column(db.String(100))
    correct_option=db.Column(db.Integer)
    quiz_id=db.Column(db.Integer,db.ForeignKey('quiz.id'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

