import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="selenium_wrapper",
    version=1.0,
    author="Philip Hausner",
    author_email="hausner@informatik.uni-heidelberg.de",
    description="Wrapper for Selenium WebDriver",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ;; OSI Approved :: GNU GPL",
        "Operating System :: Debian",
    ],
    python_requires='>=3.6',
)
