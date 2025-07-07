from fractions import Fraction
from typing import Generator, Set, TypeVar

from poly import Polynomial

T = TypeVar("T", int, Fraction, Polynomial)


def permutations(elems: str, k: int) -> Generator[str, None, None]:
    if len(elems) < k:
        return
    elif k == 0:
        yield ""
        return
    used: Set[str] = set()
    for i, elem in enumerate(elems):
        if elem in used:
            continue
        remaining = elems[:i] + elems[i + 1 :]
        for perm in permutations(remaining, k - 1):
            yield elem + perm
        used.add(elem)


def combinations(elems: str, k: int) -> Generator[str, None, None]:
    if len(elems) < k:
        return
    elif k == 0:
        yield ""
        return
    for comb in combinations(elems[1:], k - 1):
        yield elems[0] + comb
    remaining = "".join(e for e in elems[1:] if e != elems[0])
    for comb in combinations(remaining, k):
        yield comb


def type_preserving_true_div(a: T, b: int) -> T:
    if b == 0:
        raise ZeroDivisionError("division by zero")
    if isinstance(a, int):
        (q, r) = divmod(a, b)
        if r == 0:
            return q
        else:
            raise ValueError(
                f"Cannot preserve type for {a} / {b}, remainder {r} is not zero."
            )
    else:
        return a / b


def choose(n: T, k: int) -> T:
    if k < 0:
        return type(n)(0)
    result = type(n)(1)
    for i in range(k):
        result = type_preserving_true_div(result * (n - i), i + 1)
        if result == 0:
            break
    return result


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("Factorial is not defined for negative integers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
