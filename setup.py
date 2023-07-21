import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imprel",
    version="0.0.1",
    author="Mariia Zakharenko",
    author_email="maria.zakharova@ntnu.no",
    description="Package provides functionality for Classic and Imprecise Structural Reliability Analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marizakntnu/imprel",
    project_urls={
        "Bug Tracker": "https://github.com/marizakntnu/imprel/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    package_dir={'':"src"},
    packages=find_packages("src"),
    python_requires=">=3.6",
    entry_points={
                        'console_scripts': [
                                'www=imprel.utils:sayHello',
                        ]
                }
)