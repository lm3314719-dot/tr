from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from agent_se.models import Task


class Plugin(Protocol):
    name: str

    def on_tasks_created(self, tasks: list[Task]) -> list[Task]:
        ...


@dataclass
class NoOpPlugin:
    name: str = "noop"

    def on_tasks_created(self, tasks: list[Task]) -> list[Task]:
        return tasks
