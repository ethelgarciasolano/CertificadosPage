import flask 
import os

app = flask.Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)
app.config['UPLOAD_FOLDER']='static/file'
