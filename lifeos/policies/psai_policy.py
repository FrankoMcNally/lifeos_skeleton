# lifeos/policies/psai_policy.py
"""
Prime Sentient AI (PSAI) policy adapter.

This integrates the Prime Sentient AI Mark 6 agent into
the Adam & Eve simulation. It nudges partner attraction
based on competence signals from execute_task().
"""

import random
from typing import List, Optional
from .prime_sentient_ai_mark6 import SentientAgent


class PSAIPolicy:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.agents: dict[str, SentientAgent] = {}

    def ensure_agent(self, indiv_id: int) -> SentientAgent:
        """Create or fetch a SentientAgent for a given individual ID."""
        if indiv_id not in self.agents:
            self.agents[indiv_id] = SentientAgent(str(indiv_id))
        return self.agents[indiv_id]

    def choose_partner(self, indiv, candidates: List) -> Optional[object]:
        """
        Select a partner from candidate individuals.
        Preference is weighted by PSAI competence scores.
        """
        if not candidates:
            return None

        scores = []
        for cand in candidates:
            agent = self.ensure_agent(cand.id)
            competence = agent.execute_task("pairing")  # proxy for competence
            scores.append((cand, max(0.01, competence)))  # avoid zero weight

        # Weighted random choice
        total = sum(c for _, c in scores)
        r = self.rng.uniform(0, total)
        upto = 0.0
        for cand, c in scores:
            if upto + c >= r:
                return cand
            upto += c

        # fallback
        return self.rng.choice(candidates)
