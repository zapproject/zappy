from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="testGappy-Gap",
    version="0.0.10",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/testGappy",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/testGappy/issues",
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires = [
        "web3 == 5.26.0",
        "py-eth-sig-utils == 0.4.0"
    ],
    python_requires=">=3.6",
    license="MIT"
)