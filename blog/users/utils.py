import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from blog import app, mail


# save profile pictures into /static/pictures folder
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # make random hex string
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_name)
    # resize picture before save it
    output_size = (100, 100)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    # save it
    img.save(picture_path)
    return picture_name


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='noreply@gmail.com',
                  recipients=[user.email])
    # user _external to get an absolute URL rather than relative URL
    msg.body = f'''To reset your password, vist the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    If you did not make this request, please ignore this email changes be made
    '''
    # send the mail to user's mail
    mail.send(msg)
