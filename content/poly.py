from fractions import Fraction
from itertools import zip_longest
from typing import Callable, Iterator, List, Union, overload


class Polynomial:
    def __init__(self, coeffs: int | Fraction | List[int | Fraction] | "Polynomial"):
        if isinstance(coeffs, Polynomial):
            self._coeffs = coeffs._coeffs
            return
        if isinstance(coeffs, List):
            self._coeffs = [Fraction(c) for c in coeffs]
        else:
            self._coeffs = [Fraction(coeffs)]
        while self._coeffs and self._coeffs[-1] == 0:
            self._coeffs.pop()

    @overload
    def eval(self, x: int | Fraction) -> Fraction: ...

    @overload
    def eval(self, x: "Polynomial") -> "Polynomial": ...

    def eval(
        self, x: Union[int, Fraction, "Polynomial"]
    ) -> Union[Fraction, "Polynomial"]:
        if isinstance(x, Polynomial):
            result = Polynomial(0)
        else:
            result = Fraction(0)
        for coeff in reversed(self._coeffs):
            result = result * x + coeff
        return result

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Polynomial):
            return self._coeffs == other._coeffs
        elif len(self._coeffs) == 0:
            return other == 0
        elif len(self._coeffs) == 1:
            return self._coeffs[0] == other
        else:
            return False

    def __neg__(self) -> "Polynomial":
        return Polynomial([-c for c in self._coeffs])

    def __add__(self, rhs: Union[int, Fraction, "Polynomial"]) -> "Polynomial":
        return bin_helper(_add, self, rhs)

    def __radd__(self, lhs: Union[int, Fraction, "Polynomial"]) -> "Polynomial":
        return bin_helper(_add, lhs, self)

    def __sub__(self, rhs: Union[int, Fraction, "Polynomial"]) -> "Polynomial":
        return bin_helper(_add, self, -rhs)

    def __rsub__(self, lhs: Union[int, Fraction, "Polynomial"]) -> "Polynomial":
        return bin_helper(_add, lhs, -self)

    def __mul__(self, rhs: Union[int, Fraction, "Polynomial"]) -> "Polynomial":
        return bin_helper(_mul, self, rhs)

    def __rmul__(self, lhs: Union[int, Fraction, "Polynomial"]) -> "Polynomial":
        return bin_helper(_mul, lhs, self)

    def __truediv__(self, rhs: int | Fraction) -> "Polynomial":
        if rhs == 0:
            raise ZeroDivisionError("division by zero")
        return Polynomial([c / rhs for c in self._coeffs])

    def __pow__(self, rhs: int) -> "Polynomial":
        result = Polynomial(1)
        mult = self
        while rhs > 0:
            (q, r) = divmod(rhs, 2)
            if r == 1:
                result *= mult
            mult *= mult
            rhs = q
        return result

    def __str__(self) -> str:
        if not self._coeffs:
            return "0"
        terms: List[str] = []
        for i, coeff in enumerate(self._coeffs):
            if coeff == 0:
                continue
            if i == 0:
                term = f"{coeff}"
            else:
                if coeff == 1:
                    coeffstr = ""
                elif coeff == -1:
                    coeffstr = "-"
                elif coeff.is_integer():
                    coeffstr = str(coeff)
                else:
                    coeffstr = f"({str(coeff)})"
                if i == 1:
                    term = f"{coeffstr}x"
                else:
                    term = f"{coeffstr}x**{i}"
            terms.append(term)
        return " + ".join(reversed(terms)).replace("+ -", "- ").replace("+ (-", "- (")

    def __repr__(self) -> str:
        return f"Polynomial({self._coeffs})"

    def degree(self) -> int:
        return max(0, len(self._coeffs) - 1)

    def coeffs(self) -> Iterator[Fraction]:
        return iter(self._coeffs)

    def coeff_at(self, d: int) -> Fraction:
        assert d >= 0, "Degree must be non-negative"
        if d < len(self._coeffs):
            return self._coeffs[d]
        else:
            return Fraction(0)


def _add(l: Polynomial, r: Polynomial) -> Polynomial:
    raw_coeffs: List[int | Fraction] = [
        a + b for (a, b) in zip_longest(l.coeffs(), r.coeffs(), fillvalue=Fraction(0))
    ]
    return Polynomial(raw_coeffs)


def _mul(l: Polynomial, r: Polynomial) -> Polynomial:
    result: List[int | Fraction] = [Fraction(0)] * (l.degree() + r.degree() + 1)
    for li, lc in enumerate(l.coeffs()):
        for ri, rc in enumerate(r.coeffs()):
            result[li + ri] += lc * rc
    return Polynomial(result)


def bin_helper(
    f: Callable[[Polynomial, Polynomial], Polynomial],
    l: int | Fraction | Polynomial,
    r: int | Fraction | Polynomial,
) -> Polynomial:
    l_poly = Polynomial(l)
    r_poly = Polynomial(r)
    return f(l_poly, r_poly)


x = Polynomial([0, 1])
