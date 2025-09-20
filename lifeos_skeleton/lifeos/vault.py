"""
Artifact vault read/write helpers.
"""
import json
from pathlib import Path
from .artifacts import Artifact

def write_artifact(path: Path, art: Artifact):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "kind": art.kind,
            "data": art.data,
            "agent_id": art.agent_id,
            "generation": art.generation,
        }) + "\n")
