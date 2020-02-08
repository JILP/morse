"""
Morse Code Translator pytest configuration.
"""

import os

import pytest

from meli.morse.app import create_app


TEXT2MORSE = (
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
    ('.... . .-.. .-.. --- / .-- --- .-. .-.. -..',
     '10101010001000101110101000101110101000111011101110000000'
     + '1011101110001110111011100010111010001011101010001110101'),
)


BITS2TEXT = (
    ('10101010001000101110101000101110101000111011101110000000'
     + '1011101110001110111011100010111010001011101010001110101',
     'HELLO WORLD'),
    ('10101010001000101110101000101110101000111011101110000000'
     + '1011101110001110111011100010111010001011101010001110101',
     'HELLO WORLD'),
)


MORSE2TEXT = (
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


@pytest.fixture(scope='module', params=INVALID_BITS)
def invalid_bits(request):
    return request.param


@pytest.fixture(scope='module', params=TEXT2MORSE)
def text2morse(request):
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
