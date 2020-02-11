class BitDecoder:

    def encode(self, morse_msg, morse_format, timing):
        if isinstance(morse_msg, int):
            morse_msg = bin(morse_msg)[2:]

        symbol_gap = '0' * timing.intra_char
        char_gap = '0' * timing.inter_char
        word_gap = '0' * timing.inter_word

        words = morse_msg.split(morse_format.inter_word)

        encoded_word = []
        for w in words:
            encoded_char = []
            for morse_char in w.split(morse_format.inter_char):
                encoded_symbol = []
                if morse_format.intra_char:
                    morse_char = morse_char.split(morse_format.intra_char)

                if not morse_char:
                    raise ValueError(f'Invalid morse word: "{w}"')

                for symbol in morse_char:
                    encoded_symbol.append(
                        self.encode_symbol(symbol, morse_format, timing))
                encoded_char.append(symbol_gap.join(encoded_symbol))
            encoded_word.append(char_gap.join(encoded_char))

        return word_gap.join(encoded_word)

    def encode_symbol(self, symbol, morse_format, timing):
        if symbol not in (morse_format.dot, morse_format.dash):
            raise ValueError(f'Invalid morse simbol: "{symbol}"')
        duration = timing.dot if symbol == morse_format.dot else timing.dash
        return '1' * duration
    
    def decode(self, bit_msg, morse_format):
        pass
