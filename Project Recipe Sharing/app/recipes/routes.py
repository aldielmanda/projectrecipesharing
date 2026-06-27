from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Recipe, FoodRecipe, DrinkRecipe, Ingredient, Review, Bookmark
from app.recipes.forms import RecipeForm, ReviewForm

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/')
def index():
    cat = request.args.get('category')
    recipes = Recipe.query.filter_by(category=cat).all() if cat else Recipe.query.all()
    return render_template('recipes/index.html', recipes=recipes, sel_cat=cat)

@recipes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = RecipeForm()
    if form.validate_on_submit():
        if form.recipe_type.data == 'food':
            recipe = FoodRecipe(title=form.title.data, category=form.category.data, steps=form.steps.data, cooking_time=form.cooking_time.data or 0, author=current_user)
        else:
            recipe = DrinkRecipe(title=form.title.data, category=form.category.data, steps=form.steps.data, is_cold_served=form.is_cold_served.data, author=current_user)
        
        db.session.add(recipe); db.session.commit()

        for n, a in zip(request.form.getlist('ing_name'), request.form.getlist('ing_amount')):
            if n.strip(): db.session.add(Ingredient(name=n.strip(), amount=a.strip(), recipe_id=recipe.id))
        db.session.commit()

        flash('Resep berhasil dipublikasikan!', 'success')
        return redirect(url_for('recipes.index'))
    return render_template('recipes/form.html', form=form, title="Buat Konten Resep")

@recipes_bp.route('/<int:id>', methods=['GET', 'POST'])
def detail(id):
    recipe = Recipe.query.get_or_404(id)
    form = ReviewForm()
    is_bm = False
    if current_user.is_authenticated:
        is_bm = Bookmark.query.filter_by(user_id=current_user.id, recipe_id=recipe.id).first() is not None
        if form.validate_on_submit():
            rev = Review.query.filter_by(user_id=current_user.id, recipe_id=recipe.id).first()
            if rev: rev.rating, rev.comment = form.rating.data, form.comment.data
            else: db.session.add(Review(rating=form.rating.data, comment=form.comment.data, user_id=current_user.id, recipe_id=recipe.id))
            db.session.commit()
            recipe.sync_rating()
            db.session.commit()
            flash('Review Anda berhasil direkam.', 'success')
            return redirect(url_for('recipes.detail', id=recipe.id))
    return render_template('recipes/detail.html', recipe=recipe, form=form, is_bookmarked=is_bm)

@recipes_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.user_id != current_user.id and not current_user.is_admin(): abort(403)
    form = RecipeForm(obj=recipe)
    if request.method == 'GET': form.recipe_type.data = recipe.type
    
    if form.validate_on_submit():
        recipe.title, recipe.category, recipe.steps = form.title.data, form.category.data, form.steps.data
        if recipe.type == 'food': recipe.cooking_time = form.cooking_time.data or 0
        elif recipe.type == 'drink': recipe.is_cold_served = form.is_cold_served.data

        Ingredient.query.filter_by(recipe_id=recipe.id).delete()
        for n, a in zip(request.form.getlist('ing_name'), request.form.getlist('ing_amount')):
            if n.strip(): db.session.add(Ingredient(name=n.strip(), amount=a.strip(), recipe_id=recipe.id))
        db.session.commit()
        flash('Perubahan resep disimpan!', 'success')
        return redirect(url_for('recipes.detail', id=recipe.id))
    return render_template('recipes/form.html', form=form, recipe=recipe, title="Ubah Resep")

@recipes_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    recipe = Recipe.query.get_or_404(id)
    if recipe.user_id != current_user.id and not current_user.is_admin(): abort(403)
    db.session.delete(recipe); db.session.commit()
    flash('Resep dihapus permanen.', 'warning')
    return redirect(url_for('recipes.index'))