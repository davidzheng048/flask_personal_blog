from flask import Blueprint, request
from flask import render_template, request
from flaskblog.models import Post, Category, AccessCount
from flask_login import current_user
from flaskblog.main.utils import update_and_init_access_count

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    update_and_init_access_count()
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/future_feature")
def future_feature():
    return render_template('future_feature.html', title='待完成的功能')


@main.app_context_processor
def context_processor():
    categories = Category.query.order_by(Category.sequence.desc()).all()
    for i in categories:
        print(i.name)
    recent_posts = Post.query.order_by(Post.id.desc()).limit(3).all()
    access_count = AccessCount.query.first().count
    return {
        'categories': categories,
        'current_user': current_user,
        'recent_posts': recent_posts,
        'access_count': access_count,
        'site_url': request.base_url
    }
