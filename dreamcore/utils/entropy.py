"""
Dream entropy — seeded RNG for deterministic dream generation.
"""

from __future__ import annotations

import random
import time
from typing import Any, TypeVar

T = TypeVar("T")


class DreamEntropy:
    """Deterministic random source for dream generation."""

    def __init__(self, seed: int | None = None) -> None:
        if seed is None:
            seed = int(time.time() * 1000) ^ id(self)
        self._seed = seed
        self._rng = random.Random(seed)

    @property
    def seed(self) -> int:
        return self._seed

    def random(self) -> float:
        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        return self._rng.randint(a, b)

    def choice(self, seq: list[T]) -> T:
        return self._rng.choice(seq)

    def shuffle(self, seq: list[Any]) -> None:
        self._rng.shuffle(seq)

    def weighted_choice(self, options: dict[str, float]) -> str:
        keys = list(options.keys())
        weights = [max(0.0, options[k]) for k in keys]
        total = sum(weights)
        if total == 0:
            return self._rng.choice(keys)
        r = self._rng.random() * total
        cumulative = 0.0
        for key, weight in zip(keys, weights):
            cumulative += weight
            if r <= cumulative:
                return key
        return keys[-1]

    def gaussian(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        return self._rng.gauss(mu, sigma)

    def fork(self) -> "DreamEntropy":
        return DreamEntropy(seed=self._rng.randint(0, 2**31 - 1))
