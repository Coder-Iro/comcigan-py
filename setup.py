import setuptools

setuptools.setup(
    name="comcigan",
    version="0.1",
    license='MIT',
    author="Team IF",
    author_email="Coder-Iro@teamif.io",
    description="Unofficial Comcigan API python wrapper",
    long_description=open('README.md').read(),
    url="https://github.com/Team-IF/comcigan-py",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)