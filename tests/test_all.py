"""
Test suite for grok-dreamcore.
"""

import pytest

from dreamcore.engine import DreamEngine, DreamConfig, EmotionalContext
from dreamcore.sequence import (
    DreamSequence, DreamFragment, DreamFrame,
    DreamTone, TransitionStyle, SensoryChannel,
)
from dreamcore.generators.scene import SceneGenerator, SceneTemplate
from dreamcore.generators.sensory import SensoryGenerator
from dreamcore.generators.abstract import AbstractGenerator
from dreamcore.memory.anchors import MemoryAnchor, AnchorSet
from dreamcore.memory.consolidation import ConsolidationEngine
from dreamcore.symbols.archetypes import Archetype, ArchetypePool, SymbolResonance
from dreamcore.utils.entropy import DreamEntropy
from dreamcore.utils.timing import PacingCurve, ArcType


class TestDreamFrame:
    def test_creation(self):
        frame = DreamFrame(content="test", channel=SensoryChannel.VISUAL)
        assert frame.content == "test"
        assert frame.intensity == 0.5

    def test_clamped(self):
        frame = DreamFrame(content="x", intensity=5.0, distortion=5.0)
        assert frame.intensity == 1.0
        assert frame.distortion == 1.0

    def test_is_surreal(self):
        assert DreamFrame(content="x", distortion=0.8).is_surreal
        assert not DreamFrame(content="x", distortion=0.2).is_surreal

    def test_to_dict(self):
        frame = DreamFrame(content="test", symbols=["mirror"])
        d = frame.to_dict()
        assert d["content"] == "test"
        assert "mirror" in d["symbols"]


class TestDreamFragment:
    def test_narrate(self):
        frag = DreamFragment(
            title="test",
            location="a library",
            tone=DreamTone.ETHEREAL,
            frames=[DreamFrame(content="books float")],
        )
        text = frag.narrate()
        assert "library" in text
        assert "books float" in text

    def test_transition_narration(self):
        frag = DreamFragment(
            title="test",
            location="the void",
            tone=DreamTone.VOID,
            transition_in=TransitionStyle.FALL,
        )
        text = frag.narrate()
        assert "falling" in text.lower()

    def test_memory_anchor(self):
        frag = DreamFragment(
            title="test",
            location="here",
            tone=DreamTone.WARM,
            memory_anchor="that time we talked about stars",
        )
        assert frag.has_memory
        text = frag.narrate()
        assert "stars" in text

    def test_intensity(self):
        frag = DreamFragment(
            title="test",
            location="here",
            tone=DreamTone.ELECTRIC,
            frames=[
                DreamFrame(content="a", intensity=0.8),
                DreamFrame(content="b", intensity=0.4),
            ],
        )
        assert 0.5 < frag.intensity < 0.7

    def test_symbols(self):
        frag = DreamFragment(
            title="test",
            location="here",
            tone=DreamTone.EERIE,
            frames=[
                DreamFrame(content="a", symbols=["mirror"]),
                DreamFrame(content="b", symbols=["mirror", "key"]),
            ],
        )
        syms = frag.symbols
        assert "mirror" in syms
        assert "key" in syms


class TestDreamSequence:
    def _make_sequence(self, n: int = 3) -> DreamSequence:
        frags = [
            DreamFragment(
                title=f"frag_{i}",
                location=f"location_{i}",
                tone=DreamTone.ETHEREAL,
                frames=[DreamFrame(content=f"frame_{i}")],
            )
            for i in range(n)
        ]
        return DreamSequence(
            theme="test theme",
            fragments=frags,
            intensity=0.5,
        )

    def test_narrate(self):
        seq = self._make_sequence()
        text = seq.narrate()
        assert "test theme" in text
        assert "waking" in text.lower()

    def test_narrate_empty(self):
        seq = DreamSequence(theme="nothing", fragments=[], intensity=0.0)
        text = seq.narrate()
        assert "void" in text.lower() or "empty" in text.lower()

    def test_condensed_narration(self):
        seq = self._make_sequence()
        text = seq.narrate_condensed()
        assert "test theme" in text

    def test_stats(self):
        seq = self._make_sequence(4)
        assert seq.fragment_count == 4
        assert seq.total_frames == 4

    def test_to_dict(self):
        seq = self._make_sequence()
        d = seq.to_dict()
        assert d["theme"] == "test theme"
        assert "stats" in d
        assert d["stats"]["fragment_count"] == 3


