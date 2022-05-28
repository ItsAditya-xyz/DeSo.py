from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '2.0.7'
DESCRIPTION = 'A python module for DeSo'
LONG_DESCRIPTION = 'A package that allows to fetch various information from the DeSo blockchain using the bitclout APIs (by default). DeSo is a decentralised social media network'
# Setting up
setup(
    name="deso",
    version=VERSION,
    author="ItsAditya (https://bitclout.com/u/ItsAditya)",
    author_email="<chaudharyaditya0005@gmail.com>",
    description="A python module for deso",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["PyJWT", "ecdsa", "arweave-python-client", "base58"],
    keywords=['deso', 'python', 'bitclout', 'social media',
              'crypto', 'blockchain', 'decentralisation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
