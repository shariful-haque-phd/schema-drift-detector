import argparse, json
from pathlib import Path
import pandas as pd

def compact_type(s: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(s): return "numeric"
    if pd.api.types.is_bool_dtype(s): return "boolean"
    text=s.dropna().astype(str).str.strip()
    date_like=text.str.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}")
    if len(text) and date_like.mean() > 0.95:
        parsed=pd.to_datetime(text,errors="coerce")
        if parsed.notna().mean() > 0.95: return "datetime"
    return "string"

def compare(base: pd.DataFrame, cur: pd.DataFrame) -> dict:
    bcols, ccols = set(base.columns), set(cur.columns)
    out = {"added_columns": sorted(ccols-bcols), "removed_columns": sorted(bcols-ccols),
           "changed_columns": {}}
    for col in sorted(bcols & ccols):
        bt, ct = compact_type(base[col]), compact_type(cur[col])
        item = {}
        if bt != ct:
            item["type_change"] = {"baseline": bt, "current": ct}
        if bt == ct == "numeric":
            b = pd.to_numeric(base[col], errors="coerce").dropna()
            c = pd.to_numeric(cur[col], errors="coerce").dropna()
            if not b.empty and not c.empty:
                outside = int(((c < b.min()) | (c > b.max())).sum())
                if outside:
                    item["range_drift"] = {
                        "baseline_min": float(b.min()), "baseline_max": float(b.max()),
                        "current_min": float(c.min()), "current_max": float(c.max()),
                        "outside_baseline_count": outside
                    }
        elif bt == ct == "string":
            bvals = set(base[col].dropna().astype(str).unique())
            cvals = set(cur[col].dropna().astype(str).unique())
            new = sorted(cvals - bvals)
            if new:
                item["new_categories_preview"] = new[:20]
                item["new_category_count"] = len(new)
            if len(bvals) != len(cvals):
                item["cardinality"] = {"baseline": len(bvals), "current": len(cvals)}
        if item:
            out["changed_columns"][col] = item
    out["drift_detected"] = bool(out["added_columns"] or out["removed_columns"] or out["changed_columns"])
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument("baseline")
    p.add_argument("current")
    p.add_argument("--output", default="drift.json")
    a = p.parse_args()
    result = compare(pd.read_csv(a.baseline), pd.read_csv(a.current))
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__": main()
