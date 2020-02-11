import flask

from . import main
from .forms import MessageForm
from meli.morse.app.swagger import SWAGGER_URL

@main.route('/', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        form.translated_msg.data = 'translated > ' + form.msg.data
        flask.session['msg'] = form.msg.data
        flask.session['translated_msg'] = form.translated_msg.data
        return flask.redirect(flask.url_for('main.index'))

    form.msg.data = flask.session.get('msg')
    form.translated_msg.data = flask.session.get('translated_msg')
    return flask.render_template('index.html',
                                 form=form,
                                 msg=flask.session.get('msg'),
                                 translate_api = flask.url_for("main.index") + SWAGGER_URL)
