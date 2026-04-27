from __future__ import annotations

import argparse
import json

import uvicorn

from agent_se.orchestrator import EngineeringOrchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agente Software Engineering Completo")
    sub = parser.add_subparsers(dest="command", required=False)

    run = sub.add_parser("run", help="Esegue il workflow multi-agent")
    run.add_argument("--project-dir", required=True, help="Directory progetto target")
    run.add_argument("--goal", required=True, help="Obiettivo da completare")
    run.add_argument("--max-iterations", type=int, default=20)

    serve = sub.add_parser("serve", help="Avvia la piattaforma web browser-based")
    serve.add_argument("--host", default="0.0.0.0")
    serve.add_argument("--port", type=int, default=8000)

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command in (None, "run"):
        if not getattr(args, "project_dir", None) or not getattr(args, "goal", None):
            raise SystemExit("Per eseguire il workflow usa: se-agent run --project-dir ... --goal ...")
        orchestrator = EngineeringOrchestrator(
            project_dir=args.project_dir,
            max_iterations=args.max_iterations,
        )
        reports = orchestrator.run(goal=args.goal)
        print(json.dumps([r.__dict__ for r in reports], indent=2, ensure_ascii=False))
        return

    if args.command == "serve":
        uvicorn.run("agent_se.server:app", host=args.host, port=args.port, reload=False)


if __name__ == "__main__":
    main()
