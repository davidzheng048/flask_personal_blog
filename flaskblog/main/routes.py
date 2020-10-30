from flask import render_template, request, redirect, Blueprint, url_for
from flaskblog.models import Post, Category, AccessCount
from flask_login import current_user
from flaskblog.main.utils import update_and_init_access_count

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    update_and_init_access_count()
    return render_template('main/home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')


@main.route("/future_feature")
def future_feature():
    return render_template('main/future_feature.html', title='待完成的功能')


@main.route("/search", methods=['GET', 'POST'])
def search():
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)

    if not keyword:
        return redirect(url_for('main.home'))

    posts = Post.query.filter(Post.title.contains(keyword)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    post_count = Post.query.filter(Post.title.contains(keyword)).count()  # If switch to postgres then stop using this

    return render_template('main/search.html', posts=posts, keyword=keyword, post_count=post_count, page=page)


@main.app_context_processor
def context_processor():
    categories_sorted_by_sequence = Category.query.order_by(Category.sequence.desc()).all()
    categories_sorted_by_id = Category.query.order_by(Category.id.asc()).all()
    recent_posts = Post.query.order_by(Post.id.desc()).limit(3).all()
    access_count = AccessCount.query.first().count
    return {
        'categories_sorted_by_sequence': categories_sorted_by_sequence,
        'categories_sorted_by_id': categories_sorted_by_id,
        'current_user': current_user,
        'recent_posts': recent_posts,
        'access_count': access_count,
        'site_url': request.base_url
    }
