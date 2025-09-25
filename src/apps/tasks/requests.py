from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """Request model for creating a new task."""

    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(
        None, max_length=500, description="Task description"
    )
    done: bool = Field(default=False, description="Task completion status")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("description")
    @classmethod
    def description_must_not_be_empty_string(cls, v):
        if v is not None and not v.strip():
            return None
        return v.strip() if v else None


class TaskUpdate(BaseModel):
    """Request model for updating a task."""

    title: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Task title"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Task description"
    )
    done: Optional[bool] = Field(None, description="Task completion status")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty")
        return v.strip() if v else None

    @field_validator("description")
    @classmethod
    def description_must_not_be_empty_string(cls, v):
        if v is not None and not v.strip():
            return None
        return v.strip() if v else None

    def has_updates(self) -> bool:
        """Check if at least one field is being updated."""
        return any(
            [
                self.title is not None,
                self.description is not None,
                self.done is not None,
            ]
        )
