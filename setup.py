import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="instrument_logger",  # Replace with your own username
    version="0.0.1",
    author="Nate Costello",
    author_email="natecostello@gmail.com",
    description="A package that provides and interface for instruments and logs from those instruments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/natecostello/instrument_logger",
    project_urls={
        "Bug Tracker": "https://github.com/natecostello/instrument_logger/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=['instrument_logger'],
    python_requires=">=3.6",
)