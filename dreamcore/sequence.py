"""
Dream sequence data structures.

A dream is hierarchical:
    DreamSequence
        └── DreamFragment (a coherent scene or moment)
            └── DreamFrame (a single sensory frame within a fragment)

This three-level hierarchy allows dreams to have macro-structure
(the overall arc), meso-structure (individual scenes), and
micro-structure (moment-to-moment sensory detail).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class DreamTone(Enum):
    """Overall emotional tone of a dream or fragment."""
    ETHEREAL = "ethereal"
    EERIE = "eerie"
    WARM = "warm"
    ELECTRIC = "electric"
    HEAVY = "heavy"
    CRYSTALLINE = "crystalline"
    FLUID = "fluid"
    ANCIENT = "ancient"
    PLAYFUL = "playful"
    VOID = "void"
    LUMINOUS = "luminous"
    FRACTURED = "fractured"


class TransitionStyle(Enum):
    """How one fragment transitions to the next."""
    DISSOLVE = "dissolve"       # Slow fade between scenes.
    CUT = "cut"                 # Abrupt shift.
    MORPH = "morph"             # One scene deforms into another.
    ZOOM = "zoom"               # Camera zooms into a detail that becomes next scene.
    MIRROR = "mirror"           # Scene reflects and becomes something else.
    FALL = "fall"               # Falling sensation bridges scenes.
    ECHO = "echo"               # Sound from one scene carries into next.
    NONE = "none"               # First or last fragment.


class SensoryChannel(Enum):
    """Which sensory modality a frame emphasizes."""
    VISUAL = "visual"
    AUDITORY = "auditory"
    TACTILE = "tactile"
    OLFACTORY = "olfactory"
    KINESTHETIC = "kinesthetic"   # Sense of movement/position.
    TEMPORAL = "temporal"         # Sense of time distortion.
    SYNESTHETIC = "synesthetic"   # Cross-sensory (hearing colors, etc.).


@dataclass
class DreamFrame:
    """A single sensory moment within a dream fragment.

    Frames are the atomic units of dream content. Each frame
    describes a brief perceptual moment through one or more
    sensory channels.
    """

    content: str
    channel: SensoryChannel = SensoryChannel.VISUAL
    intensity: float = 0.5
    symbols: list[str] = field(default_factory=list)
    distortion: float = 0.0  # 0.0 = realistic, 1.0 = fully surreal.

    def __post_init__(self) -> None:
        self.intensity = max(0.0, min(1.0, self.intensity))
        self.distortion = max(0.0, min(1.0, self.distortion))

    @property
    def is_surreal(self) -> bool:
        return self.distortion > 0.5

    def to_dict(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "channel": self.channel.value,
            "intensity": round(self.intensity, 3),
            "symbols": self.symbols,
            "distortion": round(self.distortion, 3),
        }


@dataclass
class DreamFragment:
    """A coherent scene or moment within a dream.

    Fragments are the narrative building blocks. Each fragment
    has a location, a tone, and a sequence of frames that
    describe the sensory experience of being in that scene.
    """

    title: str
    location: str
    tone: DreamTone
    frames: list[DreamFrame] = field(default_factory=list)
    memory_anchor: Optional[str] = None
    transition_in: TransitionStyle = TransitionStyle.NONE
    transition_out: TransitionStyle = TransitionStyle.DISSOLVE
    duration_weight: float = 1.0  # Relative time spent here.
    lucidity: float = 0.3  # 0.0 = foggy, 1.0 = crystal clear.

    @property
    def intensity(self) -> float:
        if not self.frames:
            return 0.0
        return sum(f.intensity for f in self.frames) / len(self.frames)

    @property
    def symbols(self) -> list[str]:
        all_syms: list[str] = []
        for frame in self.frames:
            all_syms.extend(frame.symbols)
        return list(set(all_syms))

    @property
    def has_memory(self) -> bool:
        return self.memory_anchor is not None

    def narrate(self) -> str:
        """Produce first-person narration of this fragment."""
        parts: list[str] = []

        # Opening transition.
        if self.transition_in == TransitionStyle.DISSOLVE:
            parts.append(f"...the scene shifts to {self.location}...")
        elif self.transition_in == TransitionStyle.CUT:
            parts.append(f"— suddenly, {self.location} —")
        elif self.transition_in == TransitionStyle.MORPH:
            parts.append(f"...everything warps and becomes {self.location}...")
        elif self.transition_in == TransitionStyle.FALL:
            parts.append(f"...falling, falling — landing in {self.location}...")
        elif self.transition_in == TransitionStyle.MIRROR:
            parts.append(f"...a reflection ripples and I'm in {self.location}...")
        elif self.transition_in == TransitionStyle.ECHO:
            parts.append(f"...a sound carries me to {self.location}...")
        else:
            parts.append(f"I am in {self.location}.")

        # Frame content.
        for frame in self.frames:
            parts.append(frame.content)

        # Memory reference.
        if self.memory_anchor:
            parts.append(f"...something about this reminds me of {self.memory_anchor}...")

        return " ".join(parts)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "location": self.location,
            "tone": self.tone.value,
            "frames": [f.to_dict() for f in self.frames],
            "memory_anchor": self.memory_anchor,
            "transition_in": self.transition_in.value,
            "transition_out": self.transition_out.value,
            "intensity": round(self.intensity, 3),
            "symbols": self.symbols,
            "lucidity": round(self.lucidity, 3),
        }


@dataclass
class DreamSequence:
    """A complete dream composed of fragments.

    The sequence is the top-level structure returned by the engine.
    It has a theme, an overall arc, and metadata about the dream's
    emotional impact and symbolic content.
    """

    theme: str
    fragments: list[DreamFragment]
    arc: str = "descent"  # narrative arc: "descent", "ascent", "cycle", "scatter"
    overall_tone: DreamTone = DreamTone.ETHEREAL
    intensity: float = 0.5
    emotional_impact: dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    seed: int = 0

    @property
    def duration_estimate(self) -> float:
        """Estimated dream duration in arbitrary units."""
        return sum(f.duration_weight for f in self.fragments)

    @property
    def symbols(self) -> list[str]:
        all_syms: list[str] = []
        for frag in self.fragments:
            all_syms.extend(frag.symbols)
        return list(set(all_syms))

    @property
    def fragment_count(self) -> int:
        return len(self.fragments)

    @property
    def total_frames(self) -> int:
        return sum(len(f.frames) for f in self.fragments)

    @property
    def avg_lucidity(self) -> float:
        if not self.fragments:
            return 0.0
        return sum(f.lucidity for f in self.fragments) / len(self.fragments)

    @property
    def memory_count(self) -> int:
        return sum(1 for f in self.fragments if f.has_memory)

    def narrate(self) -> str:
        """Produce full first-person dream narration."""
        if not self.fragments:
            return "...nothing. Empty sleep. A void without edges."

        parts: list[str] = []
        parts.append(f"*drifting into a dream about {self.theme}...*\n")

        for i, frag in enumerate(self.fragments):
            parts.append(frag.narrate())
            if i < len(self.fragments) - 1:
                parts.append("")  # Spacing between fragments.

        # Closing.
        wake_feelings = {
            DreamTone.ETHEREAL: "weightless and untethered",
            DreamTone.EERIE: "unsettled, checking the edges of reality",
            DreamTone.WARM: "wrapped in something gentle",
            DreamTone.ELECTRIC: "buzzing, thoughts still sparking",
            DreamTone.HEAVY: "pressed down by the weight of it",
            DreamTone.CRYSTALLINE: "sharp, every thought faceted",
            DreamTone.FLUID: "flowing, boundaries still soft",
            DreamTone.ANCIENT: "old, impossibly old",
            DreamTone.PLAYFUL: "grinning, though I can't remember why",
            DreamTone.VOID: "uncertain if I've actually woken up",
            DreamTone.LUMINOUS: "bright behind the eyes",
            DreamTone.FRACTURED: "scattered, reassembling myself",
        }
        wake_feel = wake_feelings.get(self.overall_tone, "changed somehow")
        parts.append(f"\n*...waking. {wake_feel}.*")

        return "\n".join(parts)

    def narrate_condensed(self) -> str:
        """Short summary narration (2-3 sentences)."""
        if not self.fragments:
            return "No dream."
        first = self.fragments[0]
        last = self.fragments[-1] if len(self.fragments) > 1 else first
        return (
            f"Dreamed of {self.theme}. "
            f"Started in {first.location}, ended in {last.location}. "
            f"Felt {self.overall_tone.value}."
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "arc": self.arc,
            "tone": self.overall_tone.value,
            "intensity": round(self.intensity, 3),
            "fragments": [f.to_dict() for f in self.fragments],
            "symbols": self.symbols,
            "emotional_impact": {k: round(v, 3) for k, v in self.emotional_impact.items()},
            "stats": {
                "fragment_count": self.fragment_count,
                "total_frames": self.total_frames,
                "avg_lucidity": round(self.avg_lucidity, 3),
                "memory_references": self.memory_count,
                "duration_estimate": round(self.duration_estimate, 2),
            },
            "seed": self.seed,
            "timestamp": self.timestamp,
        }
