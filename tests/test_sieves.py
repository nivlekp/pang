import abjad
import pang


def test_sieves_00():
    sieve = abjad.Pattern(indices=[0, 1], period=12)
    origin = 1
    low = -2
    high = 3
    pitches = pang.gen_pitches_from_sieve(sieve, origin, low, high)
    assert pitches == [1, 2]


def test_sieves_01():
    sieve = abjad.Pattern(indices=[0, 1, 7], period=12)
    origin = 6
    low = -12
    high = 11
    pitches = pang.gen_pitches_from_sieve(sieve, origin, low, high)
    assert pitches == [-11, -6, -5, 1, 6, 7]
