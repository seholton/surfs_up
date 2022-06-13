# Import dependency
from flask import Flask

#Create flask app instance
app = Flask(__name__)

#Create first flask route
@app.route('/')
def hello_world():
    return 'Hello world'