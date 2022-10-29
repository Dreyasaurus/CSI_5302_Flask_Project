from flask import Flask
from flask_login import LoginManager
#from config import Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


from app import routes