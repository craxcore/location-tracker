#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="craxcore-location-tracker",
    version="1.0.0",
    description="A secure Python-based CLI tool for tracking Bangladeshi mobile numbers",
    author="CraxCore Team",
    author_email="contact@craxcore.com",
    url="https://github.com/craxcore/location-tracker",
    packages=find_packages(),
    install_requires=[
        "requests>=2.27.1",
        "geopy>=2.2.0",
        "rich>=12.0.0",
        "termcolor>=2.0.0",
        "configparser>=5.2.0",
        "cryptography>=37.0.0",
        "python-dotenv>=0.20.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Education :: Testing",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "craxtracker=launch:main",
        ],
    },
)
