from APP import db
from flask import Blueprint, flash, redirect, url_for, render_template, request
from ..models import user_model
from flask_login import login_user, login_required, logout_user

auth = Blueprint("auth", __name__)

@auth.route('/login')
def login():
    return "Login.html"

@auth.route('/login', methods=["POST"])
def login_post():
    pass

@auth.route('/signup')
def signup():
    return "Signup.html"

@auth.route('/signup', methods=["POST"])
def signup_post():
    pass

@auth.route('/logout')
@login_required
def logout():
    pass