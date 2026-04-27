from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    id: str
    description: str
    status: str = "pending"


@dataclass
class FileChange:
    path: str
    content: str


@dataclass
class IterationReport:
    iteration: int
    summary: str
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
