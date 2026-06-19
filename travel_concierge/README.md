# ✈️ Travel Concierge — Multi-Agent Demo

A simplified, local-first version of the [Google ADK Travel Concierge sample](https://github.com/google/adk-samples/tree/main/python/agents/travel-concierge).

**No Google Cloud account needed** — just a free Gemini API key.

## Architecture

```
travel_concierge (root — RouterAgent)
├── 🌍 inspiration_agent   → destination ideas, activities (google_search)
├── 🗓️ planning_agent      → flights, hotels, itinerary (mocked tools)
│   └── 📋 itinerary_agent → compiles final itinerary (AgentTool)
└── 🧳 in_trip_agent       → real-time help during the trip
```

### ADK concepts demonstrated

| Concept | Where |
|---|---|
| LLM-based routing | `root_agent` delegates to sub_agents by intent |
| `google_search` tool | `inspiration_agent`, `in_trip_agent` |
| Mocked Python tools | `search_flights`, `search_hotels`, etc. |
| `AgentTool` | `itinerary_agent` called as a tool from `planning_agent` |
| `session.state` memory | `memorize` / `recall` tools across all agents |
| `disallow_transfer_*` | `itinerary_agent` only outputs its schema |

## Setup

```bash
# 1. Install ADK
pip install google-adk

# 2. Set your API key (get one free at https://aistudio.google.com/api-keys)
cp .env.example .env
# Edit .env and paste your key

# 3. Load env vars
export $(grep -v '^#' .env | xargs)
```

## Run

```bash
# Interactive CLI
adk run travel_concierge

# Web UI (recommended)
adk web .
# Open http://localhost:8000 → select 'travel_concierge'
```

## Try these prompts

```
I want to plan a beach vacation but I'm not sure where to go yet.
```
```
I've decided on Bali! I'm flying from Mumbai on Dec 15, returning Dec 22.
```
```
I'm at the airport now, can you check my flight AI100 status?
```

## Files to explore

| File | What it teaches |
|---|---|
| `agent.py` | Root agent routing by intent via `sub_agents` |
| `sub_agents/inspiration/agent.py` | Tool-using agent with `google_search` |
| `sub_agents/planning/agent.py` | Multi-step workflow + `AgentTool` |
| `sub_agents/in_trip/agent.py` | Stateful agent using session memory |
| `tools/memory.py` | Reading/writing `session.state` from tools |
| `tools/flights.py` | Mocked tools — no external API needed |
| `tools/hotels.py` | Mocked tools — no external API needed |
