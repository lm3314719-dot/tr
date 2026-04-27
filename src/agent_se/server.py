from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from agent_se.llm import ChatRequest, LLMGateway
from agent_se.memory import ProjectMemory
from agent_se.orchestrator import EngineeringOrchestrator


class RunRequest(BaseModel):
    goal: str = Field(min_length=3)
    project_dir: str = Field(default="./workspace")
    max_iterations: int = Field(default=20, ge=1, le=500)


class ChatIn(BaseModel):
    prompt: str = Field(min_length=1)
    model: str
    api_key: str | None = None
    base_url: str = "https://integrate.api.nvidia.com/v1"


app = FastAPI(title="DevForge Pro", version="2.0.0")
web_dir = Path(__file__).parent / "web"
app.mount("/assets", StaticFiles(directory=web_dir), name="assets")
llm = LLMGateway()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/run")
def run_engineering(request: RunRequest) -> dict:
    orchestrator = EngineeringOrchestrator(
        project_dir=request.project_dir,
        max_iterations=request.max_iterations,
    )
    reports = orchestrator.run(request.goal)
    memory = ProjectMemory(Path(request.project_dir) / ".se-agent" / "memory.json").snapshot()
    return {
        "reports": [r.__dict__ for r in reports],
        "memory": memory,
    }


@app.get("/api/memory")
def read_memory(project_dir: str = "./workspace") -> dict:
    memory_path = Path(project_dir) / ".se-agent" / "memory.json"
    if not memory_path.exists():
        raise HTTPException(status_code=404, detail="Memoria non trovata")
    return ProjectMemory(memory_path).snapshot()


@app.post("/api/chat")
async def chat(data: ChatIn) -> dict[str, str]:
    content = await llm.complete(
        ChatRequest(
            prompt=data.prompt,
            model=data.model,
            api_key=data.api_key,
            base_url=data.base_url,
        )
    )
    return {"content": content}


@app.get("/")
def root() -> FileResponse:
    return FileResponse(web_dir / "index.html")
