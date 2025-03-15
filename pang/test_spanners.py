import abjad
from pang import spanners


def test_glissando_to_next_leaf():
    voice = abjad.Voice("c'4~ c'4~ c'4~ b'4")
    spanners.glissando_to_next_leaf(voice)
    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'4
            \glissando
            \hide NoteHead
            \override Accidental.stencil = ##f
            \override NoteColumn.glissando-skip = ##t
            \override NoteHead.no-ledgers = ##t
            c'4
            c'4
            ~
            \revert Accidental.stencil
            \revert NoteColumn.glissando-skip
            \revert NoteHead.no-ledgers
            \undo \hide NoteHead
            b'4
        }
        """
    )
