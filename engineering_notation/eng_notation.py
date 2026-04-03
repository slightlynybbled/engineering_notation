from __future__ import annotations

from decimal import Decimal
import re
from string import digits
import sys
from types import NotImplementedType

from typing import Self

try:
    import numpy
except ImportError:
    numpy = None

_suffix_lookup = {
    "q": "e-30",
    "r": "e-27",
    "y": "e-24",
    "z": "e-21",
    "a": "e-18",
    "f": "e-15",
    "p": "e-12",
    "n": "e-9",
    "u": "e-6",
    "m": "e-3",
    "": "e0",
    "k": "e3",
    "M": "e6",
    "G": "e9",
    "T": "e12",
    "P": "e15",
    "E": "e18",
    "Z": "e21",
    "R": "e27",
    "Q": "e30",
}

_suffix_keys = tuple(key for key in _suffix_lookup.keys() if key != "")
_NUM_RE = re.compile(r"^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")

_exponent_lookup_scaled = {
    "-60": "q",
    "-57": "r",
    "-54": "y",
    "-51": "z",
    "-48": "a",
    "-45": "f",
    "-42": "p",
    "-39": "n",
    "-36": "u",
    "-33": "m",
    "-30": "",
    "-27": "k",
    "-24": "M",
    "-21": "G",
    "-18": "T",
    "-15": "P",
    "-12": "E",
    "-9": "Z",
    "-3": "R",
    "0": "Q",
}


def _split_value_and_unit(value: str) -> tuple[str, str | None]:
    """
    Split a string into the numeric+suffix portion and the unit portion.

    Args:
        value: Raw input string (for example, "220kHz", "1.2M", "-0.22ohm").

    Returns:
        Tuple of (numeric portion, unit suffix or None).
    """
    match = _NUM_RE.match(value)
    if match is None:
        return "", value or None

    numeric = match.group(0)
    rest = value[len(numeric) :]
    suffix = ""
    if rest and rest[0] in _suffix_keys:
        suffix = rest[0]
        rest = rest[1:]
    unit = rest if rest else None
    return numeric + suffix, unit


