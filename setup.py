import sys

from setuptools import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 10)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================

This version of the Pang API requires Python {}.{}, but you're trying to
install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install pang

This will install the latest version of the Pang API which works on your
version of Python.
        """.format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

if __name__ == "__main__":
    setup(
        author="Tsz Kiu Pang",
        author_email="osamupang@gmail.com",
        install_requires=[
            "abjad",
            "abjad-ext-nauert",
            "numpy",
        ],
        name="pang",
        packages=["pang"],
        version="0.1",
        zip_safe=False,
    )
