"""
Morse Code Translator

Implements morse encoding/decoding functions
"""

from meli.morse.domain.alphabet.international import international_code
from meli.morse.domain.decoder.naive_decoder import NaiveBitDecoder as Naive


class MorseFormat:

    def __init__(self):
        self.dot = '.'
        self.dash = '-'
        self.intra_char = ''
        self.inter_char = ' '
        self.inter_word = ' ' * 4


class MorseTranslator:

    def __init__(self, alphabet=None, bit_decoder=None, morse_format=None):
        self.alpha2morse = alphabet or international_code
        self.morse2alpha = {v: k for k, v in self.alpha2morse.items()}
        self.format = morse_format or MorseFormat()
        self.bit_decoder = bit_decoder or Naive()

    def bits2text(self, msg):
        morse = self.bits2morse(msg)
        return self.morse2text(morse)

    def morse2text(self, msg):
        inter_char = self.format.inter_char
        morse_words = msg.split(sep=self.format.inter_word)
        text_words = map(lambda w: ''.join([self.decode_morse2text(code)
                                            for code in w.split(inter_char)]),
                         morse_words)
        return ' '.join(text_words)

    def decode_morse2text(self, code):
        if code not in self.morse2alpha:
            raise ValueError(f'Invalid morse code: "{code}"')
        return self.morse2alpha[code].upper()

    def text2morse(self, msg):
        char_sep = self.format.inter_char
        text_words = str.upper(msg).split()
        m_words = map(lambda w: char_sep.join([self.encode_text2morse(char)
                                               for char in w]),
                      text_words)
        return self.format.inter_word.join(m_words)

    def encode_text2morse(self, char):
        if char not in self.alpha2morse:
            raise ValueError(f'Invalid character: "{char}"')
        return self.alpha2morse[char]

    def morse2bits(self, msg, timing):
        return self.bit_decoder.encode(msg, self.format, timing)

    def bits2morse(self, bit_msg):
        return self.bit_decoder.decode(bit_msg, self.format)
