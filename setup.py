#   setup.py
#===========================================================
from setuptools import setup
#===========================================================

setup(
    name = 'ebe',
    version = '0.1.beta',
    author = 'itscomputers',
    author_email = 'its_computers@protonmail.com',
    description = 'A number theory package for Python'
    long_description = open('README.md', 'r').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/itscomputers/ebe-python',
    license = 'GNU General Public License v3.0',
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3',
        'Programming Languange :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic' :: 'Scientific/Engineering',
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
    ],
    packages = ['ebe'],
    install_requires = ['pytest', 'hypothesis'],
    python_requires = '>=3',
)

