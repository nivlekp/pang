#(ly:set-option 'relative-includes #t)
\include "abjad_contrib/abjad.ily"

\version "2.25.16"
\language "english"

#(set-default-paper-size "a4")
#(set-global-staff-size 16)

%{
function copied from MS via the lilypond mailing list at
https://www.mail-archive.com/lilypond-user@gnu.org/msg72640.html
%}
#(define shorten-tuplet-bracket-at-end-of-staff
   (lambda (grob)
     (let* ((right (ly:spanner-bound grob RIGHT))
            (bd (ly:item-break-dir right))
            (xshift (if (= bd -1) -0.5 0.0)))
       (coord-translate (ly:tuplet-bracket::calc-x-positions grob)
                        `(0 . ,xshift)))))

tszkiu-metronome-mark =
#(define-music-function
   (units-per-minute duration-exponent)
   (number? number?)
   (make-music
     'TempoChangeEvent
     'metronome-count
     units-per-minute
     'tempo-unit
     (ly:make-duration duration-exponent)))

#(define-markup-command
    (tszkiu-left-arrow layout props)
    ()
    (interpret-markup layout props
    #{
    \markup {
        \concat {
          \raise #1 \arrow-head #X #LEFT ##t
          \raise #1 \draw-line #'(2 . 0)
        }
    }
    #}
    )
)

#(define-markup-command
    (tszkiu-right-arrow layout props)
    ()
    (interpret-markup layout props
    #{
    \markup {
        \concat {
          \raise #1 \draw-line #'(2 . 0)
          \raise #1 \arrow-head #X #RIGHT ##t
        }
    }
    #}
    )
)

#(define-markup-command
    (tszkiu-metric-modulation layout props left-rhythm right-rhythm)
    (ly:music? ly:music?)
    (interpret-markup layout props
    #{
    \markup {
        \hspace #-10
        \line {
            \tszkiu-left-arrow
            \rhythm { #left-rhythm } = \rhythm { #right-rhythm }
            \tszkiu-right-arrow
        }
    }
    #}
    )
)

\header {
  composer = \markup {
    "Tsz Kiu Pang"
  }
  tagline = ##f
  title = "{{composition_title}}"
  instrument = "for piano"
}

\layout {
  indent = 0\cm
  ragged-last = ##t
  \accidentalStyle forget
  \context {
    \Score
    \override SpacingSpanner.uniform-stretching = ##t
    proportionalNotationDuration = #(ly:make-moment 1 24)
    \override StaffGrouper.staff-staff-spacing.padding = #8
    \override StaffGrouper.staff-staff-spacing.basic-distance = #8
  }
  \context {
    \Staff
    \override Beam.damping = #+inf.0
    \override Flag.stencil = #modern-straight-flag
    \override TupletBracket.max-slope-factor = #0
    \override TupletBracket.span-all-note-heads = ##t
    \override TupletBracket.padding = 1.7
    \override TupletBracket.X-positions = #shorten-tuplet-bracket-at-end-of-staff
    tupletFullLength = ##t
  }
  \context {
    \PianoStaff
    \consists "Span_stem_engraver"
    \numericTimeSignature
  }
  \context {
    \Dynamics
    \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.basic-distance = #10
  }
  \context {
    \StandaloneRhythmVoice
    \override Rest.transparent = ##t
    \override TupletBracket.bracket-visibility = ##t
  }
}

\paper {
  % system-sytem-spacing.basic-distance = #8
  % score-system-spacing =
  %   #'((basic-distance . 100)
  %      (minimum-distance . 100)
  %      (padding . 100)
  %      (stretchability . 100))
  system-system-spacing.padding = #8
  oddHeaderMarkup = \markup ""
  evenHeaderMarkup = \markup ""

  oddFooterMarkup = \markup \fill-line {
    \concat {
      "{{composition_title}}"
      "  "
      \char ##x2014
      "  "
      \fromproperty #'page:page-number-string
      "  "
      \char ##x2014
      "  "
      "Pang"
    }
  }

  evenFooterMarkup = \markup \fill-line {
    \concat {
      "{{composition_title}}"
      "  "
      \char ##x2014
      "  "
      \fromproperty #'page:page-number-string
      "  "
      \char ##x2014
      "  "
      "Pang"
    }
  }
}

end-note = {
    \once \override Score.RehearsalMark.direction = #down
    \once \override Score.RehearsalMark.padding = 4
    \mark \markup {
        \fontsize #-2
        \column {
          \line {"Naarm"}
          \hspace #0
          \line {"(November 2024)."}
      }
    }
}
