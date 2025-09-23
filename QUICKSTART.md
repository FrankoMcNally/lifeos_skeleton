# Quickstart Guide – LifeOS Skeleton

This is the **short reference** for getting started quickly with LifeOS.  
For full details, see the main [README.md](README.md).

---

## 1. Install Dependencies

### Windows (PowerShell)

```powershell
py -m pip install -r requirements.txt
```

### Linux / macOS / Git Bash

```bash
python3 -m pip install -r requirements.txt
```

---

## 2. Verify Installation

### Windows (PowerShell)
```powershell
py -m pytest -v
```

### Linux / macOS
```bash
pytest -v
```

Expected: All tests should pass ✅

---

## 3. Run Your First Experiment

```powershell
py run_experiment.py --config configs/sample_small.yaml
```

Output: `runs/EXP_<timestamp>_sample_small/` with:  
- `metrics.csv` → diversity & energy per generation  
- `lineage.json` → ancestry tree

---

## 4. Next Steps

- Edit configs in `/configs` to design new worlds  
- Explore traits, mutation rates, and policies  
- Track population survival and adaptation across generations  

---

## Common Issues

- **`pytest` not found on Windows:** Use `py -m pytest -v` instead.  
- **Config file not found:** Ensure the repo is in the updated **single-root layout** with `configs/` directly inside the root.  
- **Empty runs directory:** Check that your config file is valid and experiment executed without errors.  

---

🎯 That’s it — you’re up and running!
