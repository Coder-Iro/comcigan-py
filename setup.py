from os import environ

import setuptools

version = environ['TRAVIS_TAG'].lstrip('v') if environ['TRAVIS'] == "true" else environ["VERSION_NUMBER"]
setuptools.setup(
    name="comcigan",
    version=version,
    license='MIT',
    author="Team IF",
    author_email="Coder-Iro@teamif.io",
    description="Unofficial Comcigan API python wrapper",
    long_description=open('README.md').read(),
    url="https://github.com/Team-IF/comcigan-py",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'beautifulsoup4'],
    python_requires='>=3',
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
