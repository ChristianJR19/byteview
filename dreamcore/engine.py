"""
Dream engine — the core orchestrator.

The engine takes an emotional context and produces a complete
DreamSequence. It coordinates scene generation, symbol selection,
memory anchoring, sensory frame composition, and narrative arc
construction.

The generation pipeline:
    1. Select dream arc (descent, ascent, cycle, scatter).
    2. Determine fragment count from depth config.
    3. For each fragment:
        a. Select location from generator pool.
        b. Apply symbolic resonance from emotional context.
        c. Generate sensory frames for the location.
        d. Optionally anchor a memory reference.
        e. Determine transition style.
    4. Compute overall tone from fragment tones.
    5. Compute emotional impact (how the dream shifts mood).
    6. Assemble into DreamSequence.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from typing import Any, Optional

from dreamcore.sequence import (
    DreamSequence,
    DreamFragment,
    DreamFrame,
    DreamTone,
    TransitionStyle,
    SensoryChannel,
)
from dreamcore.generators.scene import SceneGenerator, SceneTemplate
from dreamcore.generators.sensory import SensoryGenerator
from dreamcore.generators.abstract import AbstractGenerator
from dreamcore.memory.anchors import MemoryAnchor, AnchorSet
from dreamcore.memory.consolidation import ConsolidationEngine
from dreamcore.symbols.archetypes import ArchetypePool
from dreamcore.symbols.resonance import SymbolResonance
from dreamcore.utils.entropy import DreamEntropy
from dreamcore.utils.timing import PacingCurve, ArcType


@dataclass
class EmotionalContext:
    """Input emotional state that shapes the dream.

    Attributes:
        mood: dict of emotion dimensions and their intensities (0.0-1.0).
        recent_topics: list of topics from recent interactions.
        memory_fragments: optional memory text snippets to anchor.
        companion_species: species of the companion (shapes scene pool).
        personality_chaos: how chaotic the companion's personality is.
        bond_strength: strength of bond with user (0.0-1.0).
    """

    mood: dict[str, float] = field(default_factory=dict)
    recent_topics: list[str] = field(default_factory=list)
    memory_fragments: list[str] = field(default_factory=list)
    companion_species: str = "generic"
    personality_chaos: float = 0.5
    bond_strength: float = 0.3

    @property
    def dominant_emotion(self) -> str:
        if not self.mood:
            return "neutral"
        return max(self.mood, key=lambda k: self.mood[k])

    @property
    def emotional_intensity(self) -> float:
        if not self.mood:
            return 0.0
        vals = list(self.mood.values())
        return (sum(v ** 2 for v in vals) / len(vals)) ** 0.5


@dataclass
class DreamConfig:
    """Configuration for dream generation.

    Attributes:
        depth: number of fragments (1-7). More = longer dream.
        frames_per_fragment: sensory frames per scene (2-6).
        style: generation style ("surreal", "narrative", "abstract", "lucid").
        memory_probability: chance of anchoring a memory per fragment.
        distortion_base: base level of surreal distortion (0.0-1.0).
        symbol_density: how many symbols per fragment (1-5).
        sensory_diversity: prefer varied sensory channels (0.0-1.0).
        arc_type: narrative arc ("auto", "descent", "ascent", "cycle", "scatter").
    """

    depth: int = 4
    frames_per_fragment: int = 3
    style: str = "surreal"
    memory_probability: float = 0.35
    distortion_base: float = 0.3
    symbol_density: int = 2
    sensory_diversity: float = 0.6
    arc_type: str = "auto"

    def validate(self) -> None:
        if not 1 <= self.depth <= 7:
            raise ValueError("depth must be 1-7")
        if not 2 <= self.frames_per_fragment <= 6:
            raise ValueError("frames_per_fragment must be 2-6")
        if self.style not in ("surreal", "narrative", "abstract", "lucid"):
            raise ValueError("style must be surreal/narrative/abstract/lucid")


class DreamEngine:
    """Main dream generation engine.

    Usage:
        engine = DreamEngine(config=DreamConfig(depth=4))
        context = EmotionalContext(mood={"curiosity": 0.8})
        sequence = engine.generate(context)
        print(sequence.narrate())
    """

    def __init__(
        self,
        config: Optional[DreamConfig] = None,
        seed: Optional[int] = None,
    ) -> None:
        self._config = config or DreamConfig()
        self._config.validate()
        self._entropy = DreamEntropy(seed=seed)

        # Sub-engines.
        self._scene_gen = SceneGenerator(entropy=self._entropy)
        self._sensory_gen = SensoryGenerator(entropy=self._entropy)
        self._abstract_gen = AbstractGenerator(entropy=self._entropy)
        self._archetype_pool = ArchetypePool()
        self._resonance = SymbolResonance(pool=self._archetype_pool)
        self._consolidation = ConsolidationEngine()
        self._pacing = PacingCurve()

    @property
    def config(self) -> DreamConfig:
        return self._config

    def generate(
        self,
        context: EmotionalContext,
        provider: Any = None,
    ) -> DreamSequence:
        """Generate a complete dream sequence from emotional context.

        Args:
            context: the emotional and memory state driving the dream.
            provider: optional LLM provider for enhanced narration.

        Returns:
            A complete DreamSequence ready for narration.
        """
        # 1. Determine arc type.
        arc = self._select_arc(context)

        # 2. Select theme from context.
        theme = self._derive_theme(context)

        # 3. Compute overall tone from mood.
        overall_tone = self._mood_to_tone(context)

        # 4. Build memory anchor set.
        anchors = self._build_anchors(context)

        # 5. Select symbols via resonance.
        symbols = self._resonance.select(
            mood=context.mood,
            topics=context.recent_topics,
            count=self._config.symbol_density * self._config.depth,
        )

        # 6. Generate fragments.
        fragments = self._generate_fragments(
            context=context,
            arc=arc,
            tone=overall_tone,
            anchors=anchors,
            symbols=symbols,
        )

        # 7. Compute emotional impact.
        impact = self._compute_impact(context, fragments, overall_tone)

        # 8. Compute intensity.
        intensity = self._compute_intensity(context, fragments)

        return DreamSequence(
            theme=theme,
            fragments=fragments,
            arc=arc.value,
            overall_tone=overall_tone,
            intensity=intensity,
            emotional_impact=impact,
            seed=self._entropy.seed,
        )

    def generate_fragment(
        self,
        context: EmotionalContext,
        tone: DreamTone,
        position: float,
    ) -> DreamFragment:
        """Generate a single dream fragment.

        Useful for streaming dream generation where fragments are
        produced one at a time.

        Args:
            context: emotional context.
            tone: desired tone.
            position: 0.0-1.0 position in the dream arc.
        """
        scene = self._scene_gen.generate(
            species=context.companion_species,
            tone=tone,
            chaos=context.personality_chaos,
        )

        frames = self._generate_frames(
            scene=scene,
            tone=tone,
            position=position,
            context=context,
        )

        # Memory anchor.
        memory_ref = None
        if (
            context.memory_fragments
            and self._entropy.random() < self._config.memory_probability
        ):
            memory_ref = self._entropy.choice(context.memory_fragments)

        return DreamFragment(
            title=scene.title,
            location=scene.location,
            tone=tone,
            frames=frames,
            memory_anchor=memory_ref,
            lucidity=self._compute_lucidity(position, context),
        )

    # ------------------------------------------------------------------
    # Private pipeline methods
    # ------------------------------------------------------------------

    def _select_arc(self, context: EmotionalContext) -> ArcType:
        """Select narrative arc from context."""
        if self._config.arc_type != "auto":
            return ArcType(self._config.arc_type)

        dominant = context.dominant_emotion
        arc_map = {
            "anxiety": ArcType.DESCENT,
            "sadness": ArcType.DESCENT,
            "curiosity": ArcType.ASCENT,
            "excitement": ArcType.ASCENT,
            "joy": ArcType.CYCLE,
            "serenity": ArcType.CYCLE,
            "mischief": ArcType.SCATTER,
            "anger": ArcType.SCATTER,
        }
        return arc_map.get(dominant, ArcType.CYCLE)

    def _derive_theme(self, context: EmotionalContext) -> str:
        """Derive a dream theme from context."""
        # Combine topics and mood into theme candidates.
        theme_seeds: list[str] = []

        if context.recent_topics:
            theme_seeds.extend(context.recent_topics[:3])

        mood_themes = {
            "curiosity": ["hidden passages", "unopened doors", "ancient texts"],
            "anxiety": ["endless corridors", "dissolving ground", "approaching storms"],
            "joy": ["sunlit gardens", "floating islands", "golden light"],
            "sadness": ["empty rooms", "fading photographs", "distant shores"],
            "mischief": ["trick boxes", "shapeshifting objects", "carnival mirrors"],
            "serenity": ["still water", "mountain peaks", "star fields"],
            "excitement": ["racing currents", "lightning paths", "opening horizons"],
            "affection": ["warm hearths", "intertwined paths", "shared silence"],
            "pride": ["tall towers", "polished surfaces", "crowns of light"],
            "anger": ["volcanic cracks", "shattering glass", "burning archives"],
        }

        dominant = context.dominant_emotion
        if dominant in mood_themes:
            theme_seeds.extend(mood_themes[dominant])

        if not theme_seeds:
            theme_seeds = ["shifting landscapes", "abstract forms"]

        return self._entropy.choice(theme_seeds)

    def _mood_to_tone(self, context: EmotionalContext) -> DreamTone:
        """Map dominant mood to dream tone."""
        tone_map: dict[str, DreamTone] = {
            "curiosity": DreamTone.ELECTRIC,
            "anxiety": DreamTone.EERIE,
            "joy": DreamTone.LUMINOUS,
            "sadness": DreamTone.HEAVY,
            "mischief": DreamTone.PLAYFUL,
            "serenity": DreamTone.ETHEREAL,
            "excitement": DreamTone.ELECTRIC,
            "affection": DreamTone.WARM,
            "pride": DreamTone.CRYSTALLINE,
            "anger": DreamTone.FRACTURED,
        }
        return tone_map.get(context.dominant_emotion, DreamTone.ETHEREAL)

    def _build_anchors(self, context: EmotionalContext) -> AnchorSet:
        """Build memory anchors from context."""
        anchors = AnchorSet()
        for fragment in context.memory_fragments:
            anchor = MemoryAnchor(
                content=fragment,
                salience=0.5 + self._entropy.random() * 0.3,
                emotional_weight=context.emotional_intensity,
            )
            anchors.add(anchor)
        return anchors

    def _generate_fragments(
        self,
        context: EmotionalContext,
        arc: ArcType,
        tone: DreamTone,
        anchors: AnchorSet,
        symbols: list[str],
    ) -> list[DreamFragment]:
        """Generate all fragments for the dream."""
        fragments: list[DreamFragment] = []
        depth = self._config.depth
        pacing = self._pacing.compute(arc, depth)

        for i in range(depth):
            position = i / max(1, depth - 1)

            # Tone can shift based on arc pacing.
            frag_tone = tone
            if pacing[i].get("shift_tone", False):
                frag_tone = self._shift_tone(tone, position, arc)

            # Generate scene.
            scene = self._scene_gen.generate(
                species=context.companion_species,
                tone=frag_tone,
                chaos=context.personality_chaos,
            )

            # Generate sensory frames.
            frames = self._generate_frames(scene, frag_tone, position, context)

            # Inject symbols into frames.
            sym_slice = symbols[i * self._config.symbol_density:(i + 1) * self._config.symbol_density]
            for j, sym in enumerate(sym_slice):
                if j < len(frames):
                    frames[j].symbols.append(sym)

            # Memory anchor.
            memory_ref = None
            if anchors and self._entropy.random() < self._config.memory_probability:
                anchor = anchors.select_weighted(self._entropy)
                if anchor:
                    memory_ref = anchor.content[:80]

            # Transitions.
            trans_in = TransitionStyle.NONE if i == 0 else self._select_transition(position)
            trans_out = TransitionStyle.NONE if i == depth - 1 else TransitionStyle.DISSOLVE

            fragment = DreamFragment(
                title=scene.title,
                location=scene.location,
                tone=frag_tone,
                frames=frames,
                memory_anchor=memory_ref,
                transition_in=trans_in,
                transition_out=trans_out,
                duration_weight=pacing[i].get("weight", 1.0),
                lucidity=self._compute_lucidity(position, context),
            )
            fragments.append(fragment)

        return fragments

    def _generate_frames(
        self,
        scene: SceneTemplate,
        tone: DreamTone,
        position: float,
        context: EmotionalContext,
    ) -> list[DreamFrame]:
        """Generate sensory frames for a scene."""
        frames: list[DreamFrame] = []
        count = self._config.frames_per_fragment

        # Determine channel distribution.
        channels = self._select_channels(count)

        for i in range(count):
            channel = channels[i]

            if self._config.style == "abstract":
                content = self._abstract_gen.generate(tone, channel)
            else:
                content = self._sensory_gen.generate(
                    location=scene.location,
                    channel=channel,
                    tone=tone,
                )

            distortion = self._compute_distortion(position, context)

            frame = DreamFrame(
                content=content,
                channel=channel,
                intensity=0.3 + position * 0.4 + self._entropy.random() * 0.2,
                distortion=distortion,
            )
            frames.append(frame)

        return frames

    def _select_channels(self, count: int) -> list[SensoryChannel]:
        """Select sensory channels with diversity control."""
        all_channels = list(SensoryChannel)
        if self._config.sensory_diversity > 0.5:
            # High diversity: try to use different channels.
            self._entropy.shuffle(all_channels)
            return all_channels[:count]
        else:
            # Low diversity: mostly visual with occasional others.
            channels = [SensoryChannel.VISUAL] * count
            for i in range(count):
                if self._entropy.random() < self._config.sensory_diversity:
                    channels[i] = self._entropy.choice(all_channels)
            return channels

    def _select_transition(self, position: float) -> TransitionStyle:
        """Select transition style based on dream position."""
        styles = list(TransitionStyle)
        styles = [s for s in styles if s != TransitionStyle.NONE]

        if position < 0.3:
            # Early dream: gentle transitions.
            weights = {
                TransitionStyle.DISSOLVE: 0.4,
                TransitionStyle.ECHO: 0.3,
                TransitionStyle.MORPH: 0.2,
                TransitionStyle.ZOOM: 0.1,
            }
        elif position > 0.7:
            # Late dream: more jarring transitions.
            weights = {
                TransitionStyle.CUT: 0.3,
                TransitionStyle.FALL: 0.3,
                TransitionStyle.MIRROR: 0.2,
                TransitionStyle.MORPH: 0.2,
            }
        else:
            weights = {s: 1.0 / len(styles) for s in styles}

        return TransitionStyle(self._entropy.weighted_choice(
            {s.value: w for s, w in weights.items()}
        ))

    def _shift_tone(
        self, base: DreamTone, position: float, arc: ArcType
    ) -> DreamTone:
        """Shift tone based on arc position."""
        if arc == ArcType.DESCENT:
            darker = {
                DreamTone.ETHEREAL: DreamTone.EERIE,
                DreamTone.WARM: DreamTone.HEAVY,
                DreamTone.ELECTRIC: DreamTone.FRACTURED,
                DreamTone.LUMINOUS: DreamTone.ETHEREAL,
                DreamTone.PLAYFUL: DreamTone.EERIE,
            }
            if position > 0.5:
                return darker.get(base, base)
        elif arc == ArcType.ASCENT:
            lighter = {
                DreamTone.EERIE: DreamTone.ETHEREAL,
                DreamTone.HEAVY: DreamTone.WARM,
                DreamTone.FRACTURED: DreamTone.CRYSTALLINE,
                DreamTone.VOID: DreamTone.LUMINOUS,
            }
            if position > 0.5:
                return lighter.get(base, base)
        return base

    def _compute_distortion(self, position: float, context: EmotionalContext) -> float:
        """Compute surreal distortion level."""
        base = self._config.distortion_base
        chaos_boost = context.personality_chaos * 0.3
        position_curve = position * 0.2  # Distortion increases deeper in dream.
        noise = self._entropy.random() * 0.15
        return min(1.0, base + chaos_boost + position_curve + noise)

    def _compute_lucidity(self, position: float, context: EmotionalContext) -> float:
        """Compute how lucid (clear) the dream is at this position."""
        if self._config.style == "lucid":
            return 0.7 + self._entropy.random() * 0.3
        base = 0.5 - position * 0.3  # Less lucid deeper in dream.
        chaos_penalty = context.personality_chaos * 0.15
        return max(0.0, base - chaos_penalty + self._entropy.random() * 0.1)

    def _compute_intensity(
        self, context: EmotionalContext, fragments: list[DreamFragment]
    ) -> float:
        """Compute overall dream intensity."""
        if not fragments:
            return 0.0
        frag_intensity = sum(f.intensity for f in fragments) / len(fragments)
        emotional_component = context.emotional_intensity * 0.4
        chaos_component = context.personality_chaos * 0.2
        return min(1.0, frag_intensity * 0.4 + emotional_component + chaos_component)

    def _compute_impact(
        self,
        context: EmotionalContext,
        fragments: list[DreamFragment],
        tone: DreamTone,
    ) -> dict[str, float]:
        """Compute how the dream shifts emotions afterward."""
        impact: dict[str, float] = {}

        # Dreams generally provide serenity and reduce anxiety.
        intensity = self._compute_intensity(context, fragments)
        impact["serenity"] = intensity * 0.15
        impact["anxiety"] = -intensity * 0.1

        # Tone-specific impacts.
        tone_impacts: dict[DreamTone, dict[str, float]] = {
            DreamTone.EERIE: {"anxiety": 0.05, "curiosity": 0.1},
            DreamTone.WARM: {"affection": 0.1, "joy": 0.05},
            DreamTone.ELECTRIC: {"curiosity": 0.15, "excitement": 0.1},
            DreamTone.HEAVY: {"sadness": 0.05, "serenity": 0.05},
            DreamTone.PLAYFUL: {"mischief": 0.1, "joy": 0.1},
            DreamTone.LUMINOUS: {"joy": 0.1, "pride": 0.05},
            DreamTone.CRYSTALLINE: {"curiosity": 0.1},
            DreamTone.FRACTURED: {"anxiety": 0.05, "curiosity": 0.1},
        }
        for dim, val in tone_impacts.get(tone, {}).items():
            impact[dim] = impact.get(dim, 0.0) + val

        # Memory consolidation effect.
        mem_count = sum(1 for f in fragments if f.has_memory)
        if mem_count > 0:
            impact["serenity"] = impact.get("serenity", 0.0) + mem_count * 0.03

        return impact
