from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flaskblog import db
from flaskblog.models import Category, Post
from flaskblog.categories.forms import CategoryForm
from flask_login import login_required, current_user


categories = Blueprint('categories', __name__)


@categories.route("/category/new", methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        flash('Category Created!', 'success')
        category = Category(name=form.name.data, sequence=form.sequence.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create_category.html', title='New Category', form=form, legend='New Category')


@categories.route("/category/<int:category_id>")
def category(category_id):
    is_login = current_user.is_authenticated

    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(category_id=category.id).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('category.html', title=category.name, category=category, posts=posts, is_login=is_login)


@categories.route("/category/<int:category_id>/update", methods=['GET', 'POST'])
@login_required
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.sequence = form.sequence.data
        db.session.commit()
        flash('Category info updated', 'success')
        return redirect(url_for('categories.category', category_id=category.id))
    elif request.method == 'GET':
        form.name.data = category.name
        form.sequence.data = category.sequence
    return render_template('create_category.html', title='Update Category', form=form, legend='Update Category')


@categories.route("/category/<int:category_id>/delete", methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category Deleted', 'success')
    return redirect(url_for('main.home'))
