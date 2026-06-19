#!/bin/bash
set -e

# Load .env
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

if [ -z "$GOOGLE_API_KEY" ]; then
    echo ""
    echo "  ERROR: GOOGLE_API_KEY is not set."
    echo "  Create a .env file:  cp .env.example .env"
    echo "  Get a key at:        https://aistudio.google.com/api-keys"
    echo ""
    exit 1
fi

echo ""
echo "  Killing any existing processes on ports 8000-8004..."
lsof -ti:8000,8001,8002,8003,8004 | xargs kill -9 2>/dev/null || true

export GOOGLE_GENAI_USE_VERTEXAI=False

AGENTS_DIR="$(pwd)/agents"

echo "  Starting Researcher  → port 8001"
GOOGLE_API_KEY=$GOOGLE_API_KEY GOOGLE_GENAI_USE_VERTEXAI=False \
    adk api_server --port 8001 --host 0.0.0.0 "$AGENTS_DIR/researcher" &
PID_RESEARCHER=$!

echo "  Starting Judge       → port 8002"
GOOGLE_API_KEY=$GOOGLE_API_KEY GOOGLE_GENAI_USE_VERTEXAI=False \
    adk api_server --port 8002 --host 0.0.0.0 "$AGENTS_DIR/judge" &
PID_JUDGE=$!

echo "  Starting Content Builder → port 8003"
GOOGLE_API_KEY=$GOOGLE_API_KEY GOOGLE_GENAI_USE_VERTEXAI=False \
    adk api_server --port 8003 --host 0.0.0.0 "$AGENTS_DIR/content_builder" &
PID_CONTENT=$!

echo "  Waiting for sub-agents to be ready..."
sleep 4

echo "  Starting Orchestrator (ADK Web UI) → port 8000"
GOOGLE_API_KEY=$GOOGLE_API_KEY GOOGLE_GENAI_USE_VERTEXAI=False \
    adk web --port 8000 --host 0.0.0.0 "$AGENTS_DIR" &
PID_ORCH=$!

echo ""
echo "  ✅ All agents running!"
echo "     Researcher:     http://localhost:8001"
echo "     Judge:          http://localhost:8002"
echo "     Content Builder:http://localhost:8003"
echo "     ADK Web UI:     http://localhost:8000  ← Open this"
echo ""
echo "  Press Ctrl+C to stop all agents."
echo ""

trap "echo '  Stopping...'; kill $PID_RESEARCHER $PID_JUDGE $PID_CONTENT $PID_ORCH 2>/dev/null; exit" INT TERM
wait
