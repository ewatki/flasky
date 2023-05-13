from flask import Flask
# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
# import Migrate
from flask_migrate import Migrate
# import libraries for grabbing environment variables
from dotenv import load_dotenv
# used to read envronment variables, gains access to some functions from our operating system
import os

# gives user access to database operations
db = SQLAlchemy()
migrate = Migrate()

# load the values from our .env file so the os module can use them
load_dotenv()

def create_app(test_config=None):
    # __name__ stores the name of the module we're in
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # if we're not in our testing environment
    if not test_config: 
    # set up the database
        # development environment confirguration
        # gets the variable and its value from .env
        # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('RENDER_DATABASE_URI')

    else: 
        # test environment configuration 
        # if there is a test config passed in,
        # this means we're trying to test the app,
        # confirgures the test settings
        app.config["TESTING"] = True
        # "which database am i looking at" = specify which database we're pointing to
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')


    # connect the db and migrate to our flask app
    db.init_app(app)
    migrate.init_app(app, db)

    # import routes
    from .routes import crystal_bp, healer_bp

    # register the blueprint
    app.register_blueprint(crystal_bp)
    app.register_blueprint(healer_bp)

    # import model
    from app.models.crystal import Crystal
    from app.models.healer import Healer

    return app