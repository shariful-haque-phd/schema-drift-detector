# Schema Drift Detector

Compares a baseline CSV with a current CSV and reports structural and statistical drift.

## Detects
- added and removed columns
- inferred dtype changes
- numeric values moving outside the baseline range
- new categorical values
- cardinality changes

## Usage
```bash
pip install -r requirements.txt
python src/detect_drift.py sample/baseline.csv sample/current.csv --output outputs/drift.json
```

The tool is intentionally deterministic and easy to add to a data pipeline or CI job.
