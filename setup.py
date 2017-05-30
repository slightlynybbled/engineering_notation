from setuptools import setup, find_packages
import os

# ---------------------------------
# imports the version from the package
here = os.path.dirname(os.path.dirname(__file__))
exec(open(os.path.join(here, 'engineering_notation/version.py')).read())

# ---------------------------------
# converts the readme.md to readme.rst
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

# ---------------------------------
# project requirements
requirements = []

# ---------------------------------
# project setup
setup(
    name='engineering_notation',
    version=__version__,
    description='Easy engineering notation',
    long_description=read_md('readme.md'),
    author='Jason R. Jones',
    author_email='slightlynybbled@gmail.com',
    url='https://github.com/slightlynybbled/engineering_notation',
    packages=find_packages(),
    install_requires=requirements,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English'
    ],
    keywords='engineering notation decimal'
)
