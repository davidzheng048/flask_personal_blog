from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import db
from flaskblog.models import Post, Category
from flaskblog.posts.forms import PostForm
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        flash('Post Created!', 'success')
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
            category_id=form.category_id.data
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if not current_user.is_authenticated:
        post.click_count += 1
        db.session.commit()
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    form.category_id.choices = [(category.id, category.name) for category in Category.query.all()]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted', 'success')
    return redirect(url_for('main.home'))

