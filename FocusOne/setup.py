# setup.py
from setuptools import find_packages, setup

setup(
    name="focusone",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "focusone=focusone.cli:main",
        ],
    },
)
