#(set-default-paper-size "a4landscape")
#(set-global-staff-size 16)

%{
The flat-brackets code is adapted from David Nalesnik on the LilyPond mailing
list:
http://lilypond.1069038.n5.nabble.com/Horizontal-TupletBrackets-td158413.html#a158452
%}
#(define flat-brackets
   (lambda (grob)
     (let* ((pos (ly:tuplet-bracket::calc-positions grob))
             (dir (ly:grob-property grob 'direction))
             (y (if (= UP dir)
                    (max (car pos) (cdr pos))
                    (min (car pos) (cdr pos)))))
       (cons y y))))

\layout {
  indent = 0\cm
  ragged-last = ##t
  \accidentalStyle forget
  \context {
    \Score
    %\override SpacingSpanner.strict-note-spacing = ##t
    %\override SpacingSpanner.strict-grace-spacing = ##t
    \override SpacingSpanner.uniform-stretching = ##t
    proportionalNotationDuration = #(ly:make-moment 1 24)
    \override StaffGrouper.staff-staff-spacing.padding = #8
    \override StaffGrouper.staff-staff-spacing.basic-distance = #8
  }
  \context {
    \Staff
    %\override TupletNumber.text = #tuplet-number::calc-fraction-text
    \override Beam.damping = #+inf.0
    \override Beam.details.damping-direction-penalty = #0
    \override Beam.details.round-to-zero-slope = #0
    \override Flag.stencil = #modern-straight-flag
    \override Stem.length = #10
    \override TupletBracket.positions = #flat-brackets
    tupletFullLength = ##t
  }
  \context {
    \Dynamics
    \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.basic-distance = #10
    \override DynamicText #'extra-offset = #'(1 . 0)
  }
}

\paper {
  system-system-spacing.padding = #8
  oddHeaderMarkup = \markup ""
  evenHeaderMarkup = \markup ""

  oddFooterMarkup = \markup \fill-line {
    \concat {
      "--"
      \fromproperty #'page:page-number-string
      "--"
    }
  }

  evenFooterMarkup = \markup \fill-line {
    \concat {
      "--"
      \fromproperty #'page:page-number-string
      "--"
    }
  }
}
