# lifeos/environment.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
import random


@dataclass
class EnvironmentConfig:
    base_food_per_gen: int = 100
    base_oxygen_per_gen: int = 100
    food_replenish_noise: float = 0.1
    oxygen_decay_per_gen: int = 0
    energy_per_food_unit: float = 1.0
    base_metabolic_cost: float = 1.0
    birth_cost: float = 2.0
    rng_seed: Optional[int] = None
    farming_bonus: int = 20  # NEW farming yield


class Environment:
    def __init__(self, cfg: EnvironmentConfig):
        self.cfg = cfg
        self.rng = random.Random(cfg.rng_seed)
        self.food = cfg.base_food_per_gen
        self.oxygen = cfg.base_oxygen_per_gen

    def replenish(self, generation: int):
        noise = 1.0 + self.rng.uniform(-self.cfg.food_replenish_noise, self.cfg.food_replenish_noise)
        self.food = max(0, int(round(self.cfg.base_food_per_gen * noise)))
        self.oxygen = max(0, self.cfg.base_oxygen_per_gen - self.cfg.oxygen_decay_per_gen * generation)

    def allocate_food(self, population: List, state_map: Dict[int, object], policy_adapter=None) -> Dict[int, int]:
        alive_agents = [ind for ind in population]
        if not alive_agents or self.food <= 0:
            return {}

        scores: Dict[int, float] = {}
        for ind in alive_agents:
            st = state_map[ind.id]
            deficit = max(0.0, 50.0 - getattr(st, "energy", 50.0))
            scores[ind.id] = 1.0 + deficit / 50.0

        if policy_adapter:
            for ind in alive_agents:
                try:
                    agent = policy_adapter.ensure_agent(str(ind.id))
                    scores[ind.id] += agent.execute_task("forage")
                    # NEW: farming adds more global food
                    self.food += int(agent.execute_task("farm") * self.cfg.farming_bonus)
                except Exception:
                    pass

        total_score = sum(scores.values())
        alloc: Dict[int, int] = {ind.id: 0 for ind in alive_agents}
        if total_score > 0:
            ids = list(scores.keys())
            weights = [scores[i] for i in ids]
            for _ in range(self.food):
                pick = self.rng.choices(ids, weights=weights, k=1)[0]
                alloc[pick] += 1
        self.food = 0
        return alloc

    def tick(self, generation: int, population: List, state_map: Dict[int, object], policy_adapter=None) -> Dict[str, object]:
        self.replenish(generation)
        allocations = self.allocate_food(population, state_map, policy_adapter)

        deaths: List[int] = []
        for ind in population:
            st = state_map[ind.id]
            if not hasattr(st, "energy"):
                st.energy = 50.0
            got_food = allocations.get(ind.id, 0)
            st.energy += got_food * self.cfg.energy_per_food_unit
            st.energy -= self.cfg.base_metabolic_cost
            if st.energy <= 0:
                deaths.append(ind.id)

        if self.oxygen < len(population):
            shortage = 1.0 - (self.oxygen / max(1, float(len(population))))
            to_kill = min(len(population), int(round(shortage * len(population))))
            sorted_by_energy = sorted(population, key=lambda x: state_map[x.id].energy)
            for victim in sorted_by_energy[:to_kill]:
                deaths.append(victim.id)

        return {
            "generation": generation,
            "allocated_food_total": sum(allocations.values()),
            "allocations": allocations,
            "deaths": deaths,
            "food_left": self.food,
            "oxygen_left": self.oxygen,
        }
