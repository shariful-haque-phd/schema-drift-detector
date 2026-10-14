# Architecture — Schema Drift Detector

```mermaid
flowchart LR
    A["current.csv"] --> B["detect_drift.py"]
    B --> C["drift.json"]
```

## Inputs

- `sample/current.csv`
- `sample/baseline.csv`

## Source files

- `src/detect_drift.py`

## Output

- `results/artifacts/drift.json`

This representation is intended for source navigation. It does not imply a production deployment or undisclosed components. The editable diagram is available as [`architecture.mmd`](architecture.mmd).
