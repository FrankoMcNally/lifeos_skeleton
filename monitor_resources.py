#!/usr/bin/env python3
"""
Monitor system resource usage during LifeOS stress tests.
Logs CPU, memory, and disk usage periodically into runs/system_monitor.csv.
Optionally plots a graph if matplotlib is available.

Usage:
  py monitor_resources.py --interval 2 --duration 600
"""

import argparse
import csv
import time
from datetime import datetime
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=int, default=2, help="Seconds between samples")
    ap.add_argument("--duration", type=int, default=600, help="Total duration to monitor (s)")
    ap.add_argument("--out", default="runs/system_monitor.csv", help="Output CSV path")
    args = ap.parse_args()

    try:
        import psutil
    except ImportError:
        print("psutil not installed. Install with: pip install psutil")
        return

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["timestamp", "cpu_percent", "mem_percent", "disk_percent"]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        start_time = time.time()
        while time.time() - start_time < args.duration:
            try:
                row = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "cpu_percent": psutil.cpu_percent(interval=None),
                    "mem_percent": psutil.virtual_memory().percent,
                    "disk_percent": psutil.disk_usage("/").percent,
                }
                writer.writerow(row)
                f.flush()
                print(row)  # live feedback
                time.sleep(args.interval)
            except KeyboardInterrupt:
                print("Monitoring stopped by user.")
                break
            except Exception as e:
                print(f"Error sampling resources: {e}")
                time.sleep(args.interval)

    print(f"System monitor log saved → {out_path}")

    # Optional: auto-plot if matplotlib available
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        df = pd.read_csv(out_path)
        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["cpu_percent"], label="CPU %")
        plt.plot(df["timestamp"], df["mem_percent"], label="Memory %")
        plt.plot(df["timestamp"], df["disk_percent"], label="Disk %")
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Time")
        plt.ylabel("Usage (%)")
        plt.title("System Resource Monitoring")
        plt.legend()
        plt.tight_layout()
        plot_path = out_path.with_suffix(".png")
        plt.savefig(plot_path)
        plt.close()
        print(f"System monitor plot saved → {plot_path}")
    except Exception:
        pass

if __name__ == "__main__":
    main()
