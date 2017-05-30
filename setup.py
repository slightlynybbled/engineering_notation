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
    readme = convert('readme.md', 'rst')
except ImportError:
    readme = ''


# ---------------------------------
# project requirements
requirements = []

# ---------------------------------
# project setup
setup(
    name='engineering_notation',
    version=__version__,
    description='Easy engineering notation',
    long_description=readme,
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
