from flask import Flask
from config import Config

flaskApp = Flask(__name__)
flaskApp.config.from_object(Config)

from app import routes
