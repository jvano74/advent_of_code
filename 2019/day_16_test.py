SUBMISSION = '5977603409581164454536779317998960214094871440623469497289448506' \
             '6523525742503986771912019032922788494900655855458086979764617375' \
             '5808025589635870257849188822196108319409923992017823856742232844' \
             '1149923761980019387976866821016217639460750221860263315377206297' \
             '3149533650562554942574593878073238232563649673858167635378695190' \
             '3561597963422047593931562946583662799227342133851448951166497681' \
             '8596686620241331493969217422321048493367886647894410497889001972' \
             '8562001417746656699281992028356004888860103805472866615243544781' \
             '3777486544717505608300990487475709259025757650548988995123039171' \
             '5913809737533844461080989166709405110835913401712802817423072039' \
             '8965960712'


def test_submission_length():
    assert len(SUBMISSION) == 650


def get_kernel(k_len, pos):
    kernel = []
    cnt = 1
    while True:
        for e in [0, 1, 0, -1]:
            while cnt < pos:
                kernel.append(e)
                cnt += 1
                if len(kernel) == k_len:
                    return kernel
            cnt = 0


def apply_fft(input_msg):
    out_msg = []
    k_len = len(input_msg)
    pos = 0
    while pos < k_len:
        pos += 1
        d_out = 0
        kernel = get_kernel(k_len, pos)
        for k, d_in in zip(kernel, input_msg):
            d_out += k * d_in
        if d_out < 0:
            d_out = -d_out
        d_out %= 10
        out_msg.append(d_out)
    return out_msg


def end_of_long_fft(seq, start):
    focus = seq[(start - 1):]
    focus.reverse()
    for _ in range(100):
        s = 0
        new_focus = []
        for d in focus:
            s = (s + d) % 10
            new_focus.append(s)
        focus = new_focus
    focus.reverse()
    return ''.join([str(d) for d in focus[1:9]])


def test_part2_long_fft():
    seq = [int(d) for d in '03036732577212944063491565474664'*10000]
    assert end_of_long_fft(seq, 303673) == '84462026'
    seq = [int(d) for d in '02935109699940807407585447034323'*10000]
    assert end_of_long_fft(seq, 293510) == '78725270'


def test_part2_submission():
    seq = [int(d) for d in SUBMISSION*10000]
    assert end_of_long_fft(seq, 5977603) == '23752579'


def test_submission_fft():
    sequence = [int(d) for d in SUBMISSION]
    for _ in range(100):
        sequence = apply_fft(sequence)
    assert ''.join([str(d) for d in sequence[0:8]]) == '89576828'


def test_larger_fft():
    sequence = [int(d) for d in '80871224585914546619083218645595']
    for _ in range(100):
        sequence = apply_fft(sequence)
    assert ''.join([str(d) for d in sequence[0:8]]) == '24176176'


def test_apply_fft():
    sequence = [1, 2, 3, 4, 5, 6, 7, 8]
    sequence = apply_fft(sequence)
    assert sequence == [4, 8, 2, 2, 6, 1, 5, 8]
    sequence = apply_fft(sequence)
    assert sequence == [3, 4, 0, 4, 0, 4, 3, 8]


def test_get_kernel():
    assert get_kernel(9, 1) == [1, 0, -1, 0, 1, 0, -1, 0, 1]
    assert get_kernel(9, 3) == [0, 0, 1, 1, 1, 0, 0, 0, -1]
