import pang


def test_AtaxicCloud___init___01():
    sequence = pang.AtaxicCloud()
    assert sequence.nservers == 1
