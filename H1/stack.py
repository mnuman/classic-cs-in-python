from typing import TypeVar, Generic, List
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T, validator=None) -> None:
        self._container.append(item)
        if validator is not None:
            validator(self._container)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self):
        return repr(self._container)
