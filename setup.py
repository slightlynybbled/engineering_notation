from setuptools import setup, find_packages
import os

__version__ = None

# ---------------------------------
# imports the version from the package
here = os.path.dirname(os.path.dirname(__file__))
exec(open(os.path.join(here, 'engineering_notation/version.py')).read())

try:
    with open('readme.md', 'r') as f:
        readme = f.read()
except FileNotFoundError:
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
    setup_requires=['flake8', 'pytest'],
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
