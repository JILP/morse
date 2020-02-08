from meli.morse.domain.timing.morse_timing import MorseTiming


class InternationalTiming(MorseTiming):

    def __init__(self, dot_len):
        self.dot = dot_len
        self.dash = 3 * dot_len
        self.intra_char = 1 * dot_len
        self.inter_char = 3 * dot_len
        self.inter_word = 7 * dot_len
