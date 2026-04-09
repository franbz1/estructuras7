from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterator, List, Optional, TypeVar


T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    value: T
    prev: Optional["Node[T]"] = None
    next: Optional["Node[T]"] = None


class DoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.tail: Optional[Node[T]] = None
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def is_empty(self) -> bool:
        return self.length == 0

    def prepend(self, value: T) -> Node[T]:
        new_node = Node(value=value)
        return self.prepend_node(new_node)

    def append(self, value: T) -> Node[T]:
        new_node = Node(value=value)
        return self.append_node(new_node)

    def prepend_node(self, node: Node[T]) -> Node[T]:
        node.prev = None
        node.next = self.head

        if self.head is None:
            self.head = self.tail = node
        else:
            self.head.prev = node
            self.head = node

        self.length += 1
        return node

    def append_node(self, node: Node[T]) -> Node[T]:
        node.next = None
        node.prev = self.tail

        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

        self.length += 1
        return node

    def insert_after(self, node: Node[T], value: T) -> Node[T]:
        if node is self.tail:
            return self.append(value)

        new_node = Node(value=value)
        next_node = node.next

        new_node.prev = node
        new_node.next = next_node
        node.next = new_node

        if next_node is not None:
            next_node.prev = new_node

        self.length += 1
        return new_node

    def insert_before(self, node: Node[T], value: T) -> Node[T]:
        if node is self.head:
            return self.prepend(value)

        new_node = Node(value=value)
        previous_node = node.prev

        new_node.next = node
        new_node.prev = previous_node
        node.prev = new_node

        if previous_node is not None:
            previous_node.next = new_node

        self.length += 1
        return new_node

    def remove_node(self, node: Node[T]) -> T:
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None
        self.length -= 1
        return node.value

    def remove_first(self) -> Optional[T]:
        if self.head is None:
            return None
        return self.remove_node(self.head)

    def remove_last(self) -> Optional[T]:
        if self.tail is None:
            return None
        return self.remove_node(self.tail)

    def move_to_front(self, node: Node[T]) -> None:
        if node is self.head:
            return

        self.remove_node(node)
        self.prepend_node(node)

    def move_to_back(self, node: Node[T]) -> None:
        if node is self.tail:
            return

        self.remove_node(node)
        self.append_node(node)

    def find(self, value: T) -> Optional[Node[T]]:
        current = self.head
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    def iterate_forward(self) -> Iterator[T]:
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def iterate_backward(self) -> Iterator[T]:
        current = self.tail
        while current is not None:
            yield current.value
            current = current.prev

    def to_list_forward(self) -> List[T]:
        return list(self.iterate_forward())

    def to_list_backward(self) -> List[T]:
        return list(self.iterate_backward())
