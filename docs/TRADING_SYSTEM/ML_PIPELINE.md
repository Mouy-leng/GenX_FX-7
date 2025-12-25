# ML Pipeline

## Data
- Sources: broker streams, market data vendors
- Storage: time-series DB/object storage; feature store abstractions
- Validation: schema, drift checks, data quality gates

## Training
- Offline training with experiment tracking
- Cross-validation, walk-forward, regime-aware evaluation
- Hyperparameter search; reproducible seeds and artifacts

## Model Registry
- Versioned models with metadata (data snapshot, metrics, features)
- Promotion criteria and review workflow

## Serving
- Batch (signals every interval) and streaming (tick-level)
- Canary deploy and rollback policies

## Monitoring
- Performance, drift, and stability metrics
- Alert thresholds and auto-disable on breach


