from distutils.core import setup

if __name__ == "__main__":
    setup(
        author="Tsz Kiu Pang",
        author_email="osamupang@gmail.com",
        install_requires=[
            "numpy",
            "abjad",
            "abjad-ext-nauert",
        ],
        extras_require={
            "test": [
                "black>=20.8b1",
                "flake8>=3.8.2",
                "isort>=4.3.21",
                "mypy>=0.770",
                "pytest>=5.4.3",
                "pytest-cov>=2.6.0",
                "pytest-helpers-namespace",
            ]
        },
        name="pang",
        packages=["pang"],
        version="0.1",
        zip_safe=False,
    )
