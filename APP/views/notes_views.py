from APP import db
from flask_login import login_required, current_user
from Flask import Blueprint, render_template, flash, redirect, url_for, request
from ..models import notes_model

main = Blueprint("main", __name__)

@main.route('/')
def home():
    pass

@main.route('/profile', methods=["POST"])
@login_required
def add_note():
    pass

@main.route('/profile', methods=["POST"])
@login_required
def list_notes():
    pass

@main.route('/profile/note/<note_name>')
@login_required
def list_content_note(note_name):
    pass

@main.route('/<int:id>/update_note', methods=["POST"])
@login_required
def update_note(id):
    pass

@main.route('/<int:id>/profile')
@login_required
def delete_note(id):
    pass