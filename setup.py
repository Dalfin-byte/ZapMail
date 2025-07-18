from setuptools import setup, find_packages
from pathlib import Path

<<<<<<< HEAD
# Read the contents of your README file
=======
>>>>>>> 12f6b95 (Addition to more services)
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
<<<<<<< HEAD
    name="pyemailer",
    version="1.0.0",
=======
    name="ZapMail",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Dalfin-Byte",
    author_email="gd.familie.18@gmail.com",
<<<<<<< HEAD
    description="A simple library to send emails via Gmail SMTP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dalfin-byte/pyemailer",
=======
    description="A simple, intuitive Gmail SMTP email library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dalfin-byte/ZapMail",
>>>>>>> 12f6b95 (Addition to more services)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
<<<<<<< HEAD
=======
    python_requires=">=3.7",
>>>>>>> 12f6b95 (Addition to more services)
)
