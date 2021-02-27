import numpy as np

import pang


def test_AtaxicCloud_simulate_queue_01():
    sequence = pang.AtaxicCloud()
    sequence.simulate_queue()
    np.testing.assert_almost_equal(
        sequence.servers[0].durations, [0.1269698, 3.4027337]
    )
