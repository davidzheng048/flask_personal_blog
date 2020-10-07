from flaskblog import db
from flaskblog.models import AccessCount


def update_and_init_access_count():
    access_count = AccessCount.query.first()
    if not access_count:
        access_count = AccessCount()
        db.session.add(access_count)
        db.session.commit()

    else:
        access_count.count += 1
        db.session.commit()

    print(access_count.count)
