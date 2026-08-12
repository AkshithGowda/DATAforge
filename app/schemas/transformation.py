from pydantic import BaseModel
from typing import Optional, List, Dict


class TransformationRequest(BaseModel):

    dataset_id: str

    rename_columns: Optional[Dict[str, str]] = None

    drop_columns: Optional[List[str]] = None

    select_columns: Optional[List[str]] = None

    filter_condition: Optional[str] = None

    sort_column: Optional[str] = None

    sort_ascending: bool = True