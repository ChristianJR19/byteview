# Architecture

## Pipeline

1. **Context intake** — EmotionalContext with mood, topics, memories.
2. **Arc selection** — narrative arc from dominant emotion.
3. **Theme derivation** — dream theme from topics + mood.
4. **Tone mapping** — dream tone from dominant emotion.
5. **Anchor building** — memory anchors from context fragments.
6. **Symbol selection** — archetypes via emotional resonance.
7. **Fragment generation** — scenes, frames, anchors, transitions.
8. **Impact computation** — how the dream shifts emotion.
9. **Assembly** — DreamSequence output.

## Module Map

```
dreamcore/
├── engine.py           — Orchestrator
├── sequence.py         — Data structures
├── generators/
│   ├── scene.py        — Location generation
│   ├── sensory.py      — Sensory frame content
│   └── abstract.py     — Non-representational content
├── memory/
│   ├── anchors.py      — Memory anchor system
│   └── consolidation.py — Memory processing
├── symbols/
│   ├── archetypes.py   — Symbol pool + resonance
│   └── resonance.py    — Re-export
└── utils/
    ├── entropy.py      — Deterministic RNG
    └── timing.py       — Pacing curves + arc types
```
