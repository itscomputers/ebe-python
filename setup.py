
#   setup.py

from setuptools import setup

setup(
    name = 'NumTh',
    version = '0.1.0.dev0',
    author = 'itscomputers',
    author_email = 'its_computers@protonmail.com',
    description = 'A number theory package for Python'
    long_description = open('README.md', 'r').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/itscomputers/numth',
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
    packages = ['numth'],
    install_requires = [
        'concurrent.futures', 
        'pebble',
    ],
    python_requires = '>=3',
)
