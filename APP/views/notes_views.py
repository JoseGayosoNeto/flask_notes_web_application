from APP import db
from flask_login import login_required, current_user
from flask import Blueprint, render_template, flash, redirect, url_for, request
from ..models import notes_model

main = Blueprint("main", __name__)


@main.route('/profile', methods=["GET"])
@login_required
def profile():
    page = request.args.get("page", 1, type=int)
    per_page = 5
    all_notes = notes_model.Note.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=per_page)
    return render_template("profile.html", notes=all_notes)

@main.route('/profile', methods=["POST"])
@login_required
def add_note():
    if request.method == 'POST':
        note_name = request.form.get('notename')

        if not note_name:
            flash("This field must be filled", "error_not_notename")
        else:
            new_note = notes_model.Note(note_name=note_name, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash(f"{new_note.note_name} has been added to your note list.", "success")
            return redirect(url_for("main.profile"))
        
    return redirect(url_for("main.profile"))


@main.route('/<int:id>/update_note', methods=["GET","POST"])
@login_required
def update_note(id):
    note = notes_model.Note.query.filter_by(id=id).first()
    old_note_name = note.note_name
    if request.method == "POST":
        new_note_name = request.form.get('new_notename')

        note = notes_model.Note.query.filter_by(id=id).update({"note_name": new_note_name})
        db.session.commit()
        flash(f"{old_note_name} has been updated to {new_note_name}.", "success_update")
        return redirect(url_for("main.profile"))
    return render_template("update_note.html", note=note)

@main.route('/<int:id>/delete')
@login_required
def delete_note(id):
    note = notes_model.Note.query.filter_by(id=id).first()
    db.session.delete(note)
    db.session.commit()
    flash(f"{note.note_name} has been deleted.", "success_delete")
    return redirect(url_for("main.profile"))

