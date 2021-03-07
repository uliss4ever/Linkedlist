from typing import Any, Optional

"""
    1. Реализовать класс JsonFileDriver, который будет описывать логику считывания (записи) элементов из (в) json файл.
    2. Реализовать класс SimpleFileDriver, который будет описывать логику считывания (записи) элементов из (в) файл.
    3. В блоке __main__ протестировать работу драйверов
"""

from typing import Sequence
from abc import ABC, abstractmethod
import json
import pickle
import sys
import weakref
class IStructureDriver(ABC):


    @abstractmethod
    def read(self) -> Sequence:
        """
        Считывает информацию из драйвера и возвращает её для объекта, использующего этот драйвер
        :return Последовательность элементов, считанная драйвером, для объекта
        """
        pass

    @abstractmethod
    def write(self, data: Sequence) -> None:
        """
        Получает информацию из объекта, использующего этот драйвер, и записывает её в драйвер
        :param data Последовательность элементов, полученная от объекта, для записи драйвером
        """
        pass


class JsonFileDriver(IStructureDriver):
    def __init__(self, filename: str):
        self._filename = filename


    def read(self) -> Sequence:
        with open(self._filename) as file:
            return json.load(file)


    def write(self, data: Sequence) -> None:
        with open(self._filename, "w") as file:
            json.dump(data, file)



class PicleFileDriver(IStructureDriver):
    def __init__(self, filename: str):
        self._filename = filename


    def read(self) -> Sequence:
        with open(self._filename, "rb") as file:
            return pickle.load(file)


    def write(self, data: Sequence) -> None:
        with open(self._filename, "wb") as file:
            pickle.dump(data, file)

# def main():
#     driver1: IStructureDriver = JsonFileDriver("/Users/evgeniakalinina/Desktop/smfile")
#     driver2: IStructureDriver = PicleFileDriver("/Users/evgeniakalinina/Desktop/smbin")
#     a = [2, 4, 6]
#     driver1.write(a)
#     print(driver1.read())
#     driver2.write(a)
#     print(driver2.read())
#
# if __name__ == '__main__':
#     main()



class Node:
    def __init__(self, data: Any, next_node: Optional["Node"] = None):
        self.data = data
        self.next_node = next_node

    def __str__(self):
        return f"({self.data})"

    @property
    def next_node(self):
        return self._next_node

    @next_node.setter
    def next_node(self, value):
        if value is not None and not isinstance(value, Node):
            raise ValueError

        self._next_node = value


class DoubleNode(Node):
    def __init__(
            self, data: Any, next_node: Optional["Node"] = None, prev_node: Optional["Node"] = None
    ):
        super().__init__(data, next_node)
        self.prev_node = prev_node

    def __str__(self):
        return f"[{self.data}]"

    @property
    def prev_node(self):
        return self._prev_node()

    @prev_node.setter
    def prev_node(self, value):
        if value is not None and not isinstance(value, Node):
            raise ValueError

        self._prev_node = weakref.ref(value)


# не используется
class LinkedListIterator:
    def __init__(self, head):
        self.current = head

    def __next__(self):
        if self.current is None:
            raise StopIteration

        node = self.current
        self.current = self.current.next_node
        return node.data

    def __iter__(self):
        return self


class LinkedList:
    def __init__(self, node_type=Node):
        self.head = None
        self._size = 0
        self._node_type = node_type


    def __str__(self):
        return "->".join(str(node) for node in self._node_iter())

    def __len__(self):
        return self._size
    def _get_node_(self, item):
        if not isinstance(item, int):  # item - индекс
            raise TypeError

        if item >= len(self) or item < 0:
            raise IndexError

        for i, node in enumerate(self._node_iter()):
            if i == item:
                return node

    def __getitem__(self, item):
        return self._get_node_(item).data

    def __setitem__(self, key, value):
        self._get_node_(key).data = value

    def __delitem__(self, key):
        self.delete(key)

    def __iter__(self):
        for node in self._node_iter():
            yield node.data

    def _node_iter(self):
        current_node = self.head
        while current_node is not None:
            yield current_node
            current_node = current_node.next_node

    def append(self, data: Any):
        new_node = self._node_type(data)

        for current_node in self._node_iter():
            if current_node.next_node is None:  # tail!
                current_node.next_node = new_node
                break
        else:
            self.head = new_node
        self._size += 1

    def insert(self, data, index=0):
        if index < 0 or index > self._size:
            raise ValueError

        new_node = self._node_type(data)
        self._size += 1
        if index == 0:
            new_node.next_node = self.head
            self.head = new_node
        else:
            for i, node in enumerate(self._node_iter()):
                if i == index - 1:
                    new_node.next_node = node.next_node
                    node.next_node = new_node

    def clear(self):
        self._size = 0
        self.head = None

    def index(self, data: Any):
        for i, node in enumerate(self._node_iter()):
            if node.data == data:
                return i

        raise ValueError

    def delete(self, index: int):
        if index < 0 or index >= self._size:
            raise ValueError

        self._size -= 1
        if index == 0:
            self.head = self.head.next_node
        else:
            for i, node in enumerate(self._node_iter()):
                if i == index - 1:
                    node.next_node = node.next_node.next_node



