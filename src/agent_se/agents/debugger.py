from __future__ import annotations

from agent_se.models import Task


class DebuggerAgent:
    def debug(self, task: Task) -> list[str]:
        if "bug" in task.description.lower():
            return [f"Controllo approfondito richiesto per {task.id}"]
        return []
