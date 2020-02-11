import flask

from . import main
from .forms import MessageForm
from meli.morse.app.swagger import SWAGGER_URL
from meli.morse.domain.morse import MorseTranslator

TRANSLATOR = MorseTranslator()

@main.route('/', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        try:
            form.translated_msg.data = TRANSLATOR.text2morse(form.msg.data)
        except ValueError as verr:
            form.translated_msg.data = ''
            flask.flash(verr.args[0])
        flask.session['msg'] = form.msg.data
        flask.session['translated_msg'] = form.translated_msg.data
        return flask.redirect(flask.url_for('main.index'))

    form.msg.data = flask.session.get('msg')
    form.translated_msg.data = flask.session.get('translated_msg')
    return flask.render_template('index.html',
                                 form=form,
                                 msg=flask.session.get('msg'),
                                 translate_api = flask.url_for("main.index",
                                                               _external=True)
                                                 + SWAGGER_URL[1:])
