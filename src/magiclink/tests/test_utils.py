from magiclink.utils import generate_token


def test_generate_token():
    token = generate_token()

    assert type(token) is str
