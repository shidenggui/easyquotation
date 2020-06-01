# coding:utf8
from os import path

from setuptools import setup

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="easyquotation",
    version="0.7.4",
    description="A utility for Fetch China Stock Info",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="shidenggui",
    author_email="longlyshidenggui@gmail.com",
    license="BSD",
    url="https://github.com/shidenggui/easyquotation",
    keywords="China stock trade",
    install_requires=["requests", "six", "easyutils"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: BSD License",
    ],
    packages=["easyquotation"],
    package_data={"": ["*.conf"]},
)
