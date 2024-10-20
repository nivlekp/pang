import abjad
from pang import metricmodulation


def test_metric_modulation_markup():
    assert metricmodulation.metric_modulation_markup(
        abjad.MetronomeMark(abjad.Duration(1, 4), 60),
        abjad.MetronomeMark(abjad.Duration(1, 4), 40),
    ).string == abjad.string.normalize(
        r"""
        \markup \tszkiu-metric-modulation { 8 } { \tuple 3/2 { 8 r8 r8 } }
        """
    )
