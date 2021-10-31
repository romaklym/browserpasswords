import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="browserpasswords",
    version="0.0.4",
    author="Roman Klym",
    author_email="klymromanr@protonmail.com",
    description="Collects login information from Chrome, Mozilla & Brave",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/romaklym/browserpasswords",
    project_urls={
        "Bug Tracker": "https://github.com/romaklym/browserpasswords",
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Database",
    ],
    platforms=['Windows', 'MacOS'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)