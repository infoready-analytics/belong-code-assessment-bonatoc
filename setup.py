#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup


def parse_requirements():
    with open(Path(__file__).parent.joinpath("requirements.txt"), "r") as f:
        return f.read().splitlines()


setup(
    name="belong-code-assessment",
    version="1.0.0",
    author="Christian Bonato",
    author_email="christian.bonato@arq.group",
    description="Response to the Data Engineer coding assessment provided by Belong",
    packages=find_packages(),
    include_package_data=True,
    install_requires=parse_requirements(),
    entry_points={
        "console_scripts": [
            "belong-main=belong_code_assessment.main:main",
        ],
    },
)
