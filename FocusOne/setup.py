# setup.py
from setuptools import find_packages, setup

setup(
    name="FocusOne",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "focusone=FocusOne.cli:main",
        ],
    },
)
