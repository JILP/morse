from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    msg = TextAreaField('What is your message?',
                        render_kw={"placeholder": "what is your message?"},
                        validators=[DataRequired()])
    translated_msg = TextAreaField('')
    submit = SubmitField('Translate')