class TestSceneGenerator:
    def test_generate(self):
        gen = SceneGenerator(entropy=DreamEntropy(seed=42))
        scene = gen.generate(species="octopus", tone=DreamTone.ETHEREAL)
        assert isinstance(scene, SceneTemplate)
        assert len(scene.title) > 0
        assert len(scene.location) > 0

    def test_deterministic(self):
        s1 = SceneGenerator(entropy=DreamEntropy(seed=42)).generate()
        s2 = SceneGenerator(entropy=DreamEntropy(seed=42)).generate()
        assert s1.title == s2.title

    def test_generic_species(self):
        gen = SceneGenerator(entropy=DreamEntropy(seed=42))
        scene = gen.generate(species="unknown_species")
        assert isinstance(scene, SceneTemplate)


class TestSensoryGenerator:
    def test_generate_visual(self):
        gen = SensoryGenerator(entropy=DreamEntropy(seed=42))
        content = gen.generate(location="an ocean trench", channel=SensoryChannel.VISUAL)
        assert isinstance(content, str)
        assert len(content) > 10

    def test_generate_auditory(self):
        gen = SensoryGenerator(entropy=DreamEntropy(seed=42))
        content = gen.generate(location="abstract void", channel=SensoryChannel.AUDITORY)
        assert isinstance(content, str)

    def test_generate_tactile(self):
        gen = SensoryGenerator(entropy=DreamEntropy(seed=42))
        content = gen.generate(location="a forest", channel=SensoryChannel.TACTILE)
        assert isinstance(content, str)


class TestAbstractGenerator:
    def test_generate(self):
        gen = AbstractGenerator(entropy=DreamEntropy(seed=42))
        content = gen.generate(tone=DreamTone.ELECTRIC)
        assert isinstance(content, str)
        assert len(content) > 10

    def test_all_tones(self):
        gen = AbstractGenerator(entropy=DreamEntropy(seed=42))
        for tone in DreamTone:
            content = gen.generate(tone=tone)
            assert len(content) > 0


class TestMemoryAnchors:
    def test_anchor_creation(self):
        anchor = MemoryAnchor(content="we talked about stars", salience=0.7)
        assert anchor.weight > 0

    def test_reference(self):
        anchor = MemoryAnchor(content="test", salience=0.5)
        anchor.reference()
        assert anchor.times_referenced == 1
        assert anchor.salience > 0.5

    def test_anchor_set(self):
        aset = AnchorSet()
        aset.add(MemoryAnchor(content="a", salience=0.8))
        aset.add(MemoryAnchor(content="b", salience=0.3))
        assert len(aset) == 2

    def test_weighted_selection(self):
        aset = AnchorSet()
        aset.add(MemoryAnchor(content="strong", salience=0.9, emotional_weight=0.9))
        aset.add(MemoryAnchor(content="weak", salience=0.1, emotional_weight=0.1))
        entropy = DreamEntropy(seed=42)
        selections = [aset.select_weighted(entropy).content for _ in range(20)]
        assert "strong" in selections


class TestConsolidation:
    def test_consolidate(self):
        engine = ConsolidationEngine()
        aset = AnchorSet()
        aset.add(MemoryAnchor(content="important memory", salience=0.8, emotional_weight=0.7, tags=["ocean"]))
        aset.add(MemoryAnchor(content="another ocean memory", salience=0.6, emotional_weight=0.4, tags=["ocean"]))
        result = engine.consolidate(aset)
        assert len(result.strengthened) > 0
        assert len(result.processed) > 0


