from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskOut(BaseModel):
    """Response model for task data."""

    id: str
    title: str
    description: Optional[str]
    done: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
