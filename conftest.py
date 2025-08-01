import nauert
import pytest

import abjad
import pang


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["abjad"] = abjad
    doctest_namespace["nauert"] = nauert
    doctest_namespace["pang"] = pang
