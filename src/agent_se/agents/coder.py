from __future__ import annotations

from agent_se.file_manager import FileManager
from agent_se.models import FileChange, Task


class CoderAgent:
    def code(self, task: Task, files: FileManager) -> list[FileChange]:
        filename = f"artifacts/{task.id}.md"
        content = f"# {task.id}\n\n{task.description}\n\nStatus: completed\n"
        files.write(filename, content)
        task.status = "completed"
        return [FileChange(path=filename, content=content)]