class EngUnit:
    """
    Engineering notation number with an optional unit suffix.

    Provides arithmetic and comparison with unit checking.
    """

    def __init__(
        self,
        value: str | int | float | EngNumber | EngUnit,
        precision: int | None = None,
        significant: int = 0,
        unit: str | None = None,
        separator: str = "",
    ) -> None:
        """
        Initialize an engineering number with an optional unit suffix.

        Args:
            value: String, int, float, or EngNumber value to parse.
            precision: Decimal places used when significant is 0.
                Defaults to 2 when None.
            significant: Significant digits; takes precedence over precision.
            unit: Explicit unit suffix. If None, a unit suffix is parsed from
                the end of a string value when present.
            separator: String inserted between the numeric value and suffix.
        """
        self.unit = unit

        if isinstance(value, str):
            # parse the string into unit and engineering number
            new_value, parsed_unit = _split_value_and_unit(value)
            if self.unit is None and parsed_unit is not None:
                self.unit = parsed_unit

            self.eng_num = EngNumber(new_value, precision, significant, separator)

        else:
            self.eng_num = EngNumber(value, precision, significant, separator)

    def __repr__(self) -> str:
        """
        Return the engineering string with unit suffix.

        Returns:
            String representation with unit suffix.
        """
        unit = self.unit if self.unit else ""
        return str(self.eng_num) + unit

    def _coerce_other(self, other: str | int | float | EngNumber | EngUnit) -> EngUnit:
        """
        Normalize another operand to an EngUnit instance.

        Args:
            other: Value to coerce into an EngUnit.

        Returns:
            EngUnit instance for arithmetic and comparison.
        """
        if isinstance(other, EngUnit):
            return other
        return EngUnit(str(other))

    def _unit_str(self) -> str:
        """
        Return the unit suffix as a string.

        Returns:
            Unit suffix or an empty string when unitless.
        """
        return self.unit if self.unit else ""

    def _compose_unit(self, other: EngUnit, op: str) -> str:
        """
        Compose a unit string based on the operation.

        Args:
            other: Other EngUnit operand.
            op: Operation identifier ("mul" or "div").

        Returns:
            Composed unit suffix string.
        """
        left = self._unit_str()
        right = other._unit_str()
        if op == "mul":
            return left + right
        if op == "div":
            return left + (f"/{right}" if right else "")
        raise ValueError(f"Unsupported unit operation: {op}")

    def __str__(self) -> str:
        """
        Return the engineering string with unit suffix.

        Returns:
            String representation with unit suffix.
        """
        return self.__repr__()

    def __int__(self) -> int:
        """
        Convert to int by discarding fractional components.

        Returns:
            Integer value of the numeric portion.
        """
        return int(self.eng_num)

    def __float__(self) -> float:
        """
        Convert to float.

        Returns:
            Float value of the numeric portion.
        """
        return float(self.eng_num)

    def __add__(self, other: str | int | float | EngNumber | EngUnit) -> Self:
        """
        Add two engineering numbers with matching units.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            EngUnit sum with the same unit suffix.

        Raises:
            AttributeError: If units do not match.
        """
        other = self._coerce_other(other)

        if self._unit_str() != other._unit_str():
            raise AttributeError("units do not match")

        return EngUnit(str(self.eng_num + other.eng_num) + self._unit_str())

    def __radd__(self, other: str | int | float | EngNumber | EngUnit) -> Self:
        """
        Right-hand addition for EngUnit.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            EngUnit sum with the same unit suffix.
        """
        return self.__add__(other)

    def __sub__(self, other: str | int | float | EngNumber | EngUnit) -> Self:
        """
        Subtract two engineering numbers with matching units.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            EngUnit difference with the same unit suffix.

        Raises:
            AttributeError: If units do not match.
        """
        other = self._coerce_other(other)

        if self._unit_str() != other._unit_str():
            raise AttributeError("units do not match")

        return EngUnit(str(self.eng_num - other.eng_num) + self._unit_str())

    def __rsub__(self, other: str | int | float | EngNumber | EngUnit) -> Self:
        """
        Right-hand subtraction for EngUnit.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            EngUnit difference with the same unit suffix.

        Raises:
            AttributeError: If units do not match.
        """
        other = self._coerce_other(other)

        if self._unit_str() != other._unit_str():
            raise AttributeError("units do not match")

        return EngUnit(str(other.eng_num - self.eng_num) + self._unit_str())

    def __mul__(self, other: str | int | float | EngNumber | EngUnit) -> Self:
        """
        Multiply two engineering numbers and concatenate units.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            EngUnit product with combined unit suffix.
        """
        other = self._coerce_other(other)

        return EngUnit(
            str(self.eng_num * other.eng_num) + self._compose_unit(other, "mul")
        )

    def __rmul__(self, other: str | int | float | EngNumber | EngUnit) -> Self:
        """
        Right-hand multiplication for EngUnit.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            EngUnit product with combined unit suffix.
        """
        return self.__mul__(other)

    def __truediv__(self, other: str | int | float | EngNumber | EngUnit) -> Self:
        """
        Divide two engineering numbers and compose a ratio unit.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            EngUnit quotient with "a/b" unit suffix when needed.
        """
        other = self._coerce_other(other)

        return EngUnit(
            str(self.eng_num / other.eng_num) + self._compose_unit(other, "div")
        )

    def __rtruediv__(self, other: str | int | float | EngNumber | EngUnit) -> Self:
        """
        Right-hand division for EngUnit.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            EngUnit quotient with "a/b" unit suffix when needed.
        """
        other = self._coerce_other(other)

        return EngUnit(
            str(other.eng_num / self.eng_num) + other._compose_unit(self, "div")
        )

    def __lt__(self, other: str | int | float | EngNumber | EngUnit) -> bool:
        """
        Compare two engineering numbers with matching units.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            True if self < other.

        Raises:
            AttributeError: If units do not match.
        """
        other = self._coerce_other(other)

        if self._unit_str() != other._unit_str():
            raise AttributeError("units do not match")

        return self.eng_num < other.eng_num

    def __gt__(self, other: str | int | float | EngNumber | EngUnit) -> bool:
        """
        Compare two engineering numbers with matching units.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            True if self > other.

        Raises:
            AttributeError: If units do not match.
        """
        other = self._coerce_other(other)

        if self._unit_str() != other._unit_str():
            raise AttributeError("units do not match")

        return self.eng_num > other.eng_num

    def __le__(self, other: str | int | float | EngNumber | EngUnit) -> bool:
        """
        Compare two engineering numbers with matching units.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            True if self <= other.

        Raises:
            AttributeError: If units do not match.
        """
        other = self._coerce_other(other)

        if self._unit_str() != other._unit_str():
            raise AttributeError("units do not match")

        return self.eng_num <= other.eng_num

    def __ge__(self, other: str | int | float | EngNumber | EngUnit) -> bool:
        """
        Compare two engineering numbers with matching units.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            True if self >= other.

        Raises:
            AttributeError: If units do not match.
        """
        other = self._coerce_other(other)

        if self._unit_str() != other._unit_str():
            raise AttributeError("units do not match")

        return self.eng_num >= other.eng_num

    def __eq__(self, other: object) -> bool | NotImplementedType:
        """
        Compare two engineering numbers with matching units.

        Args:
            other: EngUnit, EngNumber, or numeric value.

        Returns:
            True if values are numerically equal.

        Raises:
            AttributeError: If units do not match.
        """
        if not isinstance(other, (EngNumber, EngUnit, str, int, float)):
            return NotImplemented
        other = self._coerce_other(other)

        if self._unit_str() != other._unit_str():
            raise AttributeError("units do not match")

        return self.eng_num == other.eng_num


