import pytest
from lib.hello_world import hello_world, good_night, hello_goodbye


def test_hello_world_default():
    assert hello_world() == "string-0"


def test_hello_world_custom():
    assert hello_world(5) == "string-5"


def test_good_night():
    assert good_night() == "string"


def test_hello_goodbye(capsys):
    hello_goodbye()
    captured = capsys.readouterr()
    assert captured.out == "hello world\ngood night\n"
