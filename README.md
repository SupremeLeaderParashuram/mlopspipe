# ML Pipeline

> Any input data source should be transformable into a validated,
> ML-ready dataset package with minimal user expertise.

## Macro Architecture

```
GUI Layer → Workflow Controller → Dataset Context
                                        │
                         ┌─────────────┼─────────────┐
                         ▼             ▼             ▼
                      Import       Analysis      ML Pipeline
                      Layer         Layer          Layer
```

## Build Order

| # | Module |
|---|--------|
| 1 | DatasetContext |
| 2 | ImportManager |
| 3 | SchemaDetector |
| 4 | ProfileEngine |
| 5 | EDAEngine |
| 6 | CleaningPipeline |
| 7 | FeatureEngine |
| 8 | TaskDetector |
| 9 | ModelRecommender |
| 10 | TrainingEngine |
| 11 | DeploymentEngine |

## Module Map

| Folder | Contents |
|--------|----------|
| `context/` | DatasetContext — application RAM |
| `import/` | ImportManager + 7 adapters (CSV, Excel, JSON, XML, TLog, Image, Zip) |
| `analysis/` | SchemaDetector, ProfileEngine, StatisticalEngine, CorrelationEngine, DistributionEngine, DriftEngine, ImbalanceEngine |
| `preprocessing/` | CleaningPipeline, ValidationEngine |
| `features/` | EncodingEngine, ScalingEngine, SelectionEngine, TelemetryFeatureEngine |
| `models/` | TaskDetector, ModelRecommender, ModelRegistry |
| `training/` | TrainingEngine, EvaluationEngine, OptimizationEngine |
| `deployment/` | DeploymentExporter → model.joblib / schema.json / config.json / requirements.txt |
| `storage/` | SQLAlchemy metadata DB (SQLite) + Parquet dataset storage |
| `workflow/` | WorkflowController — stage gating |
| `plugins/` | OllamaPlugin (NL→config), MissionPlannerPlugin (MAVLink/TLOG) |
| `gui/` | Page stubs — no business logic |

## Storage Strategy

- **Metadata**: SQLite via SQLAlchemy (`datasets`, `projects`, `runs`, `models` tables)
- **Datasets**: Parquet — faster, compressed, typed, large-dataset friendly

## Quick Start

```bash
pip install -r requirements.txt
```

```python
from context import DatasetContext
from import   import ImportManager
from analysis import SchemaDetector, ProfileEngine
from preprocessing import CleaningPipeline, ValidationEngine
from features  import EncodingEngine, ScalingEngine
from models    import TaskDetector, ModelRecommender
from training  import TrainingEngine, EvaluationEngine
from deployment import DeploymentExporter
from workflow  import WorkflowController

ctx = DatasetContext()
wf  = WorkflowController()

ctx.raw_data = ImportManager().load("data.csv")
wf.advance("analyze")

ctx.schema  = SchemaDetector().detect(ctx.raw_data)
ctx.profile = ProfileEngine().profile(ctx.raw_data)
wf.advance("clean")

ctx.cleaned_data = CleaningPipeline().run(ctx.raw_data)
wf.advance("engineer")

encoded = EncodingEngine().encode(ctx.cleaned_data)
scaled  = ScalingEngine().scale(encoded)
wf.advance("train")

ctx.task_type = TaskDetector().detect(scaled, ctx.target_column)
model, metrics = TrainingEngine().train(scaled, ctx.target_column, ctx.task_type)
ctx.training_results = metrics
wf.advance("deploy")

DeploymentExporter().export(model, ctx.schema, {"task": ctx.task_type}, "output/")
```

## GUI

A full Tkinter desktop GUI is included — no browser required.

```bash
python main.py
```

### Pages

| Page | What it does |
|------|-------------|
| **Import** | Load CSV / Excel / JSON / XML / ZIP with a file browser |
| **Schema** | Detect and display column types in a sortable table |
| **EDA** | Profile, statistics, and distribution report |
| **Clean** | Drop duplicates, fill/drop nulls, remove constants |
| **Features** | One-hot / label encoding + Standard / MinMax / Robust scaling |
| **Models** | Enter target column, detect task, pick recommended model |
| **Train** | Fit model with live log output |
| **Results** | Metric cards (accuracy / F1 / RMSE / MAE / R²) |
| **Export** | Save model.joblib + schema.json + config.json + requirements.txt |

### Requirements (GUI only needs these)

```
pandas numpy scikit-learn scipy sqlalchemy pyarrow joblib openpyxl
```
