#!/usr/bin/python
# -*- coding: UTF-8 -*-
from setuptools import find_packages, setup#

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kinpin_okx_v5",
    version="0.0.2",
    author="jane-cloud,bobby4k",
    author_email="bobby4kit@outlook.com",
    description="Python SDK for OKX OpenAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://okx.com/docs-v5/",
    packages=find_packages(exclude = ['test',]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "httpx[h2]",
    ],
)