from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    msg = TextAreaField('From text',
                        render_kw={"placeholder": "what is your message?"},
                        validators=[DataRequired()])
    translated_msg = TextAreaField('To morse', render_kw={'readonly': True})
    submit = SubmitField('Translate')
