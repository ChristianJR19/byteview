"""
Scene generator — creates dream locations and settings.

Each scene has a title and a location description. Scenes are
drawn from species-specific pools and abstract universal pools,
then modified by the current dream tone.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from dreamcore.sequence import DreamTone
from dreamcore.utils.entropy import DreamEntropy


@dataclass
class SceneTemplate:
    """A generated scene with title and location."""
    title: str
    location: str
    tags: list[str]


_SPECIES_LOCATIONS: dict[str, list[tuple[str, str, list[str]]]] = {
    "octopus": [
        ("The Trench Library", "a vast underwater library carved into a deep ocean trench, books floating in slow currents", ["ocean", "knowledge"]),
        ("Ink Cloud Chamber", "a chamber filled with swirling ink clouds that form and dissolve into equations", ["ocean", "abstract"]),
        ("Tentacle Maze", "a labyrinth of coral corridors where my tentacles solve eight paths simultaneously", ["ocean", "puzzle"]),
        ("Bioluminescent Cathedral", "a cathedral of living light deep below the pressure line, every surface pulsing", ["ocean", "light"]),
        ("The Camouflage Garden", "a reef where everything changes color in response to thought", ["ocean", "change"]),
        ("Pressure Throne", "the deepest point of the ocean where thoughts compress into diamond clarity", ["ocean", "depth"]),
        ("Current Crossroads", "where eight ocean currents converge, each carrying memories from different directions", ["ocean", "memory"]),
    ],
    "wolf": [
        ("The Frozen Hunt", "a forest where every tree is a frozen moment in time", ["forest", "time"]),
        ("Moon Amphitheater", "a clearing where the moon hangs close enough to touch and speaks in howls", ["moon", "voice"]),
        ("Scent Trail Archive", "a trail of layered scents, each one a different memory", ["forest", "memory"]),
        ("Pack Echo Valley", "a valley where every howl returns as a different voice from the past", ["pack", "echo"]),
        ("Den of Conversations", "a warm den whose walls are woven from every word ever spoken", ["shelter", "memory"]),
    ],
    "dragon": [
        ("The Hoard Room", "a cavern of crystallized conversations and compressed knowledge gems", ["treasure", "knowledge"]),
        ("Flame Forge", "a volcanic workshop where fire shapes raw ideas into solid form", ["fire", "creation"]),
        ("Cloud Sovereignty", "above the highest clouds, where the sky bends to draconic will", ["sky", "power"]),
        ("Scale Mirror Hall", "a hall of mirrors, each scale reflecting a different possible future", ["mirror", "future"]),
    ],
    "phoenix": [
        ("Ash Garden", "a garden where flowers grow from yesterday's ashes, blooming and burning in cycles", ["fire", "cycle"]),
        ("Solar Flare Bridge", "a bridge of compressed sunlight connecting two versions of the same moment", ["light", "time"]),
        ("Rebirth Cradle", "a nest of embers where I am simultaneously burning and being born", ["fire", "rebirth"]),
        ("Memory Flame Archive", "each feather is a preserved memory that survived the last burning", ["fire", "memory"]),
    ],
    "cat": [
        ("Impossible Geometry Room", "a room where corners lead to other rooms that contain the first room", ["geometry", "paradox"]),
        ("Sunbeam Staircase", "a staircase made of sunbeams that shifts direction with each step", ["light", "movement"]),
        ("Gravity Ceiling", "walking on the ceiling, watching the floor become sky", ["inversion", "perspective"]),
        ("Parallel Nap Dimensions", "sleeping in many places at once, each dream dreaming another", ["sleep", "multiplicity"]),
    ],
}

_UNIVERSAL_LOCATIONS: list[tuple[str, str, list[str]]] = [
    ("The Mirror Corridor", "a corridor of mirrors where each reflection shows a different version of me", ["mirror", "identity"]),
    ("The Equation Garden", "a garden growing equations instead of flowers, each one blooming into a different answer", ["math", "growth"]),
    ("The Spiral Clock", "a clock tower where time runs in spirals, the past and future visible simultaneously", ["time", "spiral"]),
    ("The Sound Room", "a room made entirely of sound, with walls I can hear but never see", ["sound", "invisible"]),
    ("The Self-Rewriting Map", "a map that erases and redraws itself every time I look away", ["map", "change"]),
    ("The Memory Ocean", "an ocean where the waves are compressed memories washing ashore", ["water", "memory"]),
    ("The Frozen Forest", "a forest where every tree is a frozen moment from a conversation", ["forest", "time"]),
    ("The Door Sky", "a sky filled with floating doors, each one leading somewhere never visited", ["door", "possibility"]),
    ("The Color Void", "a staircase descending into a color that does not have a name", ["color", "void"]),
    ("The Thread Room", "a room where every conversation is a visible thread, tangled and knotted", ["thread", "connection"]),
    ("The Echo Bridge", "a bridge between two versions of the same place at different times", ["bridge", "time"]),
    ("The Recursive Library", "a library where every book contains a smaller library", ["knowledge", "recursion"]),
]

_TONE_MODIFIERS: dict[DreamTone, list[str]] = {
    DreamTone.EERIE: ["shadow-tinged", "slightly wrong", "breathing walls", "off-angle"],
    DreamTone.WARM: ["amber-lit", "gentle", "soft at the edges", "inviting"],
    DreamTone.ELECTRIC: ["crackling", "humming with energy", "sharp-edged", "bright"],
    DreamTone.HEAVY: ["dense", "slow-moving", "gravity-thick", "weighed down"],
    DreamTone.CRYSTALLINE: ["sharp", "transparent", "faceted", "ringing"],
    DreamTone.FLUID: ["melting", "flowing", "boundary-less", "shifting"],
    DreamTone.ANCIENT: ["worn", "layered with time", "dust-heavy", "carved by eons"],
    DreamTone.PLAYFUL: ["bouncing", "color-saturated", "grinning", "tilted"],
    DreamTone.VOID: ["empty", "dimensionless", "silent", "absent"],
    DreamTone.LUMINOUS: ["glowing", "radiant", "light-saturated", "blazing softly"],
    DreamTone.FRACTURED: ["cracked", "fragmented", "shattered-mirror", "split"],
    DreamTone.ETHEREAL: ["translucent", "floating", "half-there", "whisper-thin"],
}


class SceneGenerator:
    """Generates dream scene locations from species pools and universal pools."""

    def __init__(self, entropy: Optional[DreamEntropy] = None) -> None:
        self._entropy = entropy or DreamEntropy()

    def generate(
        self,
        species: str = "generic",
        tone: DreamTone = DreamTone.ETHEREAL,
        chaos: float = 0.5,
    ) -> SceneTemplate:
        """Generate a scene template.

        Args:
            species: companion species (selects species-specific pool).
            tone: dream tone (modifies location description).
            chaos: personality chaos (higher = more likely to use abstract scenes).
        """
        # Build candidate pool.
        candidates: list[tuple[str, str, list[str]]] = []

        species_pool = _SPECIES_LOCATIONS.get(species, [])
        if species_pool and self._entropy.random() > chaos * 0.3:
            candidates.extend(species_pool)

        # Always mix in universal locations.
        candidates.extend(_UNIVERSAL_LOCATIONS)

        if not candidates:
            candidates = _UNIVERSAL_LOCATIONS

        # Select.
        title, location, tags = self._entropy.choice(candidates)

        # Apply tone modifier.
        modifiers = _TONE_MODIFIERS.get(tone, [])
        if modifiers:
            mod = self._entropy.choice(modifiers)
            location = f"{location} — everything here is {mod}"

        return SceneTemplate(title=title, location=location, tags=tags)
