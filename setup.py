from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "2.3.5"
DESCRIPTION = "A python module for DeSo"
LONG_DESCRIPTION = "DesoPy is a python module that enables devs to interact with DeSo Blockchain using node.deso.org node by default. Includes all functions to read from or write to DeSo Blockchain"
# Setting up
setup(
    name="deso",
    version=VERSION,
    author="ItsAditya (https://itsaditya.xyz)",
    author_email="<chaudharyaditya0005@gmail.com>",
    description="A python module for deso",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["PyJWT", "ecdsa", "base58", "hdwallet"],
    keywords=[
        "deso",
        "python",
        "bitclout",
        "social media",
        "crypto",
        "blockchain",
        "decentralisation",
        "decentralized social media"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
