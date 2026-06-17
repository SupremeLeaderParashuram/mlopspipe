from dataclasses import dataclass, field
from typing import Any, Optional
import pandas as pd


@dataclass
class DatasetContext:
    """Central application state — every module reads and writes here."""
    dataset_id: Optional[str] = None
    source_files: list = field(default_factory=list)
    raw_data: Optional[Any] = None        # pd.DataFrame
    cleaned_data: Optional[Any] = None   # pd.DataFrame
    schema: Optional[dict] = None
    profile: Optional[dict] = None
    eda_report: Optional[dict] = None
    target_column: Optional[str] = None
    task_type: Optional[str] = None
    feature_config: Optional[dict] = None
    model_config: Optional[dict] = None
    training_results: Optional[dict] = None
    deployment_package: Optional[dict] = None
