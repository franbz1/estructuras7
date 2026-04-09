from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from doubly_linked_list import DoublyLinkedList, Node


@dataclass(frozen=True)
class Song:
    name: str


class SongsLRUCache:
    def __init__(self, capacity: int = 100) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be greater than zero.")
        if capacity > 100:
            raise ValueError("Capacity cannot be greater than 100.")

        self.capacity = capacity
        self.songs = DoublyLinkedList[Song]()
        self.lookup: Dict[str, Node[Song]] = {}

    def __len__(self) -> int:
        return len(self.songs)

    def is_empty(self) -> bool:
        return self.songs.is_empty()

    def contains(self, song_name: str) -> bool:
        return song_name in self.lookup

    def add_song(self, song_name: str) -> Song:
        existing_node = self.lookup.get(song_name)
        if existing_node is not None:
            self.songs.remove_node(existing_node)
            del self.lookup[song_name]

        song = Song(name=song_name)
        new_node = self.songs.prepend(song)
        self.lookup[song_name] = new_node

        if len(self.songs) > self.capacity:
            oldest_song = self.songs.remove_last()
            if oldest_song is not None:
                del self.lookup[oldest_song.name]

        return song

    def get_song(self, song_name: str) -> Optional[Song]:
        node = self.lookup.get(song_name)
        if node is None:
            return None

        self.songs.move_to_front(node)
        return node.value

    def remove_song(self, song_name: str) -> bool:
        node = self.lookup.pop(song_name, None)
        if node is None:
            return False

        self.songs.remove_node(node)
        return True

    def remove_most_recent(self) -> Optional[Song]:
        removed_song = self.songs.remove_first()
        if removed_song is not None:
            del self.lookup[removed_song.name]
        return removed_song

    def remove_oldest(self) -> Optional[Song]:
        removed_song = self.songs.remove_last()
        if removed_song is not None:
            del self.lookup[removed_song.name]
        return removed_song

    def most_recent_song(self) -> Optional[Song]:
        return None if self.songs.head is None else self.songs.head.value

    def oldest_song(self) -> Optional[Song]:
        return None if self.songs.tail is None else self.songs.tail.value

    def list_recent_to_oldest(self) -> List[str]:
        return [song.name for song in self.songs.iterate_forward()]

    def list_oldest_to_recent(self) -> List[str]:
        return [song.name for song in self.songs.iterate_backward()]

    def clear(self) -> None:
        self.songs = DoublyLinkedList[Song]()
        self.lookup.clear()
