class SegmentMaker:
    r"""
    Segment-maker.

    ..  container:: example

        >>> template = pang.make_single_staff_score_template()
        >>> maker = pang.SegmentMaker(
        ...     score_template=template,
        ... )
    """

    def __init__(
        self,
        score_template=None,
    ):
        # self._lilypond_file = None
        self._score_template = score_template

    def __call__(self, scope, commands):
        pass
