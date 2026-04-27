# DevForge Pro / se-agent

Piattaforma completa di **Software Engineering multi-agent** con backend Python + frontend HTML/CSS/JS pronta per browser.

## Include

- 📁 Gestione file reale (filesystem project dir)
- 🔁 Loop multi-step con stop intelligente (`max_iterations` + task completion)
- 🧩 Plugin system con plugin `CFDML`
- 🧪 Test automatici (`pytest`)
- 🐳 Docker + GitHub Actions CI
- 💾 Memoria persistente progetto (`.se-agent/memory.json`)
- ⚡ Multi-agent workflow (planner + coder + debugger)
- 🌐 Dashboard browser-based (`FastAPI` + UI moderna)

## Sicurezza

Le API key **non sono hardcoded** nel codice. Inseriscile in UI runtime o via variabili ambiente/proxy backend.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Eseguire workflow da CLI

```bash
se-agent run --project-dir ./workspace --goal "Crea una API REST con test"
```

## Avviare piattaforma web

```bash
se-agent serve --host 0.0.0.0 --port 8000
# poi apri http://localhost:8000
```

## Test

```bash
pytest -q
```

## Docker

```bash
docker build -t devforge-pro .
docker run --rm -p 8000:8000 -v "$PWD":/app devforge-pro
```


## File unico scaricabile

È disponibile una versione **all-in-one** in un solo file HTML:

- `dist/devforge_pro_standalone.html`

Aprilo direttamente nel browser oppure condividilo/scaricalo come file unico.
