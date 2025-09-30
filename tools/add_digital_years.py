#!/usr/bin/env python3
import argparse, csv, sys, pathlib

def add_digital_years(csv_path, gen_years=20, in_place=True, backup=True):
    p = pathlib.Path(csv_path)
    if not p.exists():
        print(f"ERROR: metrics file not found: {p}", file=sys.stderr)
        sys.exit(1)

    # read & augment
    with p.open("r", newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        header = next(r)
        if "generation" not in header:
            print("ERROR: 'generation' column not found in metrics.csv", file=sys.stderr)
            sys.exit(2)
        if "digital_years" not in header:
            header = header + ["digital_years"]
        gen_idx = header.index("generation") if "generation" in header else None
        rows = [header]
        for row in r:
            try:
                g = int(row[gen_idx])
                dy = g * gen_years
                rows.append(row + [str(dy)])
            except Exception:
                rows.append(row + [""])

    out_path = p
    if not in_place:
        out_path = p.with_name(p.stem + "_with_years.csv")

    if in_place and backup:
        bak = p.with_suffix(p.suffix + ".bak")
        if not bak.exists():
            p.replace(bak)
            with out_path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(rows)
            print(f"Wrote: {out_path}\nBackup: {bak}")
            return

    with out_path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)
    print(f"Wrote: {out_path}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Add digital_years to metrics.csv")
    ap.add_argument("metrics_csv", help="Path to metrics.csv")
    ap.add_argument("--gen-years", type=int, default=20)
    ap.add_argument("--no-in-place", action="store_true")
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args()
    add_digital_years(
        args.metrics_csv,
        gen_years=args.gen_years,
        in_place=not args.no_in_place,
        backup=not args.no_backup
    )
