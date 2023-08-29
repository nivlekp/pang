def gen_pitches_from_sieve(
    sieve, origin=0, low=0, high=12, pitch_range=None, multiplier=1
):
    r"""
    Generates pitches from a sieve (an ``abjad.Pattern`` object).
    ..  container:: example

        A simple sieve:

        >>> sieve = abjad.Pattern(indices=[0, 1, 7], period=12)
        >>> pitches = pang.gen_pitches_from_sieve(sieve=sieve, origin=6, low=-12, high=11)
        >>> print(pitches)
        [-11, -6, -5, 1, 6, 7]

        >>> notes = abjad.makers.make_notes(pitches, [(1, 4)] * len(pitches))
        >>> staff = abjad.Staff(notes)
        >>> abjad.attach(abjad.Clef("bass"), staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \clef "bass"
                cs4
                fs4
                g4
                cs'4
                fs'4
                g'4
            }

    ..  container:: example

        Microtone sieves can also be created:

        >>> sieve = abjad.Pattern(indices=[0, 3], period=10)
        >>> pitches = pang.gen_pitches_from_sieve(sieve=sieve, origin=0, low=0, high=11, multiplier=0.5)
        >>> print(pitches)
        [0.0, 1.5, 5.0, 6.5, 10.0]

        >>> notes = abjad.makers.make_notes(pitches, [(1, 4)] * len(pitches))
        >>> staff = abjad.Staff(notes)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                dqf'4
                f'4
                gqf'4
                bf'4
            }

    """
    if pitch_range is not None:
        assert isinstance(pitch_range, tuple)
        low = pitch_range[0].number
        high = pitch_range[1].number
    low = int(low / multiplier)
    high = int(high / multiplier)
    return [
        p * multiplier
        for p in range(low, high)
        if sieve.matches_index(p, high - low + 1, -origin)
    ]
