# grok-dreamcore

Surreal dream sequence engine. Procedural narrative generation from emotional state, memory anchors, and symbolic archetypes.

## What it does

Generates multi-layered dream sequences with:

- **Scene generation** — species-specific and universal dream locations with tone-appropriate atmosphere.
- **Sensory frames** — multi-channel perceptual content (visual, auditory, tactile, kinesthetic, temporal, synesthetic).
- **Memory anchors** — dreams reference real interaction memories, modeling consolidation during sleep.
- **Symbol resonance** — 27 Jungian archetypes selected by emotional consonance with the dreamer's mood.
- **Narrative arcs** — descent, ascent, cycle, and scatter arc types with pacing curves.
- **Emotional impact** — dreams shift the dreamer's emotional state (anxiety reduction, curiosity boost).

## Install

```bash
pip install grok-dreamcore
```

## Quick start

```python
from dreamcore import DreamEngine, DreamConfig
from dreamcore.engine import EmotionalContext

engine = DreamEngine(config=DreamConfig(depth=4, style="surreal"))

context = EmotionalContext(
    mood={"curiosity": 0.8, "mischief": 0.5},
    recent_topics=["ocean", "scheming", "old conversations"],
    memory_fragments=["we talked about underwater libraries"],
    companion_species="octopus",
    personality_chaos=0.7,
)

sequence = engine.generate(context)
print(sequence.narrate())
print(f"Symbols: {sequence.symbols}")
print(f"Impact: {sequence.emotional_impact}")
```

## Dream structure

```
DreamSequence (theme, arc, tone)
    └── DreamFragment (scene, location, tone, lucidity)
        └── DreamFrame (sensory content, channel, intensity, distortion)
```

## Configuration

```python
DreamConfig(
    depth=4,                  # Fragment count (1-7)
    frames_per_fragment=3,    # Sensory frames per scene (2-6)
    style="surreal",          # surreal | narrative | abstract | lucid
    memory_probability=0.35,  # Chance of memory anchor per fragment
    distortion_base=0.3,      # Base surreal distortion (0.0-1.0)
    symbol_density=2,         # Symbols per fragment
    sensory_diversity=0.6,    # Channel variety (0.0-1.0)
    arc_type="auto",          # auto | descent | ascent | cycle | scatter
)
```

## Symbol archetypes

27 built-in archetypes with emotional resonance scores:

spiral, mirror, key, door, water, fire, shadow, light, clock, eye, thread, bridge, mask, seed, shell, feather, bone, crystal, ink, echo, vortex, root, constellation, labyrinth, anvil, web, fog, tower.

Each archetype resonates with specific emotions. The resonance system automatically selects symbols that match the dreamer's current mood.

## Species support

Species-specific scene pools for: octopus, wolf, dragon, phoenix, cat. Universal scenes available for all species.

## License

Apache License 2.0
