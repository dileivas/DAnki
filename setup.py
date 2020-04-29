import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="DAnki",
    version="1.0.0",
    description="Automate deck creation for Anki to learn german",
    long_description=README,
    url="https://github.com/dileivas/DAnki",
    author="Diego Leivas",
    author_email="dileivas@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["DAnki"],
    include_package_data=True,
    install_requires=["pandas", "googletrans", "pyenchant", "requests", "bs4", "treetaggerwrapper", "unicodedata", "gtts", "genanki",],
    keywords=['anki', 'flashcards', 'memorization', 'german', 'deutsch',]
    )
