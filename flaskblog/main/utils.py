from flaskblog import db
from flaskblog.models import AccessCount
from flask_login import current_user


def update_and_init_access_count():
    access_count = AccessCount.query.first()
    if not access_count:
        access_count = AccessCount()
        db.session.add(access_count)
        db.session.commit()

    if not current_user.is_authenticated:
        access_count.count += 1
        db.session.commit()
