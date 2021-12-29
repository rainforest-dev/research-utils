from typing import Union
import os
from pathlib import Path
from mlflow.tracking.client import MlflowClient
from research_utils.typing import PathLike
from research_utils.decorators.logging import logger, Logging_Level


@logger(level=Logging_Level.INFO, transform=lambda path: f'Artifacts is downloaded at {path}')
def download_artifacts(run_id: str,
                       remote_path: Union[str, Path],
                       local_path: Union[str, Path],
                       client: MlflowClient = MlflowClient(),
                       no_cached=False) -> PathLike:
  if os.path.exists(local_path) and no_cached:
    os.remove(Path(local_path, remote_path))
  os.makedirs(local_path, exist_ok=True)
  return client.download_artifacts(run_id=run_id, path=remote_path, dst_path=local_path)