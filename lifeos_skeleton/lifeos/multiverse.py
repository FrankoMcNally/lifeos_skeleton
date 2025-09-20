# lifeos/multiverse.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
import csv
import json
import random

from .genome import Locus, Genome, MutationModel
from .traits import TraitDecoder, Traits
from .reproduction import ReproductionModel
from .lineage import LineageTracker, Individual
from .policy import Policy, Action

# -------------------------
# Policies (simple mapping)
# -------------------------
class PolicyRational(Policy):
    def decide(self, traits: Traits) -> Action:
        if traits.energy < 30:
            return "eat"
        return "explore"

class PolicySpiritual(Policy):
    def decide(self, traits: Traits) -> Action:
        # A soft-restraint bias
        if traits.energy < 50:
            return "rest"
        return "explore"

def make_policy(name: str) -> Policy:
    name = (name or "rational").lower()
    if name == "spiritual":
        return PolicySpiritual()
    return PolicyRational()

# -------------------------
# Scenario & World
# -------------------------
@dataclass
class Scenario:
    name: str
    enable_language: bool = False
    math_injection: bool = False
    money_system: bool = False
    policy: str = "rational"

class World:
    """One world with a population that evolves over generations."""
    def __init__(
        self,
        name: str,
        loci: List[Locus],
        population_size: int,
        generations: int,
        seed: int,
        mutation_rate: float,
        policy_name: str = "rational",
        out_dir: Optional[Path] = None,
    ):
        self.name = name
        self.loci = loci
        self.population_size = population_size
        self.generations = generations
        self.rng = random.Random(seed)
        self.decoder = TraitDecoder()
        self.mutation = MutationModel(per_locus_rate=mutation_rate)
        self.repro = ReproductionModel(self.mutation)
        self.policy = make_policy(policy_name)
        self.lineage = LineageTracker()
        self.out_dir = out_dir
        self.population: List[Individual] = []
        self._next_id = 0

    # ---------- initialization ----------
    def _new_individual(self, genome: Genome, parents: Optional[List[int]] = None) -> Individual:
        ind = Individual(id=self._next_id, genome=genome, parents=parents)
        self._next_id += 1
        self.lineage.add_individual(ind)
        return ind

    def initialize(self):
        for _ in range(self.population_size):
            g = Genome.random_init(self.loci, self.rng)
            ind = self._new_individual(g, parents=None)
            self.population.append(ind)

    # ---------- dynamics ----------
    def step_generation(self, gen: int):
        # Very simple “life”: convert genome -> traits -> decide action (affects energy mildly)
        updated: List[Individual] = []
        for ind in self.population:
            traits = self.decoder.decode(ind.genome)
            act = self.policy.decide(traits)
            # toy energy update (you’ll refine later)
            if act == "eat":
                # increase energy if below max
                new_energy = min(int(traits.energy) + 5, 100)
            elif act == "explore":
                new_energy = max(int(traits.energy) - 2, 0)
            else:  # rest
                new_energy = min(int(traits.energy) + 1, 100)

            # write back energy into second locus if exists (int locus)
            # if locus2 is int-based, we adjust; otherwise leave as-is
            if len(ind.genome.values) >= 2 and isinstance(ind.genome.values[1], int):
                new_vals = list(ind.genome.values)
                new_vals[1] = new_energy
                ind.genome = Genome(loci=ind.genome.loci, values=new_vals)

            updated.append(ind)

        self.population = updated

        # Reproduction: make a fresh generation by pairing neighbors
        self.rng.shuffle(self.population)
        children: List[Individual] = []
        for i in range(0, len(self.population) - 1, 2):
            p1 = self.population[i]
            p2 = self.population[i + 1]
            child_genome = self.repro.mate(p1.genome, p2.genome, self.rng)
            child = self._new_individual(child_genome, parents=[p1.id, p2.id])
            children.append(child)

        # Keep population size stable: if odd, drop last parent; if children less than target, clone random child (rare)
        if len(children) < self.population_size:
            while len(children) < self.population_size:
                if children:
                    clone_of = self.rng.choice(children)
                    # clone genome (no new lineage ID for parents) but still counts as new individual
                    c2 = self._new_individual(
                        Genome(loci=clone_of.genome.loci, values=list(clone_of.genome.values)),
                        parents=clone_of.parents,
                    )
                    children.append(c2)
                else:
                    # if somehow no children, re-initialize a random individual
                    g = Genome.random_init(self.loci, self.rng)
                    c = self._new_individual(g, parents=None)
                    children.append(c)

        self.population = children[: self.population_size]

    # ---------- metrics ----------
    def _genetic_diversity(self) -> float:
        # simple proxy: average std-like spread for float loci
        floats: List[List[float]] = []
        for idx, loc in enumerate(self.loci):
            if loc.type == "float":
                floats.append([float(ind.genome.values[idx]) for ind in self.population])
        if not floats:
            return 0.0
        spreads = []
        for column in floats:
            if len(column) < 2:
                spreads.append(0.0)
            else:
                mean = sum(column) / len(column)
                var = sum((x - mean) ** 2 for x in column) / (len(column) - 1)
                spreads.append(var ** 0.5)
        return sum(spreads) / len(spreads)

    def _avg_energy(self) -> float:
        # assumes second locus is energy (int)
        if not self.population or len(self.population[0].genome.values) < 2:
            return 0.0
        vals = [int(ind.genome.values[1]) for ind in self.population if isinstance(ind.genome.values[1], int)]
        return sum(vals) / len(vals) if vals else 0.0

    def compute_metrics(self, generation: int) -> Dict[str, Any]:
        return {
            "world": self.name,
            "generation": generation,
            "population": len(self.population),
            "genetic_diversity": round(self._genetic_diversity(), 6),
            "avg_energy": round(self._avg_energy(), 3),
        }

    # ---------- I/O ----------
    def write_metrics_row(self, csv_path: Path, row: Dict[str, Any]):
        new = not csv_path.exists()
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()))
            if new:
                writer.writeheader()
            writer.writerow(row)

    def dump_lineage(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        # simple dump: id -> parents
        data = {int(k): v.parents for k, v in self.lineage.individuals.items()}
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # ---------- run ----------
    def run(self, out_dir: Path):
        self.out_dir = out_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        metrics_csv = out_dir / "metrics.csv"
        # init pop
        self.initialize()
        # g=0 snapshot
        self.write_metrics_row(metrics_csv, self.compute_metrics(0))
        # iterate generations
        for g in range(1, self.generations + 1):
            self.step_generation(g)
            self.write_metrics_row(metrics_csv, self.compute_metrics(g))
        # lineage
        self.dump_lineage(out_dir / "lineage.json")


class Multiverse:
    """Runs multiple worlds (scenarios) from a shared base config and seed."""
    def __init__(
        self,
        base_seed: int,
        loci: List[Locus],
        population_size: int,
        generations: int,
        mutation_rate: float,
        scenarios: List[Scenario],
    ):
        self.base_seed = base_seed
        self.loci = loci
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.scenarios = scenarios

    def run_all(self, run_root: Path) -> Dict[str, Path]:
        """Run all scenarios; return map world_name -> folder path."""
        outputs: Dict[str, Path] = {}
        for idx, sc in enumerate(self.scenarios):
            # derive deterministic per-world seed (stable across runs with same base_seed)
            seed = (self.base_seed + (idx + 1) * 1009) & 0x7FFFFFFF
            world = World(
                name=sc.name,
                loci=self.loci,
                population_size=self.population_size,
                generations=self.generations,
                seed=seed,
                mutation_rate=self.mutation_rate,
                policy_name=sc.policy,
            )
            world_dir = run_root / sc.name
            world.run(world_dir)
            outputs[sc.name] = world_dir
        return outputs
