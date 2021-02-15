import abjad
import pang


def test_ManualOttavaHandler___call___01():
    voice = abjad.Voice(r"c''4 c''4 c''4 c''4")
    handler = pang.ManualOttavaHandler(n=1)
    handler(voice)
    string = abjad.lilypond(voice)
    assert string == abjad.String.normalize(
        r"""
        \new Voice
        {
            \ottava 1
            c''4
            c''4
            c''4
            c''4
        }
        """
    ), print(string)


def test_ManualOttavaHandler___call___02():
    voice_0 = abjad.Voice(r"c'''4 c'''4 c'''4 c'''4")
    voice_1 = abjad.Voice(r"c''4 c''4 c''4 c''4")
    handler = pang.ManualOttavaHandler(n=1)
    handler(voice_0)
    staff = abjad.Staff([voice_0, voice_1], simultaneous=True)
    string = abjad.lilypond(staff)
    abjad.show(staff)
    assert string == abjad.String.normalize(
        r"""
        \new Staff
        <<
            \new Voice
            {
                \ottava 1
                c'''4
                c'''4
                c'''4
                c'''4
            }
            \new Voice
            {
                c''4
                c''4
                c''4
                c''4
            }
        >>
        """
    ), print(string)
