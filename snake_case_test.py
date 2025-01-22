from main import to_snake_case


def test_single_word():
    assert to_snake_case("Word") == "word"


def test_camel_case():
    assert to_snake_case("CamelCase") == "camel_case"


def test_acronyms():
    assert to_snake_case("FOBPayCode") == "fob_pay_code"
    assert to_snake_case("PayFOBCode") == "pay_fob_code"


def test_trailing_uppercase():
    assert to_snake_case("UserID") == "user_id"
    assert to_snake_case("OrderFOB") == "order_fob"


def test_mixed_cases():
    assert to_snake_case("UserOrderID") == "user_order_id"
    assert to_snake_case("HTTPRequestID") == "http_request_id"


def test_lowercase_input():
    assert to_snake_case("lowercase") == "lowercase"


def test_numbers_in_text():
    assert to_snake_case("Version2Code") == "version2_code"
