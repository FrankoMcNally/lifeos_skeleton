from pathlib import Path
import csv, sys
from subprocess import run, PIPE

def test_digital_years_added(tmp_path: Path):
    m = tmp_path / "metrics.csv"
    m.write_text(
        "world,generation,population,genetic_diversity,avg_energy\n"
        "baseline,0,10,0.3,50.0\n"
        "baseline,3,10,0.2,55.0\n",
        encoding="utf-8"
    )
    tool = Path(__file__).resolve().parents[1] / "tools" / "add_digital_years.py"
    assert tool.exists(), "tools/add_digital_years.py missing"
    proc = run([sys.executable, str(tool), str(m), "--gen-years", "20"], stdout=PIPE, stderr=PIPE, text=True)
    assert proc.returncode == 0, proc.stderr

    with m.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert "digital_years" in reader.fieldnames
        assert rows[0]["digital_years"] == "0"
        assert rows[1]["digital_years"] == "60"
