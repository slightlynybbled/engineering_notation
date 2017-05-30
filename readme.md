![Travis CI Build Status](https://travis-ci.org/slightlynybbled/engineering_notation.svg?branch=master)

# Purpose

To easily work with human-readable engineering notation.  I wrote this as a quick tool for my own use.
I found that I was writing the same functionality into multiple packages and would like a quick pip-installable
package to take care of this manipulation for me.  The package should be easily extended for other use cases.
The package is unit-less, so only operates on numeric values.  Unit detection may be added in future versions.

# Installation

Install using pip: `pip install engineering_notation`.

# Status

This project currently has 100% test coverage.  Have a look in `test/test.py` for examples of how to use
this library.

# Use 

There are multiple ways of initializing a number to a particular value, but a string is the preferred method:

```
>>> from engineering_notation import EngNumber
>>> EngNumber('10k')
10k
>>> EngNumber('10000')
10k
>>> EngNumber(10000)
10k
>>> EngNumber(10000.0)
10k
>>> EngNumber(1e4)
10k
```

Where decimals are involved, we use a default precision of 2 digits:

```
>>> EngNumber('4.99k')
4.99k
>>> EngNumber('4.9k')
4.90k
```

This behavior can truncate your results in some cases, and cause your number to round.  To specify more or less
digits, simply specify the precision in the declaration:

```
>>> EngNumber('4.999k')
5k
>>> EngNumber('4.999k', precision=3)
4.999k
```

Most operations that you would perform on numeric values are valid, although all operations are not implemented:

```
>>> EngNumber('2.2k') * 2
4.40k
>>> 2 * EngNumber('2.2k')
4.40k
>>> EngNumber(1.2) > EngNumber('3.3k') 
False
>>> EngNumber(1.2) <= EngNumber('3.3k')
True
>>> EngNumber('3.3k') == EngNumber(3300)
True
```

# Contributions

Contributions are welcome.  Feel free to make feature requests in the issues.
