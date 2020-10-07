from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired()])
    sequence = IntegerField('Sequence')
    submit = SubmitField('Create')
