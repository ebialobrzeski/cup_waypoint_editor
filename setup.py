"""Setup configuration for Soaring CUP File Editor."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="soaring-cup-editor",
    version="1.0.0",
    author="Soaring CUP Editor Team",
    description="A waypoint editor for soaring and flight planning software",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebialobrzeski/cup_waypoint_editor",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    entry_points={
        "console_scripts": [
            "soaring-cup-editor=soaring_cup_file_editor.__main__:main",
        ],
    },
)
