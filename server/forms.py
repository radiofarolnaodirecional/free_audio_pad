from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField

#disabled
class AddTrackForm(FlaskForm):
    name = StringField('name')
    url = FileField('url')
    img_url = FileField('img url')
    submit = SubmitField('submit')
