import pytest

import pang


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["pang"] = pang
