from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

version = {}
with open("hexastore/version.py") as f:
    exec(f.read(), version)

setup(
    name="hexastore",
    version=version["__version__"],
    description="another hexastore implementation",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/e-k-m/hexastore",
    author="Eric Matti",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="hexastore",
    packages=find_packages(include=["hexastore", "hexastore.*"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[],
)
