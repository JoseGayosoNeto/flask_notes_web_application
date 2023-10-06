from flask import Flask
from flask_bcrypt import Bcrypt
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv


app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["MAIL_SERVER"] = 'smtp.office365.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD')


db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)



from .models import user_model, notes_model, note_content_model

from .views.user_views import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .views.notes_views import main as main_blueprint
app.register_blueprint(main_blueprint)

from .views.note_content_views import content as content_blueprint
app.register_blueprint(content_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return user_model.User.query.get(int(user_id))

