# GDG Workshop — Building Multi-Agent AI with Google ADK

This project was developed during a Google Developer Groups (GDG) workshop on building AI applications with Google's Agent Development Kit (ADK) and Gemini API.

## Overview

This repository demonstrates multi-agent AI systems where specialized agents collaborate through structured workflows and intelligent task delegation. The labs cover agent orchestration, structured outputs, memory management, and agent-to-agent communication.

## Features

- Multi-agent architecture using Google ADK
- Agent-to-agent communication
- Sequential and looped workflow execution
- Structured outputs with Pydantic
- Gemini-powered reasoning and content generation
- Intent routing and cross-agent memory
- Modular, extensible project structure

## Labs

### Lab 1 — Course Creation Pipeline (`agents/`)

A self-correcting research pipeline: Researcher → Judge → Content Builder.
Teaches `LoopAgent`, `SequentialAgent`, structured Pydantic output, and A2A protocol.

```
agents/
├── researcher/agent.py       ← Step 3: you write this
├── judge/agent.py            ← Step 4: you write this
├── content_builder/agent.py  ← Step 6: you write this
└── orchestrator/agent.py     ← Steps 7–10: you write this
solution/                     ← completed code for reference
```

### Lab 2 — Travel Concierge (`travel_concierge/`)

A conversational travel agent routing across Inspiration, Planning, and In-Trip specialists.
Teaches intent routing, `AgentTool`, and cross-agent session memory.

```
travel_concierge/
├── agent.py                        ← root agent (intent router)
├── sub_agents/inspiration/agent.py
├── sub_agents/planning/agent.py
└── sub_agents/in_trip/agent.py
```

## Tech Stack

- Python
- Google Agent Development Kit (ADK)
- Gemini API
- Pydantic

## Setup

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install ADK
pip install google-adk

# 3. Get a free API key at https://aistudio.google.com/api-keys
cp .env.example .env
# Edit .env and paste your key

# 4. Load env vars
export $(grep -v '^#' .env | xargs)
```

## Running

**Lab 1 — all agents at once:**

```bash
chmod +x run_local.sh && ./run_local.sh
# Opens ADK Web UI at http://localhost:8000
```

**Lab 1 — on Windows:**

```powershell
# From PowerShell
.\run_local.ps1

# Or double-click run_local.bat
```

**Lab 2 — travel concierge:**

```bash
adk web travel_concierge
# Opens ADK Web UI at http://localhost:8000
```

**Any single agent (for testing):**

```bash
adk run agents/researcher
adk web agents/judge --port 8001
```

## Acknowledgements

Created during a Google Developer Groups (GDG) workshop focused on building AI-powered applications using Google ADK and Gemini.
