"""Setup for the """
from setuptools import setup

setup(
    name="SentralTimetable",
    version="0.1",
    description="A library to get your sentral timetable.",
    long_description_content_type="text/markdown",
    author="SuperHarmony910 and J-J-B-J",
    url="https://github.com/J-J-B-J/get-sentral-timetable",
    keywords="Sentral school timetable python scraper",
    python_requires=">=3.9",
    install_requires=[
        'bs4~=0.0.1',
        'beautifulsoup4~=4.10.0',
        'selenium~=4.4.2'
    ],
    package_dir={'': '.'},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Environment :: Console",
        "Environment :: Web Environment"
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows"
        "Operating System :: Unix"
        "Topic :: Education",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    platforms=["Windows", "MacOS", "Unix"],
    packages=["SentralTimetable"],
)
