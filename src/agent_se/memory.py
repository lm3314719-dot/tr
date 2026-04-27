from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProjectMemory:
    def __init__(self, memory_path: str | Path):
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.memory_path.exists():
            self._save({"iterations": [], "notes": [], "tasks": []})

    def _load(self) -> dict[str, Any]:
        return json.loads(self.memory_path.read_text(encoding="utf-8"))

    def _save(self, data: dict[str, Any]) -> None:
        self.memory_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def append_iteration(self, summary: str, errors: list[str]) -> None:
        data = self._load()
        data["iterations"].append({"summary": summary, "errors": errors})
        self._save(data)

    def update_tasks(self, tasks: list[dict[str, Any]]) -> None:
        data = self._load()
        data["tasks"] = tasks
        self._save(data)

    def add_note(self, note: str) -> None:
        data = self._load()
        data["notes"].append(note)
        self._save(data)

    def snapshot(self) -> dict[str, Any]:
        return self._load()
