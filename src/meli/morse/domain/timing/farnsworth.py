from meli.morse.domain.timing.morse_timing import MorseTiming


class FarnsworthTiming(MorseTiming):

    def __init__(self, dot_len, farnsworth_len):
        if dot_len >= farnsworth_len:
            raise ValueError(f'len(Farnswoth) must be greater than len(Dot)')

        self.dot = dot_len
        self.dash = 3 * dot_len
        self.intra_char = 1 * dot_len
        self.inter_char = 3 * farnsworth_len
        self.inter_word = 7 * farnsworth_len
