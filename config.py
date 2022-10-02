
## a file that contains some configurations for my app

import os



DEBUG = False
TESTING = False
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
API_KEY="2b101mmdc8gSRboBNm5ERTupXe"
SECRET_KEY="49132rh9ehfr2eh234"
UPLOAD_FOLDER = 'user_uploads'
