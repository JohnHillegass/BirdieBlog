from routes import main as main_blueprint
from routes import auth as auth_blueprint
from models import *
from flask import Flask, request, render_template, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'topsecret'
engine = create_engine('sqlite:///blog.db')
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
session = Session()

# Import credentials for google sign-in
# CLIENT_ID = json.loads(open('config/credentials.json', 'r').read())[
#     'web']['client_id']

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=user_id).first()

# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)