"""Setup script for html2md package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="html2md",
    version="0.1.0",
    author="Ashitka-Laputa-IV",
    author_email="ashitka.laputa.iv@outlook.com",
    description="A Python library for converting HTML to Markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ashitka-Laputa-IV/html2md",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
)
