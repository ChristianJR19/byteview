"""
Basic dream generation example.

Run: python examples/basic_dream.py
"""

from dreamcore import DreamEngine, DreamConfig
from dreamcore.engine import EmotionalContext


def main() -> None:
    engine = DreamEngine(
        config=DreamConfig(depth=4, style="surreal"),
        seed=42,
    )

    context = EmotionalContext(
        mood={"curiosity": 0.8, "mischief": 0.5, "serenity": 0.3},
        recent_topics=["underwater temples", "old riddles", "ink patterns"],
        memory_fragments=[
            "we talked about whether dreams can solve problems",
            "that conversation about the nature of memory",
        ],
        companion_species="octopus",
        personality_chaos=0.7,
        bond_strength=0.6,
    )

    print("Generating dream...\n")
    sequence = engine.generate(context)

    print(sequence.narrate())
    print(f"\n--- Dream Stats ---")
    print(f"Theme: {sequence.theme}")
    print(f"Arc: {sequence.arc}")
    print(f"Tone: {sequence.overall_tone.value}")
    print(f"Intensity: {sequence.intensity:.2f}")
    print(f"Fragments: {sequence.fragment_count}")
    print(f"Total frames: {sequence.total_frames}")
    print(f"Symbols: {', '.join(sequence.symbols)}")
    print(f"Memory references: {sequence.memory_count}")
    print(f"Emotional impact: {sequence.emotional_impact}")


if __name__ == "__main__":
    main()
