import secrets
import os
from PIL import Image
from flask import url_for, current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    sg_token = os.environ['SG_TOKEN']
    message = Mail(
                from_email='noreply@example.com',
                to_emails=[user.email],
                subject='Password Reset Request',
                html_content=f'''<p>To reset your password, visit the following link:</p></br>
                    <a href="{url_for('users.reset_token', token=token, _external=True)}">Reset Password</a></br>
                    <p>If you did not make this request, then simply ignore this email</p>
                ''')

    sg = SendGridAPIClient(sg_token)
    sg.send(message)
