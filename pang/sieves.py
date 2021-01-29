def gen_pitches_from_sieve(sieve, origin, low, high):
    r"""
    Generates pitches from a sieve (an abjad.Pattern object).
    ..  container:: example

        A simple sieve:

        >>> import abjad
        >>> sieve = abjad.Pattern(indices=[0, 1, 7], period=12)
        >>> gen_pitches_from_sieve(sieve=sieve, origin=6, low=-12, high=11)
        [-11, -6, -5, 1, 6, 7]
    """
    return [
        p for p in range(low, high) if sieve.matches_index(p, high - low + 1, -origin)
    ]
