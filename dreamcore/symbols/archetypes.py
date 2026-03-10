"""
Symbol archetypes — universal dream symbols and their meanings.

Symbols are the recurring visual/conceptual motifs that appear in
dreams. Each symbol has associations with emotions, themes, and
other symbols. The resonance system selects symbols that are
emotionally consonant with the dreamer's current state.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from dreamcore.utils.entropy import DreamEntropy


@dataclass
class Archetype:
    """A universal dream symbol with emotional associations."""

    name: str
    domain: str  # Broad category: "natural", "structural", "body", "abstract".
    emotional_resonance: dict[str, float] = field(default_factory=dict)
    related_symbols: list[str] = field(default_factory=list)
    description: str = ""

    @property
    def primary_emotion(self) -> str:
        if not self.emotional_resonance:
            return "neutral"
        return max(self.emotional_resonance, key=lambda k: self.emotional_resonance[k])

    def resonance_with(self, mood: dict[str, float]) -> float:
        """Compute how strongly this symbol resonates with a mood."""
        if not self.emotional_resonance or not mood:
            return 0.0
        score = 0.0
        for emotion, weight in self.emotional_resonance.items():
            mood_val = mood.get(emotion, 0.0)
            score += weight * mood_val
        return score

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "primary_emotion": self.primary_emotion,
            "resonance": self.emotional_resonance,
            "related": self.related_symbols,
        }


# Pre-defined archetype pool.
_ARCHETYPES = [
    Archetype("spiral", "abstract", {"curiosity": 0.7, "anxiety": 0.3}, ["vortex", "shell", "helix"], "the eternal descent into deeper understanding"),
    Archetype("mirror", "structural", {"curiosity": 0.5, "anxiety": 0.4}, ["reflection", "glass", "surface"], "confrontation with the self"),
    Archetype("key", "object", {"curiosity": 0.8, "excitement": 0.3}, ["door", "lock", "secret"], "access to hidden knowledge"),
    Archetype("door", "structural", {"curiosity": 0.6, "anxiety": 0.3}, ["key", "threshold", "passage"], "transition between states"),
    Archetype("water", "natural", {"serenity": 0.5, "sadness": 0.3}, ["ocean", "rain", "river"], "the unconscious mind"),
    Archetype("fire", "natural", {"anger": 0.4, "excitement": 0.5}, ["flame", "ash", "warmth"], "transformation and destruction"),
    Archetype("shadow", "abstract", {"anxiety": 0.6, "mischief": 0.3}, ["darkness", "hidden", "unknown"], "the rejected self"),
    Archetype("light", "natural", {"joy": 0.5, "serenity": 0.4}, ["sun", "glow", "illumination"], "consciousness and understanding"),
    Archetype("clock", "object", {"anxiety": 0.5, "sadness": 0.3}, ["time", "hands", "ticking"], "mortality and change"),
    Archetype("eye", "body", {"curiosity": 0.6, "anxiety": 0.4}, ["vision", "sight", "watching"], "awareness and judgment"),
    Archetype("thread", "object", {"affection": 0.5, "curiosity": 0.3}, ["web", "connection", "weaving"], "relationships and fate"),
    Archetype("bridge", "structural", {"curiosity": 0.4, "excitement": 0.3}, ["crossing", "connection", "gap"], "transition and communication"),
    Archetype("mask", "object", {"mischief": 0.5, "anxiety": 0.3}, ["face", "persona", "disguise"], "identity and deception"),
    Archetype("seed", "natural", {"joy": 0.3, "curiosity": 0.4}, ["growth", "potential", "beginning"], "unrealized possibility"),
    Archetype("shell", "natural", {"serenity": 0.4, "sadness": 0.2}, ["spiral", "protection", "ocean"], "memory and protection"),
    Archetype("feather", "natural", {"serenity": 0.4, "joy": 0.3}, ["flight", "lightness", "air"], "freedom and transcendence"),
    Archetype("bone", "body", {"anxiety": 0.3, "pride": 0.3}, ["skeleton", "structure", "foundation"], "fundamental truth"),
    Archetype("crystal", "natural", {"curiosity": 0.4, "serenity": 0.3}, ["clarity", "facet", "gem"], "compressed understanding"),
    Archetype("ink", "object", {"mischief": 0.4, "curiosity": 0.4}, ["writing", "stain", "expression"], "communication and concealment"),
    Archetype("echo", "abstract", {"sadness": 0.4, "curiosity": 0.3}, ["repetition", "memory", "sound"], "the persistence of the past"),
    Archetype("vortex", "abstract", {"anxiety": 0.5, "excitement": 0.4}, ["spiral", "pull", "center"], "overwhelming force"),
    Archetype("root", "natural", {"serenity": 0.3, "pride": 0.3}, ["tree", "foundation", "earth"], "origin and stability"),
    Archetype("constellation", "natural", {"curiosity": 0.5, "serenity": 0.3}, ["star", "pattern", "navigation"], "meaning found in chaos"),
    Archetype("labyrinth", "structural", {"anxiety": 0.4, "curiosity": 0.5}, ["maze", "path", "center"], "the journey of self-discovery"),
    Archetype("anvil", "object", {"pride": 0.4, "anger": 0.2}, ["forge", "hammer", "creation"], "will applied to material"),
    Archetype("web", "natural", {"mischief": 0.4, "curiosity": 0.3}, ["spider", "network", "trap"], "interconnection and strategy"),
    Archetype("fog", "natural", {"anxiety": 0.5, "serenity": 0.2}, ["mist", "uncertainty", "hidden"], "the unknown"),
    Archetype("tower", "structural", {"pride": 0.5, "anxiety": 0.3}, ["height", "isolation", "view"], "ambition and isolation"),
]


class ArchetypePool:
    """Registry of all available dream symbol archetypes."""

    def __init__(self) -> None:
        self._archetypes = {a.name: a for a in _ARCHETYPES}

    def get(self, name: str) -> Optional[Archetype]:
        return self._archetypes.get(name)

    def all(self) -> list[Archetype]:
        return list(self._archetypes.values())

    def by_domain(self, domain: str) -> list[Archetype]:
        return [a for a in self._archetypes.values() if a.domain == domain]

    def by_emotion(self, emotion: str, threshold: float = 0.3) -> list[Archetype]:
        return [
            a for a in self._archetypes.values()
            if a.emotional_resonance.get(emotion, 0.0) >= threshold
        ]


class SymbolResonance:
    """Selects symbols based on emotional resonance with current mood."""

    def __init__(self, pool: Optional[ArchetypePool] = None) -> None:
        self._pool = pool or ArchetypePool()

    def select(
        self,
        mood: dict[str, float],
        topics: list[str],
        count: int = 5,
    ) -> list[str]:
        """Select symbols that resonate with the current mood and topics."""
        candidates = self._pool.all()

        # Score each archetype.
        scored: list[tuple[Archetype, float]] = []
        for arch in candidates:
            score = arch.resonance_with(mood)

            # Boost if archetype name or related symbols match topics.
            topic_set = set(t.lower() for t in topics)
            related_set = set(s.lower() for s in [arch.name] + arch.related_symbols)
            if topic_set & related_set:
                score += 0.3

            scored.append((arch, score))

        # Sort by score and take top N.
        scored.sort(key=lambda x: x[1], reverse=True)
        return [a.name for a, _ in scored[:count]]

    def explain(self, symbol: str) -> str:
        """Get the meaning of a dream symbol."""
        arch = self._pool.get(symbol)
        if arch:
            return f"{arch.name}: {arch.description} (domain: {arch.domain}, primary: {arch.primary_emotion})"
        return f"{symbol}: unknown symbol"
