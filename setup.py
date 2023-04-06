from os import environ

from setuptools import find_packages, setup

version = (
    environ["GITHUB_REF_NAME"].lstrip("v")
    if environ.get("GITHUB_ACTIONS")
    else environ["VERSION_NUMBER"]
)

setup(
    name="comcigan",
    version=version,
    author="Coder-Iro",
    author_email="doohee006@gmail.com",
    description="Unofficial Comcigan API python wrapper",
    long_description=open("README.md", "r", encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Coder-Iro/comcigan-py",
    packages=find_packages(exclude=["test"]),
    install_requires=["requests", "beautifulsoup4", "aiohttp", "lxml"],
    python_requires=">=3.7",
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
)
