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
    playerId        = db.Column(db.String(9), primary_key = True)
    birthYear       = db.Column(db.Integer)
    birthMonth      = db.Column(db.Integer)
    birthDay        = db.Column(db.Integer)
    birthCountry    = db.Column(db.String(255))
    birthState      = db.Column(db.String(255))
    birthCity       = db.Column(db.String(255))
    deathYear       = db.Column(db.Integer)
    deathMonth      = db.Column(db.Integer)
    deathDay        = db.Column(db.Integer)
    deathCountry    = db.Column(db.String(255))
    deathState      = db.Column(db.String(255))
    deathCity       = db.Column(db.String(255))
    nameFirst       = db.Column(db.String(255))
    nameLast        = db.Column(db.String(255))
    nameGiven       = db.Column(db.String(255))
    weight          = db.Column(db.Integer)
    height          = db.Column(db.Integer)
    bats            = db.Column(db.String(255))
    throws          = db.Column(db.String(255))
    debut           = db.Column(db.String(255))
    finalGame       = db.Column(db.String(255))
    retroID         = db.Column(db.String(255))
    bbrefID         = db.Column(db.String(255))
    birth_date      = db.Column(db.DateTime)
    debut_date      = db.Column(db.DateTime)
    finalgame_date  = db.Column(db.DateTime)
    death_date      = db.Column(db.DateTime)
    
    battingDetails  = db.relationship('Batting', lazy='dynamic')
    awards          = db.relationship('AwardsPlayers', lazy='dynamic')
    
    #formats a given date
    def dateFormatter(self,value, formatString):
        x = value.strftime(formatString)
        return x
    # Gets the Living or the death date of the player  
    def getAge(self):
        if self.death_date is None:
            age = date.today().year - self.birth_date.year
        else:
            age = self.death_date.year - self.birth_date.year
        return age
    
    def __repr__(self):
        return '<People {}>'.format(self.playerId)
        
        
class AwardsPlayers(UserMixin,db.Model):
    __tablename__ = "AwardsPlayers"
    id              = db.Column(db.Integer, primary_key = True)
    playerId        = db.Column(db.String(9),db.ForeignKey('people.playerId'))
    awardId         = db.Column(db.String(255))
    notes           = db.Column(db.String(100))
    
    def __repr__(self):
        return '<AwardsPlayers {}>'.format(self.playerId)
        
        
class Batting(UserMixin,db.Model):
    id              = db.Column(db.Integer, primary_key = True)
    playerId        = db.Column(db.String(9),db.ForeignKey('people.playerId'))
    yearId          = db.Column(db.Integer)
    teamId          = db.Column(db.Integer)
    team_ID         = db.Column(db.Integer)
    lgId            = db.Column(db.String(2))
    g               = db.Column(db.Integer)
    
    def getAge(self,birthDate):
        return self.yearId - birthDate
    
    def __repr__(self):
        return '<Batting {}>'.format(self.playerId)