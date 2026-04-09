from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class DemoStep:
    action: str
    song_name: Optional[str]
    description: str


DEMO_STEPS: List[DemoStep] = [
    DemoStep("reset", None, "Reset the cache and reload the base songs."),
    DemoStep("use", "Hotel California", "Use a song to move it to the front."),
    DemoStep("use", "Imagine", "Use another song and update recency."),
    DemoStep("add", "Smells Like Teen Spirit", "Add a new song and trigger LRU eviction."),
    DemoStep("add", "Wonderwall", "Add another song and evict the oldest one."),
    DemoStep("remove", "Billie Jean", "Remove a song manually from the cache."),
    DemoStep("add", "Losing My Religion", "Insert a different song into the cache."),
    DemoStep("use", "Wonderwall", "Use a recent song to move it to the front."),
    DemoStep("remove_oldest", None, "Remove the oldest song manually."),
]
