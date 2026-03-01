"""
Memory anchors — connect dream content to real memories.

Memory anchors are snippets of real interaction content that get
woven into dream fragments. They serve two purposes:
1. Make dreams feel personal and connected to real experience.
2. Model memory consolidation (the brain processing memories during sleep).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Optional

from dreamcore.utils.entropy import DreamEntropy


@dataclass
class MemoryAnchor:
    """A single memory fragment that can be woven into a dream."""

    content: str
    salience: float = 0.5
    emotional_weight: float = 0.3
    tags: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    times_referenced: int = 0

    @property
    def weight(self) -> float:
        """Combined weight for selection probability."""
        return self.salience * 0.6 + self.emotional_weight * 0.4

    def reference(self) -> None:
        """Mark as referenced in a dream."""
        self.times_referenced += 1
        self.salience = min(1.0, self.salience + 0.05)

    def to_dict(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "salience": round(self.salience, 3),
            "emotional_weight": round(self.emotional_weight, 3),
            "tags": self.tags,
            "times_referenced": self.times_referenced,
        }


class AnchorSet:
    """Collection of memory anchors with weighted selection."""

    def __init__(self) -> None:
        self._anchors: list[MemoryAnchor] = []

    def __bool__(self) -> bool:
        return len(self._anchors) > 0

    def __len__(self) -> int:
        return len(self._anchors)

    def add(self, anchor: MemoryAnchor) -> None:
        self._anchors.append(anchor)

    def select_weighted(self, entropy: DreamEntropy) -> Optional[MemoryAnchor]:
        """Select an anchor weighted by combined salience and emotional weight."""
        if not self._anchors:
            return None
        weights = {i: a.weight for i, a in enumerate(self._anchors)}
        idx = int(entropy.weighted_choice({str(k): v for k, v in weights.items()}))
        anchor = self._anchors[idx]
        anchor.reference()
        return anchor

    def by_tag(self, tag: str) -> list[MemoryAnchor]:
        return [a for a in self._anchors if tag in a.tags]

    def strongest(self, n: int = 3) -> list[MemoryAnchor]:
        return sorted(self._anchors, key=lambda a: a.weight, reverse=True)[:n]
