from setuptools import setup, find_packages

with open("README.d", "r") as fh:
    long_description = fh.read()

setup(
    name = "kumhocompiler",
    version = "0.0.1",
    author = "Jasmine Webb",
    author_email = "jmwebb.94@gmail.com",
    description = "A data compiler for Kumho Eng, Inc.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jasmwebb/kumho-compiler",
    packages = find_packages(exclude = [
        "Data",
        "venv"
        ]),
    install_requires = ["XlsxWriter"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ])
