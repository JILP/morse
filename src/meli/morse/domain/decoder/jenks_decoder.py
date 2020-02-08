import jenkspy


def decode(self, bit_msg, morse_format):
    if not bit_msg:
        raise ValueError(f'Invalid bit sequence: "{bit_msg}"')

    len_set = {'0': set(), '1': set()}

    # Remove enclosing zeroes transmission noise
    bit_msg = bit_msg.strip('0').strip()

    parsed = []
    prev = None
    count = 1
    for bit in bit_msg:
        if bit not in ('0', '1'):
            raise ValueError(f'Invalid bit: "{bit}"')
        if bit == prev:
            count += 1
            continue
        len_set[prev].add(count)
        if prev is not None:    # Avoid first initial None element
            parsed.append((prev, count))
        count = 1
        prev = bit
    # Process last bit sequence
    len_set[bit].add(count)
    parsed.append((bit, count))

    space_breaks = jenkspy.jenks_breaks(len_set['0'], 3)
    pulse_breaks = jenkspy.jenks_breaks(len_set['1'], 2)

    normalized = []
    for bit, count in parsed:
        if bit == '1':
            is_dot = count <= pulse_breaks[1]           # first break
            seq = morse_format.dot if is_dot else morse_format.dash
        else:
            is_intra_char = count <= space_breaks[1]    # first break
            is_inter_word = count > space_breaks[2]     # second break
            if is_intra_char:
                seq = morse_format.intra_char
            elif is_inter_word:
                seq = morse_format.inter_word
            else:
                seq = morse_format.inter_char
        normalized.append(seq)

    return ''.join(normalized)
