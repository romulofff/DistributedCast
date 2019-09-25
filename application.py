import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG='True'
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
   
    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        application.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @application.route('/')
    @application.route('/hello')
    def hello():
        return 'Olá, mundo!'

    return application

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
 