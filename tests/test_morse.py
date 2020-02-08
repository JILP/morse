import pytest

from meli.morse.domain.morse import MorseFormat
from meli.morse.domain.morse import MorseTranslator
from meli.morse.domain.alphabet import international
from meli.morse.domain.decoder.naive_decoder import NaiveBitDecoder
from meli.morse.domain.timing.international import InternationalTiming


@pytest.fixture(scope='class')
def translator():
    alpha2morse = international.international_code
    morse_format = MorseFormat()
    morse_format.inter_word = ' / '
    bit_decoder = NaiveBitDecoder()
    return MorseTranslator(alpha2morse, bit_decoder, morse_format)


class TestMorseTranslator:

    def test_text2morse(self, translator, text2morse):
        msg = text2morse[0]
        translated_msg = text2morse[1]
        assert translated_msg == translator.text2morse(msg)

    def test_invalid_text2morse(self, translator, invalid_text):
        with pytest.raises(ValueError):
            translator.text2morse(invalid_text)

    def test_morse2text(self, translator, morse2text):
        msg = morse2text[0]
        translated_msg = morse2text[1]
        assert translated_msg == translator.morse2text(msg)

    def test_invalid_morse2text(self, translator, invalid_morse):
        with pytest.raises(ValueError):
            translator.morse2text(invalid_morse)

    def test_invalid_format_morse2text(self):
        alpha2morse = international.international_code
        morse_format = MorseFormat()
        morse_format.inter_char = ' '
        morse_format.inter_word = '  '
        bit_decoder = NaiveBitDecoder()
        translator = MorseTranslator(alpha2morse, bit_decoder, morse_format)
        invalid_morse = '.- .-   .-'
        with pytest.raises(ValueError):
            translator.morse2text(invalid_morse)

    def test_bits2text(self, translator, bits2text):
        msg = bits2text[0]
        translated_msg = bits2text[1]
        assert translated_msg == translator.bits2text(msg)

    def test_invalid_bits2text(self, translator, invalid_bits):
        with pytest.raises(ValueError):
            translator.bits2text(invalid_bits)

    def test_morse2bits(self, translator, morse2bits):
        morse = morse2bits[0]
        bits = morse2bits[1]
        assert bits == translator.morse2bits(morse, InternationalTiming(1))

    def test_morse2bits_invalid_input(self, translator, invalid_morse):
        with pytest.raises(ValueError):
            translator.morse2bits(invalid_morse, InternationalTiming(1))
