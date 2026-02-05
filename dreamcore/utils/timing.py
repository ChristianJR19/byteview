"""
Pacing and arc control — determines rhythm and structure of dreams.

Each dream has a narrative arc that controls intensity, pacing,
and tone shifts across its fragments. The arc type determines
whether the dream builds up, descends into darkness, cycles, or
scatters chaotically.
"""

from __future__ import annotations

from enum import Enum
from typing import Any


class ArcType(Enum):
    """Narrative arc shapes for dream sequences."""
    DESCENT = "descent"     # Starts calm, goes deeper/darker.
    ASCENT = "ascent"       # Starts dark/heavy, rises to light.
    CYCLE = "cycle"         # Oscillates between light and dark.
    SCATTER = "scatter"     # Random intensity, no clear pattern.


class PacingCurve:
    """Computes pacing weights and tone shifts for dream arcs."""

    def compute(self, arc: ArcType, depth: int) -> list[dict[str, Any]]:
        """Compute pacing data for each fragment position.

        Returns a list of dicts, one per fragment, with:
            - weight: duration weight (how long to linger).
            - intensity: target intensity at this position.
            - shift_tone: whether to shift tone from base.
        """
        if arc == ArcType.DESCENT:
            return self._descent(depth)
        elif arc == ArcType.ASCENT:
            return self._ascent(depth)
        elif arc == ArcType.CYCLE:
            return self._cycle(depth)
        else:
            return self._scatter(depth)

    def _descent(self, depth: int) -> list[dict[str, Any]]:
        """Starts calm, each fragment goes deeper."""
        result = []
        for i in range(depth):
            position = i / max(1, depth - 1)
            result.append({
                "weight": 1.0 + position * 0.5,  # Lingers longer deeper in.
                "intensity": 0.2 + position * 0.6,
                "shift_tone": position > 0.5,
            })
        return result

    def _ascent(self, depth: int) -> list[dict[str, Any]]:
        """Starts heavy/dark, rises toward light."""
        result = []
        for i in range(depth):
            position = i / max(1, depth - 1)
            result.append({
                "weight": 1.5 - position * 0.5,  # Starts slow, quickens.
                "intensity": 0.7 - position * 0.4,
                "shift_tone": position > 0.5,
            })
        return result

    def _cycle(self, depth: int) -> list[dict[str, Any]]:
        """Oscillates between light and dark."""
        import math
        result = []
        for i in range(depth):
            position = i / max(1, depth - 1)
            wave = (math.sin(position * math.pi * 2) + 1) / 2
            result.append({
                "weight": 1.0,
                "intensity": 0.3 + wave * 0.4,
                "shift_tone": wave < 0.3 or wave > 0.7,
            })
        return result

    def _scatter(self, depth: int) -> list[dict[str, Any]]:
        """Random intensity, unpredictable pacing."""
        import random
        rng = random.Random(depth)
        result = []
        for _ in range(depth):
            result.append({
                "weight": 0.5 + rng.random() * 1.5,
                "intensity": rng.random(),
                "shift_tone": rng.random() > 0.5,
            })
        return result
