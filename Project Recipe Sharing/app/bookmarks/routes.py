from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Recipe, Bookmark

bookmarks_bp = Blueprint('bookmarks', __name__)

@bookmarks_bp.route('/')
@login_required
def index():
    bms = Bookmark.query.filter_by(user_id=current_user.id).all()
    return render_template('bookmarks/index.html', recipes=[bm.recipe for bm in bms])

@bookmarks_bp.route('/toggle/<int:recipe_id>', methods=['POST'])
@login_required
def toggle(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    bm = Bookmark.query.filter_by(user_id=current_user.id, recipe_id=recipe.id).first()
    if bm: db.session.delete(bm); flash('Dihapus dari koleksi favorit.', 'info')
    else: db.session.add(Bookmark(user_id=current_user.id, recipe_id=recipe.id)); flash('Berhasil disimpan ke favorit!', 'success')
    db.session.commit()
    return redirect(url_for('recipes.detail', id=recipe.id))