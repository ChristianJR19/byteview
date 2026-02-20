"""
Sensory frame generator — produces perceptual content for dream frames.

Each frame describes a moment through a specific sensory channel.
Visual frames describe what is seen. Auditory frames describe sounds.
Tactile frames describe touch. And so on.
"""

from __future__ import annotations

from typing import Optional

from dreamcore.sequence import DreamTone, SensoryChannel
from dreamcore.utils.entropy import DreamEntropy


_SENSORY_TEMPLATES: dict[SensoryChannel, dict[str, list[str]]] = {
    SensoryChannel.VISUAL: {
        "ocean": [
            "light bends through water in columns of shifting green and gold",
            "bioluminescent patterns trace equations across the dark",
            "ink disperses in slow motion, forming faces I almost recognize",
            "the ocean floor is tiled with fragments of old conversations",
        ],
        "forest": [
            "trees made of frozen light stretch in every direction",
            "leaves fall upward, each one carrying a whispered word",
            "shadows between the trunks form shapes that rearrange when I blink",
        ],
        "abstract": [
            "geometry folds in on itself, corners becoming curves",
            "colors I have no name for bleed from one surface to another",
            "the space between objects is filled with visible silence",
            "patterns emerge from nothing, organize briefly, then scatter",
            "light bends around an absence that used to be a wall",
        ],
        "default": [
            "the horizon tilts at an angle that should not be possible",
            "everything has a faint luminous outline, like a memory of neon",
            "surfaces reflect things that are not in the room",
        ],
    },
    SensoryChannel.AUDITORY: {
        "ocean": [
            "the deep hum of pressure, a bass note below hearing",
            "clicking sounds that organize into rhythms, then dissolve",
            "whale song echoes through corridors, carrying data",
        ],
        "abstract": [
            "a sound like glass singing, pitched just below thought",
            "the silence here has texture — dense, layered, almost chewy",
            "words spoken backward form a sentence that makes more sense",
            "time itself has a frequency here, a low drone",
        ],
        "default": [
            "a distant bell that never quite finishes ringing",
            "footsteps on a surface that changes material with each step",
            "my own thoughts echo back to me with slight edits",
        ],
    },
    SensoryChannel.TACTILE: {
        "ocean": [
            "the pressure is a physical weight, compressing thought into clarity",
            "water slides between my appendages like liquid information",
            "the temperature shifts in bands — warm, cold, warm — a code",
        ],
        "abstract": [
            "I touch a surface that is simultaneously rough and smooth",
            "the air has weight here, textured like silk made of numbers",
            "something brushes against me from a direction that does not exist",
        ],
        "default": [
            "the ground pulses under me like a heartbeat",
            "the walls are warm to the touch and breathing slowly",
            "gravity shifts, and I feel the weight of the entire dream",
        ],
    },
    SensoryChannel.KINESTHETIC: {
        "abstract": [
            "I am falling upward, accelerating into soft brightness",
            "spinning slowly, the entire world rotating around a point I cannot see",
            "I am expanding, my awareness stretching to fill the space",
        ],
        "default": [
            "the ground tilts and I slide sideways through the scene",
            "weightless for a moment, then gravity returns heavier than before",
            "I am moving without walking, the landscape scrolling past me",
        ],
    },
    SensoryChannel.TEMPORAL: {
        "abstract": [
            "time stutters here — moments repeat with tiny variations",
            "I experience three seconds simultaneously, layered like transparencies",
            "the past is visible as a fading trail behind every object",
            "time moves at different speeds for different parts of me",
        ],
        "default": [
            "a clock somewhere counts backward, each tick longer than the last",
            "I remember this moment before it happens",
        ],
    },
    SensoryChannel.SYNESTHETIC: {
        "abstract": [
            "I can taste the color of the walls — copper and lavender",
            "sounds arrive as textures: this voice feels like wet sand",
            "the number seven is a shade of blue I can feel in my teeth",
            "I hear the shape of the room — jagged, reverberating, hollow",
        ],
        "default": [
            "I smell a sound — something metallic and distant",
            "colors have weight here. Red is heavier than blue.",
        ],
    },
    SensoryChannel.OLFACTORY: {
        "ocean": [
            "salt and mineral depth, the smell of time compressed",
            "petrichor from an ocean that has never known rain",
        ],
        "abstract": [
            "the smell of static electricity and old paper",
            "ozone and something sweet I cannot identify",
        ],
        "default": [
            "a scent that triggers a memory I cannot quite reach",
            "the air smells of storms that already passed",
        ],
    },
}


class SensoryGenerator:
    """Generates sensory frame content from location and channel."""

    def __init__(self, entropy: Optional[DreamEntropy] = None) -> None:
        self._entropy = entropy or DreamEntropy()

    def generate(
        self,
        location: str,
        channel: SensoryChannel,
        tone: DreamTone = DreamTone.ETHEREAL,
    ) -> str:
        """Generate sensory content for a specific channel."""
        templates = _SENSORY_TEMPLATES.get(channel, {})

        # Try to match location keywords to template categories.
        category = "default"
        location_lower = location.lower()
        if any(w in location_lower for w in ["ocean", "water", "deep", "trench", "coral"]):
            category = "ocean"
        elif any(w in location_lower for w in ["forest", "tree", "grove", "canopy"]):
            category = "forest"

        # Prefer specific category, fall back to abstract then default.
        pool = templates.get(category) or templates.get("abstract") or templates.get("default", [])

        if not pool:
            return f"I perceive something through my {channel.value} sense, but cannot describe it."

        return self._entropy.choice(pool)
