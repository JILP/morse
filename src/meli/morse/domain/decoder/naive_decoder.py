from meli.morse.domain.timing.international import InternationalTiming
from meli.morse.domain.decoder.bit_decoder import BitDecoder


class NaiveBitDecoder(BitDecoder):

    def decode(self, bit_msg, morse_format):
        if not bit_msg:
            raise ValueError(f'Invalid bit sequence: "{bit_msg}"')

        min_len = 99999

        # Remove enclosing zeroes transmission noise
        bit_msg = bit_msg.strip('0')

        parsed = []
        prev = None
        count = 1
        for bit in bit_msg:
            if bit not in ('0', '1'):
                raise ValueError(f'Invalid bit: "{bit}"')
            if bit == prev:
                count += 1
                continue
            if prev == '1' and count < min_len:
                min_len = count
            if prev is not None:    # Avoid first initial None element
                parsed.append((prev, count))
            count = 1
            prev = bit
        # Process last bit sequence
        if bit == '1' and count < min_len:
            min_len = count
        parsed.append((bit, count))

        timing = InternationalTiming(min_len)

        normalized = []
        for bit, count in parsed:
            if bit == '1':
                is_dot = abs(timing.dot - count) < abs(timing.dash - count)
                seq = morse_format.dot if is_dot else morse_format.dash
            else:
                is_intra_char = (abs(timing.intra_char - count)
                                 < abs(timing.inter_char - count))
                is_inter_word = (abs(timing.inter_word - count)
                                 < abs(timing.inter_char - count))
                if is_intra_char:
                    seq = morse_format.intra_char
                elif is_inter_word:
                    seq = morse_format.inter_word
                else:
                    seq = morse_format.inter_char
            normalized.append(seq)

        return ''.join(normalized)
