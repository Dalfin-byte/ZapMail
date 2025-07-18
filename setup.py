from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ZapMail",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[],
    author="Dalfin-Byte",
    author_email="gd.familie.18@gmail.com",
    description="A simple, intuitive Gmail SMTP email library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dalfin-byte/ZapMail",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
