from __future__ import annotations

from pathlib import Path


class FileManager:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)
        self.project_dir.mkdir(parents=True, exist_ok=True)

    def write(self, relative_path: str, content: str) -> Path:
        target = self.project_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def read(self, relative_path: str) -> str:
        return (self.project_dir / relative_path).read_text(encoding="utf-8")

    def exists(self, relative_path: str) -> bool:
        return (self.project_dir / relative_path).exists()
