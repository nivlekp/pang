import abjad


def _get_lilypond_includes():
    return ["../../stylesheets/stylesheet.ily"]


def make_lilypond_file(score):
    includes = _get_lilypond_includes()
    items = ["#(ly:set-option 'relative-includes #t)"]
    items += [rf'\include "{include}"' for include in includes]
    items += [score]
    lilypond_file = abjad.LilyPondFile(items=items)
    return lilypond_file


def persist(lilypond_file, lilypond_file_path):
    with open(lilypond_file_path, "w") as fp:
        string = abjad.lilypond(lilypond_file)
        fp.write(string)


def section(score, scope, command):
    target = score[scope.voice_name]
    command(target)
