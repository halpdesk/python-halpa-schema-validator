import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="halpa-schema-validator",
    version="0.0.1",
    author="Daniel Leppänen",
    author_email="daniel.leppanen@gmail.com",
    description="A utility to validate JSON schemas with jsonschema with simplejson",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/halpdesk/example-pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    build_requires=['simplejson>=3.17.0', 'jsonschema>=3.2.0']
)