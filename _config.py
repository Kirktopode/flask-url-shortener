import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'short_url.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'just something random'

DATABASE_PATH = os.path.join(basedir, DATABASE)