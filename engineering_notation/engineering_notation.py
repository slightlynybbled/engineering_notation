from decimal import *


class EngNumber:
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
        return self.__repr__()

    def __add__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number + other.number
        return EngNumber(str(num))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number - other.number
        return EngNumber(str(num))

    def __mul__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number * other.number
        return EngNumber(str(num))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number / other.number
        return EngNumber(str(num))

    def __rtruediv__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = other.number / self.number
        return EngNumber(str(num))

    def __lt__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number < other.number

    def __gt__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number > other.number

    def __le__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number <= other.number

    def __ge__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number >= other.number

    def __eq__(self, other):
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number == other.number

