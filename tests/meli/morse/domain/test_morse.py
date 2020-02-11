import pytest

from meli.morse.domain.morse import decodeBits2Morse
from meli.morse.domain.morse import translate2human
from meli.morse.domain.morse import MorseFormat
from meli.morse.domain.morse import MorseTranslator
from meli.morse.domain.alphabet import international
from meli.morse.domain.decoder.jenks_decoder import JenksBitDecoder
from meli.morse.domain.decoder.naive_decoder import NaiveBitDecoder
from meli.morse.domain.timing.international import InternationalTiming


@pytest.fixture(scope='class')
def translator():
    alpha2morse = international.international_code
    morse_format = MorseFormat()
    morse_format.inter_word = ' / '
    bit_decoder = NaiveBitDecoder()
    return MorseTranslator(alpha2morse, bit_decoder, morse_format)


@pytest.fixture(scope='class')
def jenks_translator():
    alpha2morse = international.international_code
    morse_format = MorseFormat()
    morse_format.inter_word = ' / '
    bit_decoder = JenksBitDecoder()
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

    def test_bits2morse(self, translator, bits2morse):
        bits = bits2morse[0]
        morse = bits2morse[1]
        assert morse == translator.bits2morse(bits)

    def test_invalid_bits2morse(self, translator, invalid_bits):
        with pytest.raises(ValueError):
            translator.bits2morse(invalid_bits)

    def test_bits2morse_jenks(self, jenks_translator, bits2morse):
        bits = bits2morse[0]
        morse = bits2morse[1]
        assert morse == jenks_translator.bits2morse(bits)

    def test_invalid_bits2morse_jenks(self, jenks_translator, invalid_bits):
        with pytest.raises(ValueError):
            jenks_translator.bits2morse(invalid_bits)

    def test_morse2bits(self, translator, morse2bits):
        morse = morse2bits[0]
        bits = morse2bits[1]
        assert bits == translator.morse2bits(morse, InternationalTiming(1))

    def test_morse2bits_invalid_input(self, translator, invalid_morse):
        with pytest.raises(ValueError):
            translator.morse2bits(invalid_morse, InternationalTiming(1))

    def test_text2bits(self, translator, text2bits):
        text = text2bits[0]
        bits = text2bits[1]
        assert bits == translator.text2bits(text, InternationalTiming(1))

    def test_text2bits_invalid_input(self, translator, invalid_text):
        with pytest.raises(ValueError):
            translator.text2bits(invalid_text, InternationalTiming(1))


def test_decodeBits2Morse():
    morse = '-- . .-.. ..'  # MELI
    bits = '11101110001000101110101000101'        
    assert morse == decodeBits2Morse(bits)
    bits = int(bits, 2)
    assert morse == decodeBits2Morse(bits)
    bits = b'\x0e\x0e\x02\x02\x0e\x0a\x02\x08'
    assert morse == decodeBits2Morse(bits)


def test_translate2human():
    morse = '-- . .-.. ..'  # MELI
    text = 'MELI'
    assert text == translate2human(morse)
