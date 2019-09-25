
from flask import Flask, render_template, request
from application import db
from application.models import Data

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'dev'   

@application.route('/')
@application.route('/hello')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    application.run(debug=True)