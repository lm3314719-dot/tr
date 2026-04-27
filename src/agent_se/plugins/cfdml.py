from __future__ import annotations

from agent_se.models import Task


class CFDMLPlugin:
    name = "cfdml"

    def on_tasks_created(self, tasks: list[Task]) -> list[Task]:
        ids = {t.id for t in tasks}
        if "cfdml-validate" not in ids:
            tasks.append(
                Task(
                    id="cfdml-validate",
                    description="Validare pipeline CFD/ML (dataset, solver, metrica)",
                )
            )
        return tasks
