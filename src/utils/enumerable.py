from typing import Callable, Generic, TypeVar, Union

T = TypeVar("T")
TT = TypeVar("TT")


class Enumerable(Generic[T]):
    def __init__(self, items: list[T]) -> None:
        self.items = items

    def first_or_default(
        self,
        predicate: Union[Callable[[T], bool], None] = None,
        default: Union[T, None] = None,
    ) -> Union[T, None]:
        """Returns the first item of the list that satisfies the predicate
        or the default value, None if not specified."""
        if predicate is None:
            return next((item for item in self.items), default)
        return next((item for item in self.items if predicate(item)), default)

    def where(self, predicate: Callable[[T], bool]) -> list[T]:
        """Filter the items of the list based on the predicate."""
        return list(filter(predicate, self.items))

    def map(self, selecttor: Callable[[T], TT]) -> list[TT]:
        """Map the items of the list based on the selector."""
        return list(map(selecttor, self.items))