class TestArchetypes:
    def test_pool(self):
        pool = ArchetypePool()
        assert len(pool.all()) > 20
        assert pool.get("mirror") is not None

    def test_resonance(self):
        arch = Archetype("test", "abstract", {"curiosity": 0.8, "joy": 0.3})
        score = arch.resonance_with({"curiosity": 1.0, "joy": 0.5})
        assert score > 0

    def test_by_domain(self):
        pool = ArchetypePool()
        natural = pool.by_domain("natural")
        assert len(natural) > 0
        assert all(a.domain == "natural" for a in natural)

    def test_by_emotion(self):
        pool = ArchetypePool()
        curious = pool.by_emotion("curiosity", threshold=0.5)
        assert len(curious) > 0

    def test_symbol_resonance(self):
        resonance = SymbolResonance()
        symbols = resonance.select(
            mood={"curiosity": 0.9, "mischief": 0.5},
            topics=["ocean", "puzzles"],
            count=5,
        )
        assert len(symbols) == 5
        assert all(isinstance(s, str) for s in symbols)

    def test_explain(self):
        resonance = SymbolResonance()
        explanation = resonance.explain("mirror")
        assert "mirror" in explanation
        assert "self" in explanation.lower()


class TestPacing:
    def test_descent(self):
        curve = PacingCurve()
        pacing = curve.compute(ArcType.DESCENT, 4)
        assert len(pacing) == 4
        assert pacing[0]["intensity"] < pacing[-1]["intensity"]

    def test_ascent(self):
        curve = PacingCurve()
        pacing = curve.compute(ArcType.ASCENT, 4)
        assert pacing[0]["intensity"] > pacing[-1]["intensity"]

    def test_cycle(self):
        curve = PacingCurve()
        pacing = curve.compute(ArcType.CYCLE, 6)
        assert len(pacing) == 6

    def test_scatter(self):
        curve = PacingCurve()
        pacing = curve.compute(ArcType.SCATTER, 4)
        assert len(pacing) == 4


class TestEntropy:
    def test_deterministic(self):
        e1 = DreamEntropy(seed=42)
        e2 = DreamEntropy(seed=42)
        assert e1.random() == e2.random()

    def test_weighted_choice(self):
        e = DreamEntropy(seed=42)
        counts = {"a": 0, "b": 0}
        for _ in range(1000):
            r = e.weighted_choice({"a": 0.9, "b": 0.1})
            counts[r] += 1
        assert counts["a"] > counts["b"]


class TestDreamEngine:
    def test_generate_basic(self):
        engine = DreamEngine(config=DreamConfig(depth=3), seed=42)
        context = EmotionalContext(mood={"curiosity": 0.8})
        seq = engine.generate(context)
        assert isinstance(seq, DreamSequence)
        assert len(seq.fragments) == 3

    def test_generate_with_memories(self):
        engine = DreamEngine(config=DreamConfig(depth=4), seed=42)
        context = EmotionalContext(
            mood={"curiosity": 0.7, "mischief": 0.5},
            recent_topics=["ocean", "scheming"],
            memory_fragments=["we talked about underwater libraries", "that time you made a pun"],
            companion_species="octopus",
        )
        seq = engine.generate(context)
        assert seq.fragment_count == 4
        assert len(seq.symbols) > 0

    def test_narration_not_empty(self):
        engine = DreamEngine(seed=42)
        context = EmotionalContext(mood={"serenity": 0.5})
        seq = engine.generate(context)
        text = seq.narrate()
        assert len(text) > 100
        assert "dream" in text.lower() or "drifting" in text.lower()

    def test_config_validation(self):
        with pytest.raises(ValueError):
            DreamConfig(depth=0).validate()
        with pytest.raises(ValueError):
            DreamConfig(depth=10).validate()

    def test_different_styles(self):
        for style in ("surreal", "narrative", "abstract", "lucid"):
            engine = DreamEngine(config=DreamConfig(style=style, depth=2), seed=42)
            context = EmotionalContext(mood={"curiosity": 0.5})
            seq = engine.generate(context)
            assert seq.fragment_count == 2

    def test_emotional_impact(self):
        engine = DreamEngine(seed=42)
        context = EmotionalContext(mood={"anxiety": 0.8})
        seq = engine.generate(context)
        assert "anxiety" in seq.emotional_impact or "serenity" in seq.emotional_impact

    def test_deterministic(self):
        ctx = EmotionalContext(mood={"curiosity": 0.5})
        s1 = DreamEngine(seed=42).generate(ctx)
        s2 = DreamEngine(seed=42).generate(ctx)
        assert s1.theme == s2.theme
        assert s1.fragment_count == s2.fragment_count
