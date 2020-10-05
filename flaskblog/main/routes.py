from flask import Blueprint
from flask import render_template, request
from flaskblog.models import Post, Category
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.app_context_processor
def context_processor():
    categories = Category.query.all()
    recent_posts = Post.query.order_by(Post.id.desc()).limit(5).all()
    return {
        'categories': categories,
        'current_user': current_user,
        'recent_posts': recent_posts
    }
