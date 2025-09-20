# Reproducibility — LifeOS

## Save for every run & world
- `config.yaml` (exact file used)
- `seed.txt` (single integer)
- `metrics.csv` (standard columns; one row per generation)
- `lineage.json` (parent→child edges, agent traits)
- `artifact_vault/*.jsonl`
- `logs/run.log`
- `requirements.txt` (`pip freeze`)
- Python version & OS

## Naming
`runs/EXP_YYYYMMDD_HHMM_<experiment_name>/<world_name>/...`

## Determinism
- Set and log RNG seed(s).
- Avoid hidden randomness; pass RNG explicitly where possible.

## Minimal Smoke Test
- `population_size: 50`, `generations: 20`
- Expect: metrics, lineage, logs present and non-empty.
