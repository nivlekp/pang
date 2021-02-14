import abjad
import pang


def test_pad_voices_with_grace_skips_01():
    voice_0 = abjad.Voice("{ c'4 c'4 c'4 c'4 }")
    voice_1 = abjad.Voice("{ c'4 c'4 c'4 c'4 }")
    container = abjad.BeforeGraceContainer("cs'16")
    abjad.attach(container, abjad.get.leaf(voice_0, 0))
    # assert False, print([component._parent for component in abjad.iterate([voice_0, voice_1]).timeline()])
    pang.pad_voices_with_grace_skips([voice_0, voice_1])

    string = abjad.lilypond(voice_0)
    assert string == abjad.String.normalize(
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
    assert string == abjad.String.normalize(
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
