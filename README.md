# Schema Drift Detector

Compares a baseline CSV with a current CSV and reports structural and statistical drift.

[Research notes](docs/RESEARCH.md) · [Architecture](docs/ARCHITECTURE.md) · [Execution record](docs/RESULTS.md) · [Project site](docs/index.html)

---

## Research context

Can baseline-versus-current comparisons identify meaningful dataset changes while limiting false alerts?

The repository provides an inspectable implementation of **production schema/statistical drift**. It is an exploratory engineering project; broader effectiveness and practical deployment require further study.

## Implemented capabilities

- added and removed columns
- inferred dtype changes
- numeric values moving outside the baseline range
- new categorical values
- cardinality changes

## Architecture

```mermaid
flowchart LR
    A["current.csv"] --> B["detect_drift.py"]
    B --> C["drift.json"]
```

The diagram is a simplified view of the supplied implementation. Detailed modules and interface assumptions are in [architecture notes](docs/ARCHITECTURE.md).

## Run locally

**Environment:** Python 3.11+ is the documented baseline. Install optional services or hardware drivers when required. Dependencies: pandas, numpy.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

Run the following commands from the repository root:

```bash
python src/detect_drift.py sample/baseline.csv sample/current.csv --output outputs/drift.json
```

**Input:** `sample/current.csv`, `sample/baseline.csv`

## Results

**Executed locally** with the included input files. This is an implementation check, not an independently validated benchmark.

![Output from the local execution](assets/result.svg)


**Execution evidence:** [Full command transcript](results/execution.txt) · [Inputs and checksums](results/execution.json)

**Saved outputs**

- [`drift.json`](results/artifacts/drift.json)

The values above come from the bundled fixtures. Model scores, simulated costs, and resource-use estimates should not be interpreted as real-world deployment results.

## Source structure

- [`src/detect_drift.py`](src/detect_drift.py)

Documentation is in [`docs/`](docs/). Bundled inputs remain in their original folders. The original project instructions are archived in [`docs/ORIGINAL_README.md`](docs/ORIGINAL_README.md).

## Limits and next research steps

- Results shown here are from local bundled inputs; they are not published research findings or evidence of external deployment.
- Validate domain assumptions and compare against a documented baseline before making performance or reliability claims.
- Extend testing to larger, independently sourced datasets and report reproducibility, failures and relevant ethical risks.

For the methodology and evaluation design, see [the research brief](docs/RESEARCH.md).

## License

See [`LICENSE`](LICENSE). No affiliation, patent, publication, production deployment or independent endorsement is implied.
