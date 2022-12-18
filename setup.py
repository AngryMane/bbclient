from setuptools import setup, find_packages
from os import path


def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()


setup(
    name="bbclient",
    version="0.6.1",
    description="bbclient provides utility commands for bitbake.",
    long_description_content_type="text/markdown",
    long_description=read("README.md"),
    keywords=["yocto", "bitbake"],
    url="https://github.com/AngryMane/bbclient",
    author="AngryMane",
    author_email="regulationdango@gmail.com",
    license="MIT",
    python_requires=">=3.7",
    install_requires=["bbclient"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Plugins",
        "Topic :: Software Development :: Build Tools",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
    entry_points={
        "console_scripts": [
            "bbclient=bbclient.console:main",
        ],
    },
    packages=find_packages(),
)
