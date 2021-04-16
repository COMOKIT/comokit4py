# File created following this official tutorial
# https://packaging.python.org/tutorials/packaging-projects/

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="comokit4py",  # Replace with your own username
    version="0.1.4",    # Format : https://www.python.org/dev/peps/pep-0440/
    author="COMOKIT",
    author_email="contact@comokit.org",
    description="Python3 library to simplify the exploration of COMOKIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/COMOKIT/comokit4py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "Environment :: Plugins",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Science/Research",
        "Programming Language :: Other",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
)
