"""
grok-dreamcore — surreal dream sequence engine.

Generates procedural narrative dream sequences from emotional state,
memory anchors, and symbolic archetypes. Built for integration with
LLM companion systems. Powers the /dream command infrastructure.

Usage:
    from dreamcore import DreamEngine, EmotionalContext, DreamConfig

    engine = DreamEngine(config=DreamConfig(depth=4, style="surreal"))
    context = EmotionalContext(
        mood={"curiosity": 0.8, "serenity": 0.4},
        recent_topics=["ocean", "puzzles", "old conversations"],
    )
    sequence = engine.generate(context)
    print(sequence.narrate())
"""

__version__ = "0.6.0"

from dreamcore.engine import DreamEngine, DreamConfig
from dreamcore.sequence import DreamSequence, DreamFragment, DreamFrame
from dreamcore.memory.anchors import MemoryAnchor, AnchorSet
from dreamcore.symbols.archetypes import Archetype, ArchetypePool

__all__ = [
    "DreamEngine",
    "DreamConfig",
    "DreamSequence",
    "DreamFragment",
    "DreamFrame",
    "MemoryAnchor",
    "AnchorSet",
    "Archetype",
    "ArchetypePool",
]
