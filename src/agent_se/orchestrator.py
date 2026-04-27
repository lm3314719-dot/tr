from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from agent_se.agents.coder import CoderAgent
from agent_se.agents.debugger import DebuggerAgent
from agent_se.agents.planner import PlannerAgent
from agent_se.file_manager import FileManager
from agent_se.memory import ProjectMemory
from agent_se.models import IterationReport
from agent_se.plugins.manager import PluginManager


class EngineeringOrchestrator:
    def __init__(self, project_dir: str | Path, max_iterations: int = 20):
        self.file_manager = FileManager(project_dir)
        self.memory = ProjectMemory(Path(project_dir) / ".se-agent" / "memory.json")
        self.planner = PlannerAgent()
        self.coder = CoderAgent()
        self.debugger = DebuggerAgent()
        self.plugins = PluginManager()
        self.max_iterations = max_iterations

    def run(self, goal: str) -> list[IterationReport]:
        tasks = self.plugins.process_tasks(self.planner.plan(goal))
        self.memory.update_tasks([asdict(t) for t in tasks])

        reports: list[IterationReport] = []
        iteration = 0

        while iteration < self.max_iterations:
            pending = [t for t in tasks if t.status != "completed"]
            if not pending:
                self.memory.add_note("Loop terminato: tutti i task completati")
                break

            iteration += 1
            task = pending[0]
            self.coder.code(task, self.file_manager)
            errors = self.debugger.debug(task)
            summary = f"Iterazione {iteration}: completato {task.id}"
            report = IterationReport(iteration=iteration, summary=summary, errors=errors)
            reports.append(report)
            self.memory.append_iteration(summary=summary, errors=errors)

            if errors:
                self.memory.add_note(f"Rilevati warning su {task.id}")

        if iteration >= self.max_iterations:
            self.memory.add_note("Loop terminato: raggiunto max_iterations")

        return reports
