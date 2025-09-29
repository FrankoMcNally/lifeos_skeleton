# lifeos/sentient_mk6.py
from __future__ import annotations
import random
from typing import Dict, Any, List, Optional


class MindConfig:
    """
    Compatibility shim for mk6 -> mk7.
    Older tests/engine code expect MindConfig to exist with thresholds.
    """
    def __init__(
        self,
        hunger_energy_threshold: float = 55.0,
        low_food_threshold_per_capita: float = 0.4,
        max_farm_effort_per_tick: float = 1.0,
        rng_seed: Optional[int] = None,
    ):
        self.hunger_energy_threshold = hunger_energy_threshold
        self.low_food_threshold_per_capita = low_food_threshold_per_capita
        self.max_farm_effort_per_tick = max_farm_effort_per_tick
        self.rng_seed = rng_seed


class SentientMind:
    """
    SentientMind MK7 (wired as MK6 for compatibility).
    - Retains mk6 interface: decide_actions(), execute_task()
    - Adds mk7 layered states: curiosity, competence, stress, social_bond, dreams, memory_trace
    """

    def __init__(self, agent_id: int = 0, cfg: Optional[MindConfig] = None):
        self.id = int(agent_id)
        self.cfg = cfg or MindConfig()
        seed = self.cfg.rng_seed if self.cfg.rng_seed is not None else (self.id * 7919)
        self.rng = random.Random(seed)

        # Core states
        self.energy: float = 50.0
        self.curiosity: float = 0.5
        self.competence: float = 0.5
        self.social_bond: float = 0.5
        self.stress: float = 0.2

        # Subconscious buffers
        self.dreams: List[str] = []
        self.memory_trace: List[Dict[str, Any]] = []

        # Simple log for debugging
        self._log: List[Dict[str, Any]] = []

    # --------- mk6 compatibility API ----------
    def decide_actions(
        self, gen: int, energy: float, env_snapshot: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Called by engine each tick.
        Must return list[dict] of actions like:
        [{"type": "farm", "effort": 0.7}]
        """
        return self.environment_action(gen, energy, env_snapshot)

    def execute_task(self, task: str) -> float:
        """
        Called by Environment for forage boost.
        In mk7 this reflects curiosity + competence.
        """
        if task == "forage":
            return self.competence * (0.5 + self.curiosity)
        return 0.0

    # --------- mk7 behaviors ----------
    def environment_action(
        self, gen: int, energy: float, env_snapshot: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        actions: List[Dict[str, Any]] = []
        pop = max(1, int(env_snapshot.get("population", 1)))
        food = int(env_snapshot.get("food", 0))

        # Farming decision
        hungry = energy < self.cfg.hunger_energy_threshold
        food_low = (food / float(pop)) < self.cfg.low_food_threshold_per_capita
        if hungry or food_low:
            base = 0.5
            hunger_scale = max(
                0.0,
                min(
                    1.0,
                    (self.cfg.hunger_energy_threshold - energy)
                    / self.cfg.hunger_energy_threshold,
                ),
            )
            shortage_scale = 0.0
            if food_low:
                per_cap = food / float(pop)
                shortage_scale = max(
                    0.0,
                    min(
                        1.0,
                        (self.cfg.low_food_threshold_per_capita - per_cap)
                        / max(1e-9, self.cfg.low_food_threshold_per_capita),
                    ),
                )
            farm_effort = base + 0.3 * hunger_scale + 0.3 * shortage_scale
            farm_effort += self.rng.uniform(-0.1, 0.1)
            farm_effort = max(0.0, min(self.cfg.max_farm_effort_per_tick, farm_effort))
            if farm_effort > 0:
                actions.append({"type": "farm", "effort": round(farm_effort, 3)})

        # Sleep / rest cycle
        if self.rng.random() < 0.1:
            actions.append({"type": "sleep"})

        # Share with needy
        if energy > 70 and self.rng.random() < 0.2:
            actions.append({"type": "share", "amount": 1})

        # Subconscious dream logging
        if self.rng.random() < 0.05:
            dream = f"dream-{self.rng.randint(1, 999)}"
            self.dreams.append(dream)
            self.curiosity = min(1.0, self.curiosity + 0.05)

        return actions

    def choose_partner(self, self_ind, candidates):
        """
        PSAI hook: choose partner based on cooperation & energy.
        """
        if not candidates:
            return None
        scored = []
        for cand in candidates:
            coop = getattr(cand.genome, "cooperation", 0.5)
            energy = getattr(cand, "energy", 50.0)
            score = coop * 0.6 + (energy / 100.0) * 0.4
            scored.append((score, cand))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    def consolidate_memory(self, events: List[Dict[str, Any]]) -> None:
        """
        Subconscious processing: adjust stress/curiosity.
        """
        self.memory_trace.extend(events[-5:])  # keep last 5
        if any("death" in str(e) for e in events):
            self.stress = min(1.0, self.stress + 0.1)
        if any("birth" in str(e) for e in events):
            self.curiosity = min(1.0, self.curiosity + 0.05)

    # --------- logging ----------
    def observe(self, gen: int, event: Dict[str, Any]) -> None:
        self._log.append({"gen": gen, **event})

    def dump_log(self) -> List[Dict[str, Any]]:
        return list(self._log)
