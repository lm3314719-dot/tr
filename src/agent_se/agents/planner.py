from __future__ import annotations

from agent_se.models import Task


class PlannerAgent:
    def plan(self, goal: str) -> list[Task]:
        seeds = [
            f"Analizzare goal: {goal}",
            "Creare struttura progetto",
            "Implementare test e pipeline",
            "Verificare qualità e bug fixing",
        ]
        return [Task(id=f"task-{i+1}", description=d) for i, d in enumerate(seeds)]
