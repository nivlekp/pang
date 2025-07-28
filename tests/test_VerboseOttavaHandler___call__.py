import abjad
import pang


def test_VerboseOttavaHandler___call___01() -> None:
    voice = abjad.Voice(r"c''''4 c'4 c'4 c''''4")
    handler = pang.VerboseOttavaHandler()
    handler(voice)
    string = abjad.lilypond(voice)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            c''''4
            ^ \markup { c }
            c'4
            c'4
            c''''4
            ^ \markup { c }
        }
        """
    ), print(string)


def test_VerboseOttavaHandler___call___02() -> None:
    voice = abjad.Voice(r"c,,,4 c,4 c,4 c,,,4")
    clef = abjad.Clef("bass")
    abjad.attach(clef, pang.get.leaf(voice, 0))
    handler = pang.VerboseOttavaHandler()
    handler(voice)
    string = abjad.lilypond(voice)
    assert string == abjad.string.normalize(
        r"""
        \new Voice
        {
            \clef "bass"
            c,,,4
            _ \markup { c }
            c,4
            c,4
            c,,,4
            _ \markup { c }
        }
        """
    ), print(string)
