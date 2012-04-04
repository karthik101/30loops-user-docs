import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read().strip()

VERSION = '0.1'

setup(
    name = "30loops-user-docs",
    version = VERSION,
    author = "30loops",
    author_email = "mail@30loops.net",
    description = "Generate sphinx documentation for the 30loops platform",
    long_description = read('README.rst'),
    license = 'GNU LGPL',
    url = "http://github.com/30loops/30loops-user-docs.git",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        ("License :: OSI Approved :: GNU Library or Lesser General "
        "Public License (LGPL)"),
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        ],

    zip_safe = False,
    packages=[
        '30loops-user-docs',
    ],
    include_package_data = True
)
