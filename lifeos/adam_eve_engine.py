# lifeos/adam_eve_engine.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import csv, json, random

from .genome import Locus, Genome, MutationModel
from .reproduction import ReproductionModel
from .lineage import LineageTracker, Individual
from .adam_eve_memory import RingMemory, SharedLedger
from .environment import Environment, EnvironmentConfig
from .sentient_mk6 import SentientMind, MindConfig  # <-- NEW

# Optional PSAI policy (loaded only if selected)
try:
    from policies.psai_policy import PSAIPolicy  # type: ignore
except Exception:
    PSAIPolicy = None  # noqa: N816


# ---------------------
# Datamodel for states
# ---------------------
@dataclass
class PersonState:
    # Age/life-cycle
    phase: int = 0
    # Social / family
    partner_id: Optional[int] = None
    couple_id: Optional[int] = None
    children_count: int = 0
    # Physiology / memory
    energy: float = 50.0
    memory: RingMemory = field(default_factory=lambda: RingMemory(capacity=8))
    # Cognition
    mind: Optional[SentientMind] = None  # <-- NEW


# ---------------------
# Adam & Eve World
# ---------------------
class AdamEveWorld:
    """
    Adam & Eve world with optional caps, PSAI partner selection, and a global Environment.
    Adds SentientMind per agent (farming decisions), and allows reproduction for all phases
    >= reproduction_phase (or >= pair_at_phase if reproduction_phase is None).
    """

    # Simple economics for farming (kept in-engine to avoid breaking Environment)
    FARM_YIELD_PER_EFFORT = 4        # food units created per 1.0 effort
    FARM_ENERGY_COST_PER_EFFORT = 0.6

    def __init__(
        self,
        seed: int,
        loci: List[Locus],
        num_couples: int = 12,
        generations: int = 60,
        mutation_rate: float = 0.01,
        lifespan_phases: Optional[int] = 4,       # None => no death by phase
        reproduction_phase: Optional[int] = 1,    # None => reproduce when phase >= pair_at_phase
        pair_at_phase: int = 1,
        children_cap_range: Tuple[int, int] = (4, 8),
        traits_dir: Optional[Path] = None,
        per_individual_kb: int = 2,               # kept for compat; RingMemory size is internal
        shared_pool_kb: int = 16,                 # SharedLedger capacity (KB)
        policy: str = "baseline",                 # "baseline" or "psai"
        env_cfg: Optional[dict] = None,           # environment config dict
        out_dir: Optional[Path] = None,
    ):
        self.rng = random.Random(int(seed))
        self.loci = loci
        self.num_couples = int(num_couples)
        self.generations = int(generations)

        # Lifespan / reproduction settings (allow None for unlimited)
        self.lifespan_phases: Optional[int] = None if lifespan_phases in (None, 0) else int(lifespan_phases)
        self.reproduction_phase: Optional[int] = None if reproduction_phase in (None, -1) else int(reproduction_phase)
        self.pair_at_phase = int(pair_at_phase)

        # Children cap handling (None => unlimited)
        self.children_cap_range = children_cap_range

        self.traits_dir = Path(traits_dir) if traits_dir else None

        self.decoder_mutation = MutationModel(per_locus_rate=float(mutation_rate))
        self.repro = ReproductionModel(crossover_rate=0.5)
        self.lineage = LineageTracker()
        self.out_dir: Optional[Path] = out_dir

        self.population: List[Individual] = []
        self.state: Dict[int, PersonState] = {}              # id -> PersonState
        self.couple_cap: Dict[int, Optional[int]] = {}       # couple_id -> cap or None for unlimited
        self.couple_members: Dict[int, Tuple[int, int]] = {} # couple_id -> (idA, idB)
        self._next_id = 0

        # Shared memory ledger (global KB-scale)
        self.shared_ledger = SharedLedger(cap_bytes=shared_pool_kb * 1024)

        # audit trail of births/deaths (do NOT log farming here to keep tests stable)
        self.reproduction_events: List[Dict] = []

        # optional: load trait specs (names only)
        self.available_traits: List[str] = self._load_trait_names(self.traits_dir) if self.traits_dir else []

        # Policy plug-in
        if policy == "psai" and PSAIPolicy is not None:
            self.policy = PSAIPolicy(seed=int(seed))
        else:
            self.policy = None

        # Environment setup
        ecfg = env_cfg or {}
        env_conf = EnvironmentConfig(
            base_food_per_gen = int(ecfg.get("base_food_per_gen", 100)),
            base_oxygen_per_gen = int(ecfg.get("base_oxygen_per_gen", 100)),
            food_replenish_noise = float(ecfg.get("food_replenish_noise", 0.1)),
            oxygen_decay_per_gen = int(ecfg.get("oxygen_decay_per_gen", 0)),
            energy_per_food_unit = float(ecfg.get("energy_per_food_unit", 1.0)),
            base_metabolic_cost = float(ecfg.get("base_metabolic_cost", 1.0)),
            birth_cost = float(ecfg.get("birth_cost", 2.0)),
            rng_seed = int(ecfg.get("rng_seed", int(seed))),
        )
        self.environment = Environment(env_conf)

    # ---------- utils ----------
    def _new_individual(self, genome: Genome, parents: Optional[List[int]] = None) -> Individual:
        ind = Individual(id=self._next_id, genome=genome, parents=parents)
        self._next_id += 1
        self.lineage.add_individual(ind)
        st = PersonState()
        # wire the mind
        st.mind = SentientMind(agent_id=ind.id, cfg=MindConfig(rng_seed=self.rng.randint(1, 10_000_000)))
        self.state[ind.id] = st
        return ind

    def _load_trait_names(self, root: Path) -> List[str]:
        names: List[str] = []
        if root and root.exists():
            for p in root.rglob("*.json"):
                names.append(p.stem)
        return sorted(set(names))

    def _are_full_siblings(self, a: Individual, b: Individual) -> bool:
        pa = set(a.parents or [])
        pb = set(b.parents or [])
        return len(pa) == 2 and pa == pb

    def _couple_cap_value(self) -> Optional[int]:
        lo, hi = self.children_cap_range
        if hi >= 9999:
            return None  # unlimited
        return self.rng.randint(lo, hi)

    # ---------- init founders ----------
    def initialize_founders(self):
        for cidx in range(self.num_couples):
            g1 = Genome.random_init(self.loci, self.rng)
            g2 = Genome.random_init(self.loci, self.rng)
            a = self._new_individual(g1, parents=None)
            b = self._new_individual(g2, parents=None)
            couple_id = cidx
            self.state[a.id].partner_id = b.id
            self.state[b.id].partner_id = a.id
            self.state[a.id].couple_id = couple_id
            self.state[b.id].couple_id = couple_id
            cap = self._couple_cap_value()
            self.couple_cap[couple_id] = cap
            self.couple_members[couple_id] = (a.id, b.id)
            self.population.extend([a, b])

            # memory / log
            self.state[a.id].memory.remember(0, {"event": "founder", "partner": b.id})
            self.state[b.id].memory.remember(0, {"event": "founder", "partner": a.id})
            self.shared_ledger.add({"gen": 0, "event": "founder_pair", "ids": [a.id, b.id]})

    # ---------- pairing ----------
    def _pair_unpaired_adults(self, gen: int):
        pool = [ind for ind in self.population
                if self.state[ind.id].partner_id is None and self.state[ind.id].phase >= self.pair_at_phase]
        self.rng.shuffle(pool)

        matched: set[int] = set()
        for focal in pool:
            if focal.id in matched:
                continue
            candidates = [c for c in pool if c.id not in matched and c.id != focal.id]
            # incest block: prevent full-sibling pairs
            candidates = [c for c in candidates if not self._are_full_siblings(focal, c)]
            if not candidates:
                continue

            if self.policy:
                partner = self.policy.choose_partner(focal, candidates)  # external PSAI chooser if present
            else:
                partner = self.rng.choice(candidates)

            new_cid = max(self.couple_cap.keys(), default=self.num_couples - 1) + 1
            self.state[focal.id].partner_id = partner.id
            self.state[partner.id].partner_id = focal.id
            self.state[focal.id].couple_id = new_cid
            self.state[partner.id].couple_id = new_cid
            cap = self._couple_cap_value()
            self.couple_cap[new_cid] = cap
            self.couple_members[new_cid] = (focal.id, partner.id)
            matched.update([focal.id, partner.id])

            # memory / log
            self.state[focal.id].memory.remember(gen, {"event": "paired", "partner": partner.id})
            self.state[partner.id].memory.remember(gen, {"event": "paired", "partner": focal.id})
            self.shared_ledger.add({"gen": gen, "event": "pair", "ids": [focal.id, partner.id]})

    # ---------- step ----------
    def step_generation(self, gen: int):
        births: List[Individual] = []

        # 1) Age and remove dead by lifespan cap (if any)
        survivors: List[Individual] = []
        for ind in self.population:
            st = self.state[ind.id]
            st.phase += 1 if gen > 0 else 0  # generation 0 is initial snapshot
            if self.lifespan_phases is None or st.phase < self.lifespan_phases:
                survivors.append(ind)
        self.population = survivors

        # 2) Pair newly eligible adults (loyal thereafter)
        self._pair_unpaired_adults(gen)

        # 2.5) Let minds decide proactive actions (e.g., FARM) BEFORE food is allocated
        # Convert effort into food & apply energy cost
        total_farm_food = 0
        for ind in self.population:
            st = self.state[ind.id]
            if st.mind is None:
                continue
            env_snap = {"food": self.environment.food, "oxygen": self.environment.oxygen, "population": len(self.population)}
            actions = st.mind.decide_actions(gen, st.energy, env_snap)
            for act in actions:
                if act.get("type") == "farm":
                    effort = float(act.get("effort", 0.0))
                    if effort <= 0:
                        continue
                    # apply energy cost
                    st.energy -= effort * self.FARM_ENERGY_COST_PER_EFFORT
                    # “create” food
                    created = int(round(effort * self.FARM_YIELD_PER_EFFORT))
                    if created > 0:
                        total_farm_food += created
                        # log to shared ledger only (keep reproduction_events clean)
                        self.shared_ledger.add({"gen": gen, "event": "farm", "id": ind.id, "effort": round(effort, 3), "yield": created})
                        if st.mind:
                            st.mind.observe(gen, {"event": "farm", "effort": round(effort, 3), "yield": created})
        if total_farm_food > 0:
            self.environment.food += total_farm_food  # minds generated extra food before allocation

        # 3) Reproduction (at most once per couple per generation)
        repro_pairs_seen: set[int] = set()
        for ind in self.population:
            st = self.state[ind.id]

            # NEW RULE:
            # - if reproduction_phase is None => allow when phase >= pair_at_phase
            # - else allow when phase >= reproduction_phase  (not strict equality)
            if self.reproduction_phase is None:
                if st.phase < self.pair_at_phase:
                    continue
            else:
                if st.phase < self.reproduction_phase:
                    continue

            pid = st.partner_id
            cid = st.couple_id
            if pid is None or cid is None or cid in repro_pairs_seen:
                continue

            # ensure partner is alive & still loyal
            if pid not in self.state:
                continue
            pst = self.state[pid]
            if pst.partner_id != ind.id:
                continue  # loyalty check

            # cap check (None => unlimited)
            total_children = self.state[ind.id].children_count + self.state[pid].children_count
            cap = self.couple_cap.get(cid, None)
            if cap is not None and total_children >= cap:
                continue

            # Partner object
            other = next((x for x in self.population if x.id == pid), None)
            if other is None:
                continue

            # child creation
            child_genome = self.repro.mate(ind.genome, other.genome, self.rng)
            child_genome = self.decoder_mutation.mutate(child_genome, self.rng)
            child = self._new_individual(child_genome, parents=[ind.id, other.id])
            births.append(child)

            # update couple children counts
            self.state[ind.id].children_count += 1
            self.state[pid].children_count += 1
            repro_pairs_seen.add(cid)

            # birth energy cost (parents)
            bc = self.environment.cfg.birth_cost
            self.state[ind.id].energy -= bc
            self.state[pid].energy -= bc

            # audit + memory
            self.reproduction_events.append({
                "generation": gen,
                "event": "birth",
                "parents": (ind.id, pid),
                "couple_id": cid,
                "child_id": child.id,
                "phase": st.phase,
            })
            self.state[ind.id].memory.remember(gen, {"event": "birth", "child": child.id})
            self.state[pid].memory.remember(gen, {"event": "birth", "child": child.id})
            self.shared_ledger.add({"gen": gen, "event": "birth", "parents": [ind.id, pid], "child": child.id})

        # 4) Add births now so newborns can be fed by the environment this generation
        self.population.extend(births)

        # 5) Environment tick: allocate food, apply metabolic costs, compute environmental deaths
        env_summary = self.environment.tick(gen, self.population, self.state, policy_adapter=self.policy)

        # Apply environment deaths
        dead_ids = set(env_summary.get("deaths", []))
        if dead_ids:
            self.population = [ind for ind in self.population if ind.id not in dead_ids]
            for did in dead_ids:
                self.reproduction_events.append({
                    "generation": gen,
                    "event": "death_env",
                    "id": did,
                    "reason": "env"
                })

    # ---------- metrics ----------
    def compute_metrics(self, generation: int) -> Dict[str, object]:
        alive = len(self.population)
        pairs = sum(1 for ind in self.population if self.state[ind.id].partner_id is not None) // 2
        births_this_gen = sum(1 for e in self.reproduction_events
                              if e.get("event") == "birth" and e.get("generation") == generation)
        deaths_env_this_gen = sum(1 for e in self.reproduction_events
                                  if e.get("event") == "death_env" and e.get("generation") == generation)
        avg_energy = (sum(self.state[ind.id].energy for ind in self.population) / max(1, alive)) if alive else 0.0

        # Environment levels
        food_left = getattr(getattr(self, "environment", None), "food", None)
        oxygen_left = getattr(getattr(self, "environment", None), "oxygen", None)

        # Shared pool usage (KB)
        used_bytes = len(str(self.shared_ledger.events).encode("utf-8"))
        return {
            "generation": generation,
            "alive": alive,
            "pairs": pairs,
            "births": births_this_gen,
            "deaths_env": deaths_env_this_gen,
            "avg_energy": round(avg_energy, 3),
            "food_left": food_left,
            "oxygen_left": oxygen_left,
            "shared_pool_capacity_kb": self.shared_ledger.capacity_bytes // 1024,
            "shared_pool_used_kb": self.shared_ledger.used_bytes // 1024,
        }

    # ---------- I/O ----------
    def write_metrics_row(self, csv_path: Path, row: Dict[str, object]):
        new = not csv_path.exists()
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()))
            if new:
                writer.writeheader()
            writer.writerow(row)

    def dump_lineage(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {int(k): v.parents for k, v in self.lineage.individuals.items()}
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # ---------- run ----------
    def run(self, out_dir: Path):
        self.out_dir = out_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        metrics_csv = out_dir / "metrics.csv"

        # minimal loci fallback if user didn't wire custom loci
        if not self.loci:
            self.loci = [
                Locus(name="cooperation", type="float", min=0.0, max=1.0),
                Locus(name="curiosity", type="float", min=0.0, max=1.0),
                Locus(name="energy", type="int", min=0, max=100),
            ]

        # founders
        self.initialize_founders()

        # g=0 snapshot
        self.write_metrics_row(metrics_csv, self.compute_metrics(0))

        # iterate generations
        for g in range(1, self.generations + 1):
            self.step_generation(g)
            self.write_metrics_row(metrics_csv, self.compute_metrics(g))

        # lineage & audit
        self.dump_lineage(out_dir / "lineage.json")
        (out_dir / "reproduction_events.json").write_text(
            json.dumps(self.reproduction_events, indent=2), encoding="utf-8"
        )
        # small trait catalogue (if any)
        (out_dir / "traits_loaded.json").write_text(
            json.dumps(self.available_traits, indent=2), encoding="utf-8"
        )
        # shared ledger dump (includes farm logs)
        (out_dir / "shared_memory.json").write_text(
            json.dumps(self.shared_ledger.events, indent=2), encoding="utf-8"
        )
