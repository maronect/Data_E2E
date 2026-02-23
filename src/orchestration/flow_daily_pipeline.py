import os
import subprocess
from pathlib import Path

from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

REPO_ROOT = Path(__file__).resolve().parents[2]   # ~/engdados
DBT_DIR = REPO_ROOT / "dbt" / "engdados_dbt"      # ~/engdados/dbt/engdados_dbt


@task(
    name="Run ingestion (Python)",
    retries=2,
    retry_delay_seconds=10,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(minutes=5),
)
def run_ingestion():
    # roda: python -m src.ingestion.run_ingestion
    cmd = ["python", "-m", "src.ingestion.run_ingestion"]
    print(f"[CMD] {' '.join(cmd)}  (cwd={REPO_ROOT})")
    subprocess.run(cmd, cwd=str(REPO_ROOT), check=True)


@task(name="dbt run", retries=1, retry_delay_seconds=5)
def dbt_run(select: str):
    cmd = ["dbt", "run", "--select", select]
    print(f"[CMD] {' '.join(cmd)}  (cwd={DBT_DIR})")
    subprocess.run(cmd, cwd=str(DBT_DIR), check=True)


@task(name="dbt test", retries=1, retry_delay_seconds=5)
def dbt_test(select: str):
    cmd = ["dbt", "test", "--select", select]
    print(f"[CMD] {' '.join(cmd)}  (cwd={DBT_DIR})")
    subprocess.run(cmd, cwd=str(DBT_DIR), check=True)


@flow(name="engdados_daily_pipeline")
def engdados_daily_pipeline():
    """
    Pipeline end-to-end:
      1) Ingestão (Python) -> lake (MinIO) + staging (Postgres)
      2) dbt run (silver + gold)
      3) dbt test (silver + gold)
    """
    run_ingestion()

    # Transformações
    dbt_run("silver")
    dbt_run("gold")

    # Qualidade
    dbt_test("silver")
    dbt_test("gold")


if __name__ == "__main__":
    engdados_daily_pipeline()
