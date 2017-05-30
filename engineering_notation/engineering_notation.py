from decimal import *


class EngNumber:
    """
    Used for easy manipulation of numbers which use engineering notation
    """

    suffix_lookup = {
        'p': 'e-12',
        'n': 'e-9',
        'u': 'e-6',
        'm': 'e-3',
        '': 'e0',
        'k': 'e3',
        'M': 'e6',
        'G': 'e9',
        'T': 'e12'
    }

    exponent_lookup_scaled = {
        '-36': 'p',
        '-33': 'n',
        '-30': 'u',
        '-27': 'm',
        '-24': '',
        '-21': 'k',
        '-18': 'M',
        '-15': 'G',
        '-12': 'T'
    }

    def __init__(self, value: (str, int, float), precision=2):
        """
        Initialize the class

        :param value: string, integer, or float representing the numeric value of the number
        :param precision: the precision past the decimal - default to 2
        """
        self.precision = precision

        if isinstance(value, str):
            suffix_keys = [key for key in self.suffix_lookup.keys() if key != '']

            for suffix in suffix_keys:
                if suffix in value:
                    value = value[:-1] + self.suffix_lookup[suffix]
                    break

            self.number = Decimal(value)

        elif isinstance(value, int) or isinstance(value, float):
            self.number = Decimal(str(value))

    def __repr__(self):
        """
        Returns the string representation
        :return: a string representing the engineering number
        """
        # since Decimal class only really converts number that are very small
        # into engineering notation, then we will simply make all number a
        # small number and take advantage of Decimal class
        num_str = self.number * Decimal('10e-25')
        num_str = num_str.to_eng_string().lower()

        base, exponent = num_str.split('e')

        base = str(round(Decimal(base), self.precision))
        if '.00' in base:
            base = base[:-3]

        return base + self.exponent_lookup_scaled[exponent]

    def __str__(self, eng=True, context=None):
        """
        Returns the string representation
        :return: a string representing the engineering number
        """
        return self.__repr__()

    def __add__(self, other):
        """
        Add two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number + other.number
        return EngNumber(str(num))

    def __radd__(self, other):
        """
        Add two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        Subtract two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number - other.number
        return EngNumber(str(num))

    def __rsub__(self, other):
        """
        Subtract two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = other.number - self.number
        return EngNumber(str(num))

    def __mul__(self, other):
        """
        Multiply two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number * other.number
        return EngNumber(str(num))

    def __rmul__(self, other):
        """
        Multiply two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Divide two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number / other.number
        return EngNumber(str(num))

    def __rtruediv__(self, other):
        """
        Divide two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = other.number / self.number
        return EngNumber(str(num))

    def __lt__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number < other.number

    def __gt__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number > other.number

    def __le__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number <= other.number

    def __ge__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number >= other.number

    def __eq__(self, other):
        """
        Compare two engineering numbers
        :param other: EngNum, float, or int
        :return: result
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number == other.number