class EngNumber:
    """
    Engineering notation number backed by Decimal.
    """

    def __init__(
        self,
        value: str | int | float | EngNumber,
        precision: int | None = None,
        significant: int = 0,
        separator: str = "",
    ) -> None:
        """
        Initialize an engineering notation value.

        Args:
            value: String, int, float, or EngNumber value to parse.
            precision: Decimal places used when significant is 0.
                Defaults to 2 when None.
            significant: Significant digits; takes precedence over precision.
            separator: String inserted between the numeric value and suffix.

        Raises:
            TypeError: If the value type is unsupported.
            ValueError: If a string value cannot be parsed by Decimal.
        """
        self.precision = 2 if precision is None else precision
        self._precision_explicit = precision is not None
        self.significant = significant
        self.separator = separator

        if isinstance(value, str):
            numeric_part, _ = _split_value_and_unit(value)
            for suffix in _suffix_keys:
                if suffix == numeric_part[-1]:
                    numeric_part = numeric_part[:-1] + _suffix_lookup[suffix]
                    break

            self.number = Decimal(numeric_part)

        elif (
            isinstance(value, int)
            or isinstance(value, float)
            or isinstance(value, EngNumber)
        ):
            self.number = Decimal(str(value))
        else:
            # finally, check for numpy import
            if numpy is not None and isinstance(value, numpy.integer):
                self.number = Decimal(str(value))
            else:
                raise TypeError(
                    f"Unsupported type for EngNumber: {type(value).__name__}"
                )

    def to_pn(self, sub_letter: str | None = None) -> str:
        """
        Return a part-number style string for the value.

        For example, "1.2k" becomes "1k20".

        Args:
            sub_letter: Replacement letter for decimal points when no suffix
                is present (for example, "R" for resistors).

        Returns:
            Part-number style string.
        """
        string = str(self)
        if "." not in string:
            return string

        # take care of the case of when there is no scaling unit
        if not string[-1].isalpha():
            if sub_letter is not None:
                return string.replace(".", sub_letter)

            return string

        letter = string[-1]
        return string.replace(".", letter)[:-1].strip(self.separator)

    def __repr__(self) -> str:
        """
        Return the engineering notation string with suffix.

        Returns:
            String representation using SI prefixes.
        """
        if self.number == 0:
            base = Decimal(0)
            exponent = "-30"
        else:
            adjusted = self.number.adjusted()
            exp = adjusted - (adjusted % 3)
            base = self.number.scaleb(-exp)
            exponent = str(exp - 30)

        if self.significant > 0:
            if abs(Decimal(base)) >= 100.0:
                base = str(round(Decimal(base), self.significant - 3))
            elif abs(Decimal(base)) >= 10.0:
                base = str(round(Decimal(base), self.significant - 2))
            else:
                base = str(round(Decimal(base), self.significant - 1))
        else:
            base = str(round(Decimal(base), self.precision))

        if "e" in base.lower():
            base = str(int(Decimal(base)))

        # remove trailing decimals:
        # print(base)
        # https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python
        # https://stackoverflow.com/questions/11227620/drop-trailing-zeros-from-decimal
        # base = '%s' % float("%#.2G"%Decimal(base))
        # print(base)
        # remove trailing decimal
        if "." in base:
            base = base.rstrip(".")

        # remove trailing .00 in precision 2
        if (
            self.precision == 2
            and self.significant == 0
            and not self._precision_explicit
        ):
            if ".00" in base:
                base = base[:-3]

        return base + self.separator + _exponent_lookup_scaled[exponent]

    def __str__(self, eng: bool = True, context: object | None = None) -> str:
        """
        Return the engineering notation string.

        Args:
            eng: Unused; kept for compatibility.
            context: Unused; kept for compatibility.

        Returns:
            String representation using SI prefixes.
        """
        return self.__repr__()

    def __int__(self) -> int:
        """
        Convert to int by discarding fractional components.

        Returns:
            Integer value of the numeric portion.
        """
        return int(self.number)

    def __float__(self) -> float:
        """
        Convert to float.

        Returns:
            Float value of the numeric portion.
        """
        return float(self.number)

    def __add__(self, other: str | int | float | EngNumber) -> Self:
        """
        Add two engineering numbers.

        Args:
            other: EngNumber or numeric value.

        Returns:
            EngNumber sum.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number + other.number
        return EngNumber(str(num))

    def __radd__(self, other: str | int | float | EngNumber) -> Self:
        """
        Right-hand addition for EngNumber.

        Args:
            other: EngNumber or numeric value.

        Returns:
            EngNumber sum.
        """
        return self.__add__(other)

    def __sub__(self, other: str | int | float | EngNumber) -> Self:
        """
        Subtract two engineering numbers.

        Args:
            other: EngNumber or numeric value.

        Returns:
            EngNumber difference.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number - other.number
        return EngNumber(str(num))

    def __rsub__(self, other: str | int | float | EngNumber) -> Self:
        """
        Right-hand subtraction for EngNumber.

        Args:
            other: EngNumber or numeric value.

        Returns:
            EngNumber difference.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = other.number - self.number
        return EngNumber(str(num))

    def __mul__(self, other: str | int | float | EngNumber) -> Self:
        """
        Multiply two engineering numbers.

        Args:
            other: EngNumber or numeric value.

        Returns:
            EngNumber product.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number * other.number
        return EngNumber(str(num))

    def __rmul__(self, other: str | int | float | EngNumber) -> Self:
        """
        Right-hand multiplication for EngNumber.

        Args:
            other: EngNumber or numeric value.

        Returns:
            EngNumber product.
        """
        return self.__mul__(other)

    def __truediv__(self, other: str | int | float | EngNumber) -> Self:
        """
        Divide two engineering numbers.

        Args:
            other: EngNumber or numeric value.

        Returns:
            EngNumber quotient.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = self.number / other.number
        return EngNumber(str(num))

    def __rtruediv__(self, other: str | int | float | EngNumber) -> Self:
        """
        Right-hand division for EngNumber.

        Args:
            other: EngNumber or numeric value.

        Returns:
            EngNumber quotient.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        num = other.number / self.number
        return EngNumber(str(num))

    def __lt__(self, other: str | int | float | EngNumber) -> bool:
        """
        Compare two engineering numbers.

        Args:
            other: EngNumber or numeric value.

        Returns:
            True if self < other.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number < other.number

    def __gt__(self, other: str | int | float | EngNumber) -> bool:
        """
        Compare two engineering numbers.

        Args:
            other: EngNumber or numeric value.

        Returns:
            True if self > other.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number > other.number

    def __le__(self, other: str | int | float | EngNumber) -> bool:
        """
        Compare two engineering numbers.

        Args:
            other: EngNumber or numeric value.

        Returns:
            True if self <= other.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number <= other.number

    def __ge__(self, other: str | int | float | EngNumber) -> bool:
        """
        Compare two engineering numbers.

        Args:
            other: EngNumber or numeric value.

        Returns:
            True if self >= other.
        """
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number >= other.number

    def __eq__(self, other: object) -> bool | NotImplementedType:
        """
        Compare two engineering numbers for equality.

        Args:
            other: EngNumber or numeric value.

        Returns:
            True if values are numerically equal.
        """
        if not isinstance(other, (EngNumber, str, int, float)):
            return NotImplemented
        if not isinstance(other, EngNumber):
            other = EngNumber(other)

        return self.number == other.number
