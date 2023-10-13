from collections import deque
from dataclasses import dataclass,field
from itertools import starmap,repeat
@dataclass
class Queue():
    _items : deque= field(default_factory=deque,repr=False)

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        try:
            return self._items.pop()
        except IndexError:
            return
            #raise IndexError("dequeue from an empty queue") from None

    def __len__(self):
        return len(self._items)

    def __range__(self):
        return range(len(self._items))

    def __contains__(self, item):
        return item in self._items

    def __iter__(self):
        yield from self._items

    def __reversed__(self):
        yield from reversed(self._items)

@dataclass
class ResolvingQueue(Queue):
    def __post_init__(self):
        self._list=list
    def append_resolved_games(self, game_type,status):
        game_resolved = {
            "type": game_type,
            "status": status,
        }
        self._items.append(game_resolved)
    def return_(self):
        
        
        return self._list(starmap(self.dequeue, repeat((), self.__len__())))