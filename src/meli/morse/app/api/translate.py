import flask

from meli.morse.app.api import api
from meli.morse.app.api.errors import bad_request
from meli.morse.app.api.errors import validation_error
from meli.morse.app.exceptions import ValidationError
from meli.morse.domain.morse import MorseFormat
from meli.morse.domain.morse import MorseTranslator


@api.route('/2text', methods=['POST'])
def translate2text():
    try:
        verify_request(flask.request, target='text')
    except ValidationError as verr:
        return validation_error(verr)

    req_params = flask.request.get_json()
    msg = req_params['msg']
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
            'src': 'text',
            'content': translation
        }
    }
    return flask.jsonify(res)


@api.route('/2morse', methods=['POST'])
def translate2morse():
    try:
        verify_request(flask.request, target='morse')
    except ValidationError as verr:
        return validation_error(verr)

    req_params = flask.request.get_json()
    msg = req_params['msg']
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
        if src == 'text':
            translation = morse_translator.text2morse(content)
        else:
            translation = morse_translator.bits2morse(content)
    except ValueError as verr:
        return bad_request(str(verr))

    res = {
        'msg': {
            'src': 'morse',
            'content': translation,
            'format': mformat.to_dict()
        }
    }
    return flask.jsonify(res)


@api.route('/2bits', methods=['POST'])
def translate2bits():
    try:
        verify_request(flask.request, target='bits')
    except ValidationError as verr:
        return validation_error(verr)

    req_params = flask.request.get_json()
    msg = req_params['msg']
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
        if src == 'text':
            translation = morse_translator.text2bits(content)
        else:
            translation = morse_translator.morse2bits(content)
    except ValueError as verr:
        return bad_request(str(verr))

    #print()
    #print('#'*80)
    #print(mformat.to_dict())
    #print('#'*80)

    res = {
        'msg': {
            'src': 'bits',
            'content': translation
        }
    }
    return flask.jsonify(res)


def verify_request(req, target):
    
    if req.content_type != 'application/json':
        raise ValidationError('Invalid content type: "{req.content_type}"')
    
    req_params = req.get_json()
    
    if 'msg' not in req_params:
        raise ValidationError('Missing msg attribute')
        
    msg = req_params['msg']

    if 'content' not in msg or 'src' not in msg:
        raise ValidationError('Message not valid')

    src = msg['src']
    if src == target or src not in ('text', 'morse', 'bits'):
        raise ValidationError('Message source not valid')

    content = msg['content']
    limit = flask.current_app.config['MESSAGE_SIZE_LIMIT']
    if len(content) > limit:
        raise ValidationError('Character limit exceeded ({limit})')
