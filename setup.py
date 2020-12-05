from os import environ
from setuptools import setup, find_packages

version = environ['TRAVIS_TAG'].lstrip('v') if environ['TRAVIS'] == 'true' else environ['VERSION_NUMBER']

setup(
    name = 'comcigan',
    version = version,
    license = 'MIT',
    author = 'Team IF',
    author_email = 'Coder-Iro@teamif.io',
    description = 'Unofficial Comcigan API python wrapper',
    long_description = open('README.md').read(),
    url = 'https://github.com/Team-IF/comcigan-py',
    packages = find_packages(),
    install_requires = ['requests', 'beautifulsoup4', 'aiohttp'],
    python_requires = '>=3.7',
    classifiers = [
        # 패키지에 대한 태그
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
)