class DoubleLinkedList(LinkedList):
    def __init__(self, node_type=DoubleNode):
        super().__init__(node_type)
        self.tail = None

    def __str__(self):
        return "<->".join(str(node) for node in self._node_iter())


    def _node_iter_rev(self):     # перебираем ноды в обратном порядке
        current_node = self.tail
        while current_node is not None:
            yield current_node
            current_node = current_node.prev_node


    def _get_node_(self, item):
        if not isinstance(item, int):  # item - индекс
            raise TypeError

        if item >= len(self) or item < 0:
            raise IndexError
        if item < self._size/2:
            return super()._get_node_(item)

        for i, node in enumerate(self._node_iter_rev()):
            if i == self._size - 1 -item:
                return node


    def append(self, data: Any):
        new_node = self._node_type(data)
        if self._size == 0:
            self.head = new_node
            self.tail = new_node
        else:
            old_node = self.tail
            self.tail = new_node
            old_node.next_node = new_node
            new_node.prev_node = old_node
        self._size += 1


    def insert(self, data, index=0):
        if index < 0 or index > self._size:
            raise ValueError

        new_node = self._node_type(data)
        if index == 0:
            old_node = self.head.next_node
            self.head = new_node
            new_node.next_node = self.head
            old_node.prev_node = new_node
        elif index == self._size:
            self.append(data)
            return
        else:
            old_node = self._get_node_(index)
            old_node_left = self._get_node_(index-1)
            new_node.next_node = old_node
            old_node.prev_node = new_node
            new_node.prev_node = old_node_left
            old_node_left.next_node = new_node
        self._size += 1



    def clear(self):
        # self._size = 0
        # self.head = None
        super().clear()
        self.tail = None

    def index(self, data: Any):  # наверное такой же, как родительский метод?
        for i, node in enumerate(self._node_iter()):
            if node.data == data:
                return i
        raise ValueError


    """Всё ещё непонятно, почему мы не можем удалять -1 элемент"""


    def delete(self, index: int):
        if index < 0 or index >= self._size:
            raise ValueError

        if index == 0:
            self.head = self.head.next_node
            self.head.prev_node = None
        elif index == self._size - 1:
            self.tail = self.tail.prev_node
            self.tail.next_node = None

        else:
            new_node_l = self._get_node_(index-1)
            new_node_r = self._get_node_(index + 1)
            new_node_l.next_node = new_node_r
            new_node_r.prev_node = new_node_l
        self._size -= 1

class LinkedListWithDriver(LinkedList):
    def __init__(self, driver: IStructureDriver):
        self._driver = driver
        super().__init__()

    def read(self):
        self.clear()
        for item in self._driver.read():
            self.append(item)

    def write(self):
        ll_as_list = [item for item in self]
        self._driver.write(ll_as_list)


def main():
    driver = PicleFileDriver("some.bin")
    ll = LinkedListWithDriver(driver)
    ll.append("a")
    ll.append("b")
    ll.append("c")
    ll.append("d")
    ll.append("e")
    ll.write()
    ll[2] = "g"
    print(ll)
    ll2 = LinkedListWithDriver(driver)
    ll2.read()
    print(ll2)
    # ll.insert("6", 5)
    # ll.insert("6", 2)
    # ll.insert("6", 0)
    # print(ll)

if __name__ == "__main__":
    main()
