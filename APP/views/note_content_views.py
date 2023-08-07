from APP import app, db
from flask_login import login_required
from flask import Blueprint, render_template, flash, redirect, url_for, request
from ..models import note_content_model, notes_model

content = Blueprint("content", __name__)

@content.route('/note/<int:id>/note_content', methods=["GET", "POST"])
@login_required
def list_content(id):
    page = request.args.get('page', 1, type=int)
    per_page = 5
    note = notes_model.Note.query.filter_by(id=id).first()
    all_note_content = note_content_model.Note_Content.query.filter_by(note_id=note.id).paginate(page=page, per_page=per_page)
    
    return render_template("note_content.html", note=note, note_contents=all_note_content)

@content.route('/note/<int:id>/add_note_content', methods=["POST"])
@login_required
def add_note_content(id):
    if request.method == "POST":
        content = request.form.get("content")

        if not content:
            flash("This field must be filled", "error_not_content")
        else:
            new_note_content = note_content_model.Note_Content(content=content, note_id=id)
            db.session.add(new_note_content)
            db.session.commit()
            flash(f"{content} has been added to your note list.", "success")
            return redirect(url_for("content.list_content", id=id))

    return redirect(url_for("content.list_content", id=id))


@content.route('/note/content/id/<int:content_id>/update_is_completed_content', methods=["POST"])
@login_required
def is_completed_checkbox(content_id):
    if request.method == "POST":
        is_completed = True if request.form.get('checkbox') else False

        note_content = note_content_model.Note_Content.query.filter_by(id=content_id).update({'is_completed': is_completed})
        db.session.commit()
        current_note_content = note_content_model.Note_Content.query.filter_by(id=content_id).first()
        return redirect(url_for('content.list_content', id=current_note_content.note_id))
    return redirect(url_for("content.list_content", id=current_note_content.note_id))

@content.route('/note/content/id/<int:content_id>/update_content', methods=["GET", "POST"])
@login_required
def update_note_content(content_id):
    content_data = note_content_model.Note_Content.query.filter_by(id=content_id).first()
    old_content_data = content_data.content
    note_content_id = content_data.note_id
    if request.method == "POST":
        new_content_data = request.form.get("new_notecontent")
        content_data = note_content_model.Note_Content.query.filter_by(id=content_id).update({"content": new_content_data})
        db.session.commit()
        flash(f"{old_content_data} has been updated to {new_content_data}.", "success_update")
        return redirect(url_for("content.list_content", id = note_content_id))
    return render_template("update_note_content.html", content=content_data)

@content.route('/note/content/id/<int:content_id>/delete_content')
@login_required
def delete_note_content(content_id):
    content_data = note_content_model.Note_Content.query.filter_by(id=content_id).first()
    db.session.delete(content_data)
    db.session.commit()
    return redirect(url_for("content.list_content", id = content_data.note_id))