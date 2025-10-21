from abc import ABC, abstractmethod
from typing import Callable

class Pointer:
    def __init__(self, tokens:list[str]):
        self.tokens:list[str] = tokens
        self.current:int = -1
    
    def __len__(self) -> int:
        return len(self.tokens)

    def __iter__(self) -> "Pointer":
        self.current = -1
        return self

    def __next__(self) -> str:
        if self.current < self.tokens:
            self.current += 1
            return self.tokens[self.current]
        raise StopIteration

    def __getitem__(self, index:int) -> str:
        return self.tokens[index]


class TokenStep(ABC):
    @abstractmethod
    def run(pointer:Pointer, moveStep:Callable[[str], None]) -> None:
        pass



class TokenizerCode:
    def __init__(self):
        self.token:list[str] = []
