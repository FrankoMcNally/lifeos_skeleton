"""
LifeOS package
DNA-inspired framework for simulating digital beings.
"""

# Re-export modules so they are accessible with just `import lifeos`
from . import genome
from . import lineage
from . import traits
from . import policy
from . import multiverse
from . import prime_map
from . import reproduction
from . import artifacts
from . import metrics
from . import vault

__all__ = [
    "genome",
    "lineage",
    "traits",
    "policy",
    "multiverse",
    "prime_map",
    "reproduction",
    "artifacts",
    "metrics",
    "vault",
]
