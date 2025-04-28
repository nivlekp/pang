import abjad
import pang


def test_glissando_to_next_leaf() -> None:
    voice = abjad.Voice("c''4~ c''4~ c''4 f''4")
    pang.spanners.glissando_to_next_leaf(abjad.get.logical_tie(pang.get.leaf(voice, 0)))
    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c''4
            \glissando
            \hide NoteHead
            \override Accidental.stencil = ##f
            \override NoteColumn.glissando-skip = ##t
            \override NoteHead.no-ledgers = ##t
            d''4
            ef''4
            \revert Accidental.stencil
            \revert NoteColumn.glissando-skip
            \revert NoteHead.no-ledgers
            \undo \hide NoteHead
            f''4
        }
        """
    )
