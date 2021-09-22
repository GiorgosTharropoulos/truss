import itertools
from typing import TypeVar, Iterable

T = TypeVar("T")


def flatten(iterable: Iterable[Iterable[T]]):
    return list(itertools.chain.from_iterable(iterable))
