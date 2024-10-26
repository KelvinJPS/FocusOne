# setup.py
from setuptools import find_packages, setup

setup(
    name="FocusOne",
    version="0.1",
    packages=find_packages(include=['FocusOne', 'FocusOne.*']),
    python_requires=">=3.6",
    install_requires=[
        # Add your dependencies here
    ],
    entry_points={
        "console_scripts": [
            "focusone=FocusOne.cli:main",
        ],
    },
    author="Your Name",
    description="A focus timer application",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/FocusOne",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
