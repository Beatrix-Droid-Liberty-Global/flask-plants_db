
from distutils.command.config import config
from dotenv import load_dotenv
import os


load_dotenv()

class Config(object):

 
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
