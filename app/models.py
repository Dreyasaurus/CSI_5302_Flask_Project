from datetime import datetime, date
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from app import login

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    
    

    
class People(UserMixin,db.Model):
    playerId    = db.Column(db.String(9), primary_key = True)
    birthYear   = db.Column(db.Integer)
    birthMonth  = db.Column(db.Integer)
    birthDay    = db.Column(db.Integer)
    nameFirst   = db.Column(db.String(255))
    nameLast    = db.Column(db.String(255))
    birth_date  = db.Column(db.DateTime)
    death_date  = db.Column(db.DateTime)
    
    def dateFormatter(self,value, formatString):
        x = value.strftime(formatString)
        return x
        
    def getAge(self):
        if self.death_date is None:
            age = date.today().year - self.birth_date.year
        else:
            age = self.death_date.year - self.birth_date.year
        return age
    
    def __repr__(self):
        return '<People {}>'.format(self.playerId)
        
        
    