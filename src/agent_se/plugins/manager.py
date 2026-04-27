from __future__ import annotations

from typing import Iterable

from agent_se.models import Task
from agent_se.plugins.base import Plugin
from agent_se.plugins.cfdml import CFDMLPlugin


class PluginManager:
    def __init__(self, plugins: Iterable[Plugin] | None = None):
        base_plugins = list(plugins or [])
        if not any(getattr(p, "name", "") == "cfdml" for p in base_plugins):
            base_plugins.append(CFDMLPlugin())
        self.plugins = base_plugins

    def process_tasks(self, tasks: list[Task]) -> list[Task]:
        output = tasks
        for plugin in self.plugins:
            output = plugin.on_tasks_created(output)
        return output
