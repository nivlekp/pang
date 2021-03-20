def gen_pitches_from_sieve(sieve, origin, low=None, high=None, pitch_range=None):
    r"""
    Generates pitches from a sieve (an ``abjad.Pattern`` object).
    ..  container:: example

        A simple sieve:

        >>> sieve = abjad.Pattern(indices=[0, 1, 7], period=12)
        >>> pang.gen_pitches_from_sieve(sieve=sieve, origin=6, low=-12, high=11)
        [-11, -6, -5, 1, 6, 7]
    """
    if pitch_range is not None:
        assert isinstance(pitch_range, tuple)
        low = pitch_range[0].number
        high = pitch_range[1].number
    return [
        p for p in range(low, high) if sieve.matches_index(p, high - low + 1, -origin)
    ]
