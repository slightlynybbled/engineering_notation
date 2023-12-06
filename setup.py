from setuptools import setup

import os

__version__ = None

# ---------------------------------
# imports the version from the package (with a pycharm patch)
here = os.path.dirname(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'engineering_notation/version.py'), 'r') as f:
        fdata = f.read()
except FileNotFoundError:
    with open(os.path.join(here, 'engineering_notation/engineering_notation/version.py'), 'r') as f:
        fdata = f.read()

exec(fdata)

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
    long_description_content_type='text/markdown',
    author='Jason R. Jones',
    author_email='slightlynybbled@gmail.com',
    url='https://github.com/slightlynybbled/engineering_notation',
    packages=["engineering_notation"],
    package_data={"engineering_notation": ["py.typed"]},
    install_requires=requirements,
    setup_requires=['flake8', 'pytest'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English'
    ],
    keywords='engineering notation decimal'
)
