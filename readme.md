[![Unit Tests](https://github.com/slightlynybbled/engineering_notation/actions/workflows/unittest.yml/badge.svg)](https://github.com/slightlynybbled/engineering_notation/actions/workflows/unittest.yml)

# Purpose

To easily work with human-readable engineering notation.  I wrote this as a quick tool for my own use.
I found that I was writing the same functionality into multiple packages and would like a quick pip-installable
package to take care of this manipulation for me.  The package should be easily extended for other use cases.
The package is unit-less, so only operates on numeric values.  Unit detection may be added in future versions.

More information may be found at [for(embed)](http://forembed.com/engineering-notation-in-python.html).

# Installation

Install using pip: `pip install engineering_notation`.

# Usage

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

All of the above operations are also possible on the `EngUnit()` class as well.  The only difference is
that units must match for addition/subtraction/comparison operations.  Although multiplication and division
operations will work numerically, they may not always be strictly correct.  This is because EngUnit is not
intended to replace a computer algebra system!

```
>>> EngUnit('2s') / EngUnit('4rotations')
0.5s/rotations
```

Additionally, since there are 'reserved' letters for sizing the number, you must be careful with your units!

```
>>> EngUnit('2mm')
2mm        # <<< this value equivalent to "0.002m"
>>> EngUnit('2meter')
2meter     # <<< this value is equivalent to "0.002eter", the "m" was used to scale the unit!
>>> EngUnit('2', unit='meter')   # <<< this will work better
```

# Contributions

Contributions are welcome.  Feel free to make feature requests in the issues.

## Test Installation

If you are developing, you probably want to perform a local editable installation:

```bash
uv run pip install -e .
```

## Testing

```bash
uv run python -m pytest
```
