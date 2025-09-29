# lifeos/adam_eve_rules.py
from __future__ import annotations
import math
from typing import Dict, List, Tuple, Any

PHI = (1.0 + 5 ** 0.5) / 2.0  # golden ratio


# -------------------------
# Core Rule Helpers
# -------------------------
def allowed_generation(gen: int, allowed: Tuple[int, int]) -> bool:
    lo, hi = allowed
    return lo <= gen <= hi


def attraction_score(a_traits: Dict[str, float],
                     b_traits: Dict[str, float],
                     weights: Dict[str, float] | None = None) -> float:
    """
    Higher = more compatible. Uses similarity + small complementarity bonus.
    """
    if weights is None:
        weights = {
            "health": 1.4, "fertility": 1.6, "cooperation": 1.2,
            "curiosity": 1.0, "spirit": 0.6
        }
    score = 0.0
    for k, w in weights.items():
        if k in a_traits and k in b_traits:
            score += w * (1.0 - abs(a_traits[k] - b_traits[k]))  # similarity
    # complementarity nudge
    score += 0.3 * abs((a_traits.get("extroversion", 0.5) - 0.5) *
                       (b_traits.get("introversion", 0.5) - 0.5))
    return max(score, 0.0)


def kin_ok(ancestor_map: Dict[str, List[str]],
           a_id: str, b_id: str,
           min_distance: int = 2) -> bool:
    """
    Blocks incest. If agents share any ancestor within `min_distance` hops,
    return False. Keeps the rule simple & safe by default.
    """
    a_anc = set(ancestor_map.get(a_id, []))
    b_anc = set(ancestor_map.get(b_id, []))
    if not a_anc or not b_anc:
        return True
    return len(a_anc & b_anc) == 0


def under_pair_cap(pair_key: str,
                   children_count: Dict[str, int],
                   cap: int) -> bool:
    return children_count.get(pair_key, 0) < cap


# -------------------------
# Elder Assistance
# -------------------------
def elders_help(energy_by_id: Dict[str, float],
                gen_by_id: Dict[str, int],
                elder_gen: int,
                help_amount: float = 2.0,
                max_transfers: int = 5) -> None:
    """
    Elders (gen >= elder_gen) donate small energy to struggling young.
    """
    elders = [i for i, g in gen_by_id.items() if g >= elder_gen]
    needy = [i for i, e in energy_by_id.items() if e < 1.0]
    if not elders or not needy:
        return
    n = min(len(needy), max_transfers)
    for e_id, y_id in zip(elders[:n], needy[:n]):
        if energy_by_id.get(e_id, 0.0) > help_amount:
            energy_by_id[e_id] -= help_amount
            energy_by_id[y_id] = energy_by_id.get(y_id, 0.0) + help_amount


# -------------------------
# Pacing
# -------------------------
def golden_sleep(base_ms: int, generation: int) -> int:
    """
    Optional pacing to avoid CPU spikes: every ~10 gens, grow by PHI-1.
    """
    mult = (PHI - 1.0) ** (generation // 10)
    return max(1, int(round(base_ms * mult)))


# -------------------------
# Memory-Driven Extensions
# -------------------------
def memory_recent_partner(indiv_state: Any) -> int | None:
    """
    Look into an individual's RingMemory to recall their most recent partner.
    Returns partner_id or None if no record.
    """
    return indiv_state.memory.recall("partner", None)


def ledger_recent_events(shared_ledger: Any, n: int = 5) -> List[Dict[str, Any]]:
    """
    Get the most recent world events from the shared ledger.
    """
    return shared_ledger.recent(n)


def avoid_repeat_pairing(indiv_state: Any, candidate_id: int) -> bool:
    """
    Example rule: check memory to avoid re-pairing with the same candidate
    multiple times in quick succession.
    """
    last_partner = memory_recent_partner(indiv_state)
    return last_partner != candidate_id
