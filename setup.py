"""
Setup script for hlquery Python client
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hlquery-python-client",
    version="1.0.0",
    author="Carlos F. Ferry",
    author_email="carlos.ferry@gmail.com",
    description="Python client library for hlquery search engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hlquery/hlquery",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Core client usage uses the Python standard library only.
    ],
    extras_require={
        "pdf": ["PyPDF2"],
    },
)
