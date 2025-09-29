# lifeos/sentient_mk6.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import random


@dataclass
class MindConfig:
    """Tiny, dependency-free config for the SentientMind."""
    # action thresholds
    hunger_energy_threshold: float = 55.0
    low_food_threshold_per_capita: float = 0.4
    # farming “effort” and yield knobs (the engine will convert effort to food units)
    max_farm_effort_per_tick: float = 1.0  # abstract effort units (0..1)
    # for foraging boost (used by Environment if it calls execute_task("forage"))
    forage_competence_base: float = 0.1
    forage_competence_noise: float = 0.15
    rng_seed: Optional[int] = None


class SentientMind:
    """
    SentientMind MK6 (lite): tiny policy the agent uses each tick.
    - Decides when to FARM based on personal energy & global food.
    - Offers a small foraging competence boost when the Environment asks for it.
    - Logs observations (no heavy memory system here — the engine already has RingMemory).
    """
    def __init__(self, agent_id: int, cfg: Optional[MindConfig] = None):
        self.id = int(agent_id)
        self.cfg = cfg or MindConfig()
        self.rng = random.Random(self.cfg.rng_seed if self.cfg.rng_seed is not None else (self.id * 7919))
        self._log: List[Dict[str, Any]] = []

    # --------- public API used by the engine ----------
    def decide_actions(self, gen: int, energy: float, env_snapshot: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Return a list of actions for this tick. Minimal set for now:
        - {"type": "farm", "effort": float in [0, max_farm_effort_per_tick]}
        """
        actions: List[Dict[str, Any]] = []
        pop = max(1, int(env_snapshot.get("population", 1)))
        food = int(env_snapshot.get("food", 0))

        # simple heuristics: farm when I'm hungry OR per-capita food is low
        hungry = (energy < self.cfg.hunger_energy_threshold)
        food_low = (food / float(pop)) < self.cfg.low_food_threshold_per_capita

        if hungry or food_low:
            # scale effort by how hungry we are and how short food is
            hunger_scale = max(0.0, min(1.0, (self.cfg.hunger_energy_threshold - energy) / self.cfg.hunger_energy_threshold))
            shortage_scale = 0.0
            if food_low:
                # 0 -> at threshold, 1 -> zero food
                per_cap = food / float(pop)
                shortage_scale = max(0.0, min(1.0, (self.cfg.low_food_threshold_per_capita - per_cap) / max(1e-9, self.cfg.low_food_threshold_per_capita)))
            base = 0.4 + 0.4 * hunger_scale + 0.4 * shortage_scale
            noise = self.rng.uniform(-0.1, 0.1)
            effort = max(0.0, min(self.cfg.max_farm_effort_per_tick, base + noise))
            if effort > 0.0:
                actions.append({"type": "farm", "effort": round(effort, 3)})

        return actions

    def execute_task(self, task: str) -> float:
        """
        Optional hook used by the Environment for foraging priority/competence.
        We keep it very small: return a small positive number with noise.
        """
        if task == "forage":
            base = self.cfg.forage_competence_base
            noise = self.rng.uniform(-self.cfg.forage_competence_noise, self.cfg.forage_competence_noise)
            return max(0.0, base + noise)
        return 0.0

    # --------- logging (for debugging only) ----------
    def observe(self, gen: int, event: Dict[str, Any]) -> None:
        self._log.append({"gen": gen, **event})

    def dump_log(self) -> List[Dict[str, Any]]:
        return list(self._log)
