from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pdfutils",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pdfutils = pdfutils.main:main",
        ]
    },
    author="Teshan Liyanage",
    author_email="teshanuka@gmail.com",
    description="A CLI tool for simple PDF operations",
    url="https://github.com/teshanshanuka/pdfutils",
    license="MIT",
)
