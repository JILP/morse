import flask

from meli.morse.app.api import api
from meli.morse.app.api.errors import bad_request
from meli.morse.app.api.errors import validation_error
from meli.morse.app.exceptions import ValidationError
from meli.morse.domain.morse import MorseFormat
from meli.morse.domain.morse import MorseTranslator


@api.route('/2text', methods=['POST'])
def translate2text():
    req_params = flask.request.get_json()
    msg = req_params['msg']

    try:
        verify_msg(msg)
    except ValidationError as verr:
        return validation_error(verr)

    mformat = MorseFormat()
    msg_format = msg.get('format')
    if msg_format:
        mformat.dot = msg_format.get('dot', mformat.dot)
        mformat.dash = msg_format.get('dash', mformat.dash)
        mformat.intra_char = msg_format.get('intra_char', mformat.intra_char)
        mformat.inter_char = msg_format.get('inter_char', mformat.inter_char)
        mformat.inter_word = msg_format.get('inter_word', mformat.inter_word)

    morse_translator = MorseTranslator(morse_format=mformat)

    src = msg['src']
    content = msg['content']

    try:
        if src == 'morse':
            translation = morse_translator.morse2text(content)
        else:
            translation = morse_translator.bits2text(content)
    except ValueError as verr:
        return bad_request(str(verr))

    res = {
        'msg': {
            'content': translation,
            'src': 'text'
        }
    }
    return flask.jsonify(res)


@api.route('/2morse', methods=['POST'])
def translate2morse():
    pass


def verify_msg(msg):
    if 'content' not in msg or 'src' not in msg:
        raise ValidationError('Message not valid')

    src = msg['src']
    if src not in ('morse', 'bits'):
        raise ValidationError('Message source not valid')

    content = msg['content']
    limit = flask.current_app.config['MESSAGE_SIZE_LIMIT']
    if len(content) > limit:
        raise ValidationError('Character limit exceeded ({limit})')
