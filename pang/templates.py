import abjad


def make_single_staff_score_template(
    voice_names=["Voice"], staff_name="Staff", score_name="Score", simultaneous=True
):
    r"""
    Make single-staff score template.

    ..  container:: example

        >>> score = pang.make_single_staff_score_template()
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                <<
                    \context Voice = "Voice"
                    {
                    }
                >>
            >>

    ..  container:: example

        >>> score = pang.make_single_staff_score_template(
        ...     voice_names=["Voice_1", "Voice_2"],
        ... )
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                <<
                    \context Voice = "Voice_1"
                    {
                    }
                    \context Voice = "Voice_2"
                    {
                    }
                >>
            >>
    """
    voices = [abjad.Voice(name=voice_name) for voice_name in voice_names]
    staff = abjad.Staff(voices, name=staff_name, simultaneous=simultaneous)
    score = abjad.Score([staff], name=score_name)
    return score
