"""Setup for the """
from setuptools import setup

setup(
    name="SentralTimetable",
    version="2022.0.7",
    description="A tool to get your timetable from Sentral.",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    author="SuperHarmony910 and J-J-B-J",
    url="https://github.com/J-J-B-J/get-sentral",
    keywords="Sentral school timetable python scraper",
    python_requires=">=3.9",
    install_requires=[
        'bs4~=0.0.1',
        'beautifulsoup4~=4.10.0',
        'selenium~=4.4.2',
        'TextBarcodeGenerator~=2022.0.2',
        'pyinstaller~=5.6.2',
        'webdriver-manager~=3.8.3',
        'python-dotenv~=0.20.0',
        'setuptools~=61.3.0',
        'Pillow~=9.0.1',
        'pyperclip~=1.8.2',
    ],
    package_dir={'': '.'},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Topic :: Education",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    platforms=["Windows", "MacOS", "Unix"],
    packages=["SentralTimetable"],
)
