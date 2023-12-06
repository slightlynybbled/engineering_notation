from decimal import Decimal
from string import digits
import sys

from typing import Optional

try:
    import numpy
except ImportError:
    pass

_suffix_lookup = {
    'y': 'e-24',
    'z': 'e-21',
    'a': 'e-18',
    'f': 'e-15',
    'p': 'e-12',
    'n': 'e-9',
    'u': 'e-6',
    'm': 'e-3',
    '': 'e0',
    'k': 'e3',
    'M': 'e6',
    'G': 'e9',
    'T': 'e12',
    'P': 'e15',
    'E': 'e18',
    'Z': 'e21',
}

_exponent_lookup_scaled = {
    '-54': 'y',
    '-51': 'z',
    '-48': 'a',
    '-45': 'f',
    '-42': 'p',
    '-39': 'n',
    '-36': 'u',
    '-33': 'm',
    '-30': '',
    '-27': 'k',
    '-24': 'M',
    '-21': 'G',
    '-18': 'T',
    '-15': 'P',
    '-12': 'E',
    '-9': 'Z',
}


class EngUnit:
    """
    Represents an engineering number, complete with units
    """
    def __init__(self, value,
                 precision=2, significant=0, unit: Optional[str] = None, separator=""):
        """
        Initialize engineering with units
        :param value: the desired value in the form of a string, int, or float
        :param precision: the number of decimal places
        :param significant: the number of significant digits
        if given, significant takes precendence over precision
        """
        suffix_keys = [key for key in _suffix_lookup.keys() if key != '']
        self.unit = unit

        if isinstance(value, str):
            # parse the string into unit and engineering number
            new_value = ''
            v_index = 0
            for c in value:
                if (c in digits) or (c in ['.', '-']) or (c in suffix_keys):
                    new_value += c
                    v_index += 1
                else:
                    break

            if self.unit is None and len(value) >= v_index:
                self.unit = value[v_index:]

            self.eng_num = EngNumber(new_value, precision,
                                     significant, separator)

        else:
            self.eng_num = EngNumber(value, precision, significant, separator)

    def __repr__(self):
        """
        Returns the object representation
        :return: a string representing the engineering number
        """
        unit = self.unit if self.unit else ''
        return str(self.eng_num) + unit

    def __str__(self):
        """
        Returns the string representation
        :return: a string representing the engineering number
        """
        return self.__repr__()

    def __int__(self):
        """
        Implements the 'int()' method
        :return:
        """
        return int(self.eng_num)

    def __float__(self):
        """
        Implements the 'float()' method
        :return:
        """
        return float(self.eng_num)

    def __add__(self, other):
        """
        Add two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        if self.unit != other.unit:
            raise AttributeError('units do not match')

        return EngUnit(str(self.eng_num + other.eng_num) + self.unit)

    def __radd__(self, other):
        """
        Add two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        Subtract two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        if self.unit != other.unit:
            raise AttributeError('units do not match')

        return EngUnit(str(self.eng_num - other.eng_num) + self.unit)

    def __rsub__(self, other):
        """
        Subtract two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        if self.unit != other.unit:
            raise AttributeError('units do not match')

        return EngUnit(str(other.eng_num - self.eng_num) + self.unit)

    def __mul__(self, other):
        """
        Multiply two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        return EngUnit(str(self.eng_num * other.eng_num)
                       + self.unit + other.unit)

    def __rmul__(self, other):
        """
        Multiply two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Divide two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        new_unit = ''
        if self.unit:
            new_unit += self.unit
        if other.unit:
            new_unit += '/' + other.unit

        return EngUnit(str(self.eng_num / other.eng_num) + new_unit)

    def __rtruediv__(self, other):
        """
        Divide two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        return EngUnit(str(other.eng_num / self.eng_num)
                       + (other.unit + '/' + self.unit))

    def __lt__(self, other):
        """
        Compare two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        if self.unit != other.unit:
            raise AttributeError('units do not match')

        return self.eng_num < other.eng_num

    def __gt__(self, other):
        """
        Compare two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        if self.unit != other.unit:
            raise AttributeError('units do not match')

        return self.eng_num > other.eng_num

    def __le__(self, other):
        """
        Compare two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        if self.unit != other.unit:
            raise AttributeError('units do not match')

        return self.eng_num <= other.eng_num

    def __ge__(self, other):
        """
        Compare two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        if self.unit != other.unit:
            raise AttributeError('units do not match')

        return self.eng_num >= other.eng_num

    def __eq__(self, other):
        """
        Compare two engineering numbers, with units
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, (EngNumber, EngUnit, str, int, float)):
            return NotImplemented
        if not isinstance(other, EngNumber):
            other = EngUnit(str(other))

        if self.unit != other.unit:
            raise AttributeError('units do not match')

        return self.eng_num == other.eng_num


class EngNumber:
    """
    Used for easy manipulation of numbers which use engineering notation
    """

    def __init__(self, value,
                 precision=2, significant=0, separator=""):
        """
        Initialize the class

        :param value: string, integer, or float representing
        the numeric value of the number
        :param precision: the precision past the decimal - default to 2
        :param significant: the number of significant digits
        if given, significant takes precendence over precision
        """
        self.precision = precision
        self.significant = significant
        self.separator = separator

        if isinstance(value, str):
            suffix_keys = [key for key in _suffix_lookup.keys() if key != '']

            for suffix in suffix_keys:
                if suffix == value[-1]:
                    value = value[:-1] + _suffix_lookup[suffix]
                    break

            self.number = Decimal(value)

        elif (isinstance(value, int)
              or isinstance(value, float)
              or isinstance(value, EngNumber)):
            self.number = Decimal(str(value))
        else:
            # finally, check for numpy import
            if 'numpy' in sys.modules and isinstance(value, numpy.integer):
                self.number = Decimal(str(value))

    def to_pn(self, sub_letter=None):
        """
        Returns the part number equivalent.  For instance,
        a '1k' would still be '1k', but a
        '1.2k' would, instead, be a '1k2'
        :return:
        """
        string = str(self)
        if '.' not in string:
            return string

        # take care of the case of when there is no scaling unit
        if not string[-1].isalpha():
            if sub_letter is not None:
                return string.replace('.', sub_letter)

            return string

        letter = string[-1]
        return string.replace('.', letter)[:-1].strip(self.separator)

    def __repr__(self):
        """
        Returns the string representation
        :return: a string representing the engineering number
        """
        # since Decimal class only really converts number that are very small
        # into engineering notation, then we will simply make all number a
        # small number and take advantage of Decimal class
        num_str = self.number * Decimal('10e-31')
        num_str = num_str.to_eng_string().lower()

        base, exponent = num_str.split('e')

        if self.significant > 0:
            if abs(Decimal(base)) >= 100.0:
                base = str(round(Decimal(base), self.significant - 3))
            elif abs(Decimal(base)) >= 10.0:
                base = str(round(Decimal(base), self.significant - 2))
            else:
                base = str(round(Decimal(base), self.significant - 1))
        else:
            base = str(round(Decimal(base), self.precision))

        if 'e' in base.lower():
            base = str(int(Decimal(base)))

        # remove trailing decimals:
        # print(base)
        # https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
        # https://stackoverflow.com/questions/11227620/drop-trailing-zeros-from-decimal
        # base = '%s' % float("%#.2G"%Decimal(base))
        # print(base)
        # remove trailing decimal
        if '.' in base:
            base = base.rstrip('.')

        # remove trailing .00 in precision 2
        if self.precision == 2 and self.significant == 0:
            if '.00' in base:
                base = base[:-3]

        return base + self.separator + _exponent_lookup_scaled[exponent]

    def __str__(self, eng=True, context=None):
        """
        Returns the string representation
        :return: a string representing the engineering number
        """
        return self.__repr__()

    def __int__(self):
        """
        Implements the 'int()' method
        :return:
        """
        return int(self.number)

    def __float__(self):
        """
        Implements the 'float()' method
        :return:
        """
        return float(self.number)

    def __add__(self, other):
        """
        Add two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number + other.number
        return EngNumber(str(num))

    def __radd__(self, other):
        """
        Add two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        Subtract two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number - other.number
        return EngNumber(str(num))

    def __rsub__(self, other):
        """
        Subtract two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = other.number - self.number
        return EngNumber(str(num))

    def __mul__(self, other):
        """
        Multiply two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number * other.number
        return EngNumber(str(num))

    def __rmul__(self, other):
        """
        Multiply two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Divide two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number / other.number
        return EngNumber(str(num))

    def __rtruediv__(self, other):
        """
        Divide two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = other.number / self.number
        return EngNumber(str(num))

    def __lt__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number < other.number

    def __gt__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number > other.number

    def __le__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number <= other.number

    def __ge__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number >= other.number

    def __eq__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, str, float, or int
        :return: result
        """
        if not isinstance(other, (EngNumber, str, int, float)):
            return NotImplemented
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number == other.number
