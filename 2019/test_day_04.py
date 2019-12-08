def password_is_valid(password: int) -> bool:
    password = str(password)
    previous = -1
    run_len = 0
    double = False
    for p in password:
        if previous > int(p):
            return False
        if previous == int(p):
            run_len += 1
        else:
            if run_len == 1:
                double = True
            run_len = 0
        previous = int(p)
    if run_len == 1:
        double = True
    return double


def test_password_is_valid_returns_true_when_input_has_repeated_string():
    assert password_is_valid(123455)


def test_password_is_valid_returns_false_when_input_has_no_repeated_string():
    assert not password_is_valid(123456)


def test_password_is_valid_returns_false_when_input_has_only_repeated_string_longer_than_2():
    assert not password_is_valid(122256)


def test_password_is_valid_returns_true_if_values_do_not_decrease():
    assert password_is_valid(124456)


def test_password_is_valid_returns_false_if_values_do_decrease():
    assert not password_is_valid(123450)

MYINPUT_MIN = 152085
MYINPUT_MAX = 670283

def test_submission():
    assert sum([1 if password_is_valid(d) else 0 for d in range(MYINPUT_MIN,MYINPUT_MAX+1)]) == 1196 # orig 1764