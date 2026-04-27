from __future__ import annotations

import json

from agent_se.orchestrator import EngineeringOrchestrator


def test_orchestrator_runs_and_persists_memory(tmp_path):
    project_dir = tmp_path / "proj"
    orchestrator = EngineeringOrchestrator(project_dir=project_dir, max_iterations=10)

    reports = orchestrator.run(goal="Crea agente completo")

    assert reports
    memory_file = project_dir / ".se-agent" / "memory.json"
    assert memory_file.exists()

    data = json.loads(memory_file.read_text(encoding="utf-8"))
    assert len(data["tasks"]) >= 4
    assert len(data["iterations"]) >= 1


def test_cfdml_plugin_task_is_injected(tmp_path):
    orchestrator = EngineeringOrchestrator(project_dir=tmp_path / "proj2")
    tasks = orchestrator.plugins.process_tasks(orchestrator.planner.plan("x"))
    assert any(t.id == "cfdml-validate" for t in tasks)
