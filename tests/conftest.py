"""
Morse Code Translator pytest configuration.
"""

import os

import pytest

from meli.morse.app import create_app


TEXT2MORSE = (
    ('e', '.'),
    ('ee', '. .'),
    ('e e', '. / .'),
    ('hello world', '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'),
    ('HELLO WORLD.', '.... . .-.. .-.. --- / .-- --- .-. .-.. -.. .-.-.-'),
    ('HELLOWORLD', '.... . .-.. .-.. --- .-- --- .-. .-.. -..'),
    ('HELLO         WORLD', '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'),
    ('HELLO     WORLD  ', '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'),
    ('  HELLO     WORLD', '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'),
    ('  HELLO     WORLD  ', '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'),
    ('HELLO MELI', '.... . .-.. .-.. --- / -- . .-.. ..'),
    ('The quick brown fox jumps over the lazy dog',
     '- .... . / --.- ..- .. -.-. -.- / -... .-. --- .-- -. / ..-. --- '
     + '-..- / .--- ..- -- .--. ... / --- ...- . .-. / - .... . / .-.. '
     + '.- --.. -.-- / -.. --- --.'),
)


MORSE2BITS = (
    ('.', '1'),
    ('..', '101'),
    ('. / .', '100000001'),
    ('.... . .-.. .-.. --- / .-- --- .-. .-.. -..',
     '10101010001000101110101000101110101000111011101110000000'
     + '1011101110001110111011100010111010001011101010001110101'),
)


BITS2MORSE = (
    ('1', '.'),
    ('111', '.'),
    ('101', '..'),
    ('10101010001000101110101000101110101000111011101110000000'
     + '1011101110001110111011100010111010001011101010001110101',
     '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'),
     ('10110101000100010111110101000101111101010001111011110111110000000'
     + '10111101111000111101111011110001011110100010111110101000111110101',
     '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'),
)


BITS2TEXT = (
    ('1', 'E'),
    ('101', 'I'),
    ('10101010001000101110101000101110101000111011101110000000'
     + '1011101110001110111011100010111010001011101010001110101',
     'HELLO WORLD'),
    ('10101010001000101110101000101110101000111011101110000000'
     + '1011101110001110111011100010111010001011101010001110101',
     'HELLO WORLD'),
    ('110110110110001100011011110110110001101111011011000111101111011110000000'
     + '11011110111100011110111101111000110111101100011011110110110001111011011'
     + '0000001',
     'HELLO WORLD E'),

)


TEXT2BITS = (
    ('E', '1'),
    ('I', '101'),
    ('HELLO WORLD',
     '10101010001000101110101000101110101000111011101110000000'
     + '1011101110001110111011100010111010001011101010001110101'),
    ('HELLO WORLD',
     '10101010001000101110101000101110101000111011101110000000'
     + '1011101110001110111011100010111010001011101010001110101'),
)


MORSE2TEXT = (
    ('.', 'E'),
    ('..', 'I'),
    ('.... . .-.. .-.. --- / .-- --- .-. .-.. -..', 'HELLO WORLD'),
    ('.... . .-.. .-.. --- / .-- --- .-. .-.. -.. .-.-.-', 'HELLO WORLD.'),
    ('.... . .-.. .-.. --- .-- --- .-. .-.. -..', 'HELLOWORLD'),
    ('.... . .-.. .-.. --- / -- . .-.. ..', 'HELLO MELI'),
    ('- .... . / --.- ..- .. -.-. -.- / -... .-. --- .-- -. / ..-. --- '
     + '-..- / .--- ..- -- .--. ... / --- ...- . .-. / - .... . / .-.. '
     + '.- --.. -.-- / -.. --- --.',
     'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG'),
)


INVALID_MORSE = (
    '',
    '.-A',
    '1111',
    'Hola #',
    '.      .',
)


INVALID_TEXT = (
    '#',
    '$',
    'Hola #',
)


INVALID_BITS = (
    '',
    '00000',
    '0A',
    '11A11',
    '01 ',
    ' 01',
    '0 1'
)


@pytest.fixture(scope='module', params=MORSE2TEXT)
def morse2text(request):
    return request.param


@pytest.fixture(scope='module', params=MORSE2BITS)
def morse2bits(request):
    return request.param


@pytest.fixture(scope='module', params=INVALID_MORSE)
def invalid_morse(request):
    return request.param


@pytest.fixture(scope='module', params=BITS2TEXT)
def bits2text(request):
    return request.param


@pytest.fixture(scope='module', params=BITS2MORSE)
def bits2morse(request):
    return request.param


@pytest.fixture(scope='module', params=INVALID_BITS)
def invalid_bits(request):
    return request.param


@pytest.fixture(scope='module', params=TEXT2MORSE)
def text2morse(request):
    return request.param


@pytest.fixture(scope='module', params=TEXT2BITS)
def text2bits(request):
    return request.param


@pytest.fixture(scope='module', params=INVALID_TEXT)
def invalid_text(request):
    return request.param


@pytest.fixture(scope='module')
def test_client():
    app = create_app(os.getenv('FLASK_CONFIG') or 'test')

    # Flask provides a way to test your application by exposing the
    # Werkzeug test Client and handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
