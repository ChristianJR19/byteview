"""
Memory consolidation — models how dreams process and reorganize memories.

During dreaming, the consolidation engine:
1. Identifies which memories are emotionally charged.
2. Reduces emotional intensity (processing).
3. Strengthens important memories.
4. Creates new associative links between related memories.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dreamcore.memory.anchors import MemoryAnchor, AnchorSet


@dataclass
class ConsolidationResult:
    """Result of dream-based memory consolidation."""
    strengthened: list[str]  # Content summaries of strengthened memories.
    processed: list[str]     # Content summaries of emotionally processed memories.
    new_associations: list[tuple[str, str]]  # Pairs of newly linked memory summaries.

    def to_dict(self) -> dict[str, Any]:
        return {
            "strengthened": self.strengthened,
            "processed": self.processed,
            "new_associations": [list(a) for a in self.new_associations],
        }


class ConsolidationEngine:
    """Processes memories during dream generation."""

    def __init__(
        self,
        strengthen_threshold: float = 0.5,
        process_threshold: float = 0.3,
    ) -> None:
        self._strengthen_threshold = strengthen_threshold
        self._process_threshold = process_threshold

    def consolidate(self, anchors: AnchorSet) -> ConsolidationResult:
        """Run consolidation on a set of memory anchors.

        High-salience memories get strengthened.
        High-emotion memories get their emotional weight reduced (processed).
        Memories with overlapping tags get linked.
        """
        strengthened: list[str] = []
        processed: list[str] = []
        associations: list[tuple[str, str]] = []

        all_anchors = anchors.strongest(n=20)

        for anchor in all_anchors:
            # Strengthen high-salience memories.
            if anchor.salience >= self._strengthen_threshold:
                anchor.salience = min(1.0, anchor.salience + 0.05)
                strengthened.append(anchor.content[:60])

            # Process high-emotion memories (reduce emotional charge).
            if anchor.emotional_weight >= self._process_threshold:
                anchor.emotional_weight *= 0.85
                processed.append(anchor.content[:60])

        # Find associations by tag overlap.
        for i, a in enumerate(all_anchors):
            for j, b in enumerate(all_anchors):
                if i >= j:
                    continue
                if a.tags and b.tags:
                    overlap = set(a.tags) & set(b.tags)
                    if overlap:
                        associations.append((a.content[:40], b.content[:40]))

        return ConsolidationResult(
            strengthened=strengthened,
            processed=processed,
            new_associations=associations[:5],  # Cap at 5.
        )
