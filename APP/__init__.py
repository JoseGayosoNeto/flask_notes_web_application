from flask import Flask
from flask_bcrypt import Bcrypt
import secrets
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy()
login_manager = LoginManager()

secret_key = secrets.token_hex(16)
secret_key_hash = bcrypt.generate_password_hash(secret_key)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
app.config["SECRET_KEY"] = secret_key_hash

db.init_app(app)
login_manager.init_app(app)



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

