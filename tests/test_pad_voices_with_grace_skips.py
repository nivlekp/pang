import abjad
import pang


def test_pad_voices_with_grace_skips_01():
    voice_0 = abjad.Voice("{ c'4 c'4 c'4 c'4 }")
    voice_1 = abjad.Voice("{ c'4 c'4 c'4 c'4 }")
    container = abjad.BeforeGraceContainer("cs'16")
    abjad.attach(container, abjad.get.leaf(voice_0, 0))
    pang.pad_voices_with_grace_skips([voice_0, voice_1])

    string = abjad.lilypond(voice_0)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                \grace {
                    cs'16
                }
                c'4
                c'4
                c'4
                c'4
            }
        }
        """
    ), print(string)

    string = abjad.lilypond(voice_1)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                \grace {
                    s16
                }
                c'4
                c'4
                c'4
                c'4
            }
        }
        """
    ), print(string)


def test_pad_voices_with_grace_skips_02():
    voice_0 = abjad.Voice(r"{ \tuplet 5/4 { c'4 c'4 c'4 c'4 c'4 } }")
    voice_1 = abjad.Voice(r"{ \tuplet 6/4 { c'4 c'4 c'4 c'4 c'4 c'4 } }")
    container = abjad.BeforeGraceContainer("cs'16")
    abjad.attach(container, abjad.get.leaf(voice_0, 0))
    pang.pad_voices_with_grace_skips([voice_0, voice_1])

    string = abjad.lilypond(voice_0)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                \tuplet 5/4
                {
                    \grace {
                        cs'16
                    }
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                }
            }
        }
        """
    ), print(string)

    string = abjad.lilypond(voice_1)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                \tuplet 6/4
                {
                    \grace {
                        s16 * 6/5
                    }
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                }
            }
        }
        """
    ), print(string)


def test_pad_voices_with_grace_skips_03():
    voice_0 = abjad.Voice(r"{ \tuplet 5/4 { c'4 c'4 c'4 c'4 c'4 } }")
    voice_1 = abjad.Voice(r"{ \tuplet 6/4 { c'4 c'4 c'4 c'4 c'4 c'4 } }")
    container = abjad.BeforeGraceContainer("cs'16")
    abjad.attach(container, abjad.get.leaf(voice_0, 0))
    container = abjad.BeforeGraceContainer("ds'16")
    abjad.attach(container, abjad.get.leaf(voice_1, 0))
    pang.pad_voices_with_grace_skips([voice_0, voice_1])

    string = abjad.lilypond(voice_0)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                \tuplet 5/4
                {
                    \grace {
                        cs'16
                    }
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                }
            }
        }
        """
    ), print(string)

    string = abjad.lilypond(voice_1)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            {
                \tuplet 6/4
                {
                    \grace {
                        ds'16 * 6/5
                    }
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                    c'4
                }
            }
        }
        """
    ), print(string)
