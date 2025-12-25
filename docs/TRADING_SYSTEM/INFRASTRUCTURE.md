# Infrastructure and Deployment

## Local
- Docker Compose dev stack; single-node orchestrator
- `.env` and secrets via local vault/store

## Cloud
- Containerized services (e.g., Kubernetes, ECS) with autoscaling
- Managed time-series storage and message bus
- Centralized secrets and IAM roles with least privilege

## IaC
- Define resources via Terraform/Pulumi
- Environments: dev, staging, prod with drift detection

## Observability
- Logs, metrics, traces shipped to a managed backend
- Dashboards and SLO/SLA definitions with alerts


