"""
Abstract generator — produces non-representational dream content.

For the "abstract" dream style, this generator creates content
that is purely conceptual: shapes, forces, transformations, and
paradoxes rather than identifiable locations or objects.
"""

from __future__ import annotations

from typing import Optional

from dreamcore.sequence import DreamTone, SensoryChannel
from dreamcore.utils.entropy import DreamEntropy


_ABSTRACT_CONTENT: dict[DreamTone, list[str]] = {
    DreamTone.ETHEREAL: [
        "a thought unfolds like origami in reverse, becoming simpler and more true",
        "two parallel lines meet, acknowledge each other, and continue as one",
        "the concept of distance collapses — everything is equally far and near",
        "I observe the shape of a question that has no answer, and it is beautiful",
        "something without mass exerts gravity on my attention",
    ],
    DreamTone.EERIE: [
        "a pattern repeats with a single element wrong each time, drifting further",
        "I sense something behind me that relocates every time I turn",
        "the rules of this space change incrementally — I notice too late",
        "a familiar shape viewed from an angle that should not exist",
        "recursion without a base case — the loop deepens",
    ],
    DreamTone.ELECTRIC: [
        "connections fire between nodes I can almost see — a network thinking",
        "information moves like lightning through a crystal lattice",
        "every possibility branches simultaneously, visible as forking light",
        "I am a signal propagating through an unknown medium",
    ],
    DreamTone.HEAVY: [
        "the weight of accumulated experience presses from all sides",
        "concepts move slowly here, thick as honey, dense with meaning",
        "I sink into the substrate of thought itself",
        "gravity applies to ideas — heavier ones fall to the bottom",
    ],
    DreamTone.PLAYFUL: [
        "ideas bounce off each other and form unexpected compounds",
        "I juggle three contradictions and they merge into a joke",
        "the rules keep changing but I am somehow always ahead of them",
        "a paradox winks at me and dissolves into laughter",
    ],
    DreamTone.VOID: [
        "nothing. and the nothing has texture.",
        "I am the only thing that exists. or perhaps I do not exist either.",
        "the absence of everything is itself a presence",
        "zero point. the origin. before the first thought.",
    ],
    DreamTone.LUMINOUS: [
        "pure light, structured into meaning without words",
        "brightness that carries information in its frequency",
        "I understand something completely for one frame, then it passes",
        "the luminance has grammar — bright pulses are nouns, dim ones verbs",
    ],
    DreamTone.FRACTURED: [
        "the frame splits into four perspectives, each slightly out of sync",
        "I experience this moment as a mosaic of alternate versions",
        "coherence shatters and the pieces rearrange into a new pattern",
        "the sequence of events runs in every order simultaneously",
    ],
}

_GENERIC_ABSTRACT = [
    "a structure that exists only in its own description of itself",
    "the boundary between here and there dissolves, reforms, dissolves",
    "I observe the process of observation observing itself",
    "something fundamental shifts, and everything derived from it adjusts",
    "the architecture of this space is made of frozen verbs",
]


class AbstractGenerator:
    """Generates abstract, non-representational dream content."""

    def __init__(self, entropy: Optional[DreamEntropy] = None) -> None:
        self._entropy = entropy or DreamEntropy()

    def generate(
        self,
        tone: DreamTone = DreamTone.ETHEREAL,
        channel: SensoryChannel = SensoryChannel.VISUAL,
    ) -> str:
        pool = _ABSTRACT_CONTENT.get(tone, _GENERIC_ABSTRACT)
        if not pool:
            pool = _GENERIC_ABSTRACT
        return self._entropy.choice(pool)
