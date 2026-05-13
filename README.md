# Deep Agents Workshop

A hands-on workshop covering Deep Agents, Deep Agents Deploy, and LangSmith evaluations.

| Part | Topic | Duration |
|------|-------|----------|
| **1** | Deep Agents: Harness, Filesystem, Tools, Subagents, Memory, Middleware, HITL, Skills | ~45 min |
| **2** | Deep Agents Deploy: Ship to LangSmith | ~10 min |
| **3** | LangSmith: Tracing, Datasets & Evaluations | ~20 min |

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

You'll need:

| Key | Where to get it |
|-----|----------------|
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) |
| `LANGSMITH_API_KEY` | [smith.langchain.com](https://smith.langchain.com) |
| `TAVILY_API_KEY` | [tavily.com](https://tavily.com) |

3. Start the notebook:

```bash
uv run jupyter notebook notebooks/workshop.ipynb
```

## Switching Models

The notebook uses `init_chat_model()` which supports any provider. Change the model in the setup cell:

```python
# OpenAI (default)
model = init_chat_model("openai:gpt-4.1-mini")

# Anthropic
model = init_chat_model("anthropic:claude-sonnet-4-20250514")

# Azure OpenAI
model = init_chat_model("azure_openai:gpt-4.1-mini", azure_deployment="your-deployment")

# AWS Bedrock
model = init_chat_model("bedrock:anthropic.claude-sonnet-4-20250514-v1:0")
```

Some providers need an extra package:

```bash
uv add langchain-anthropic   # Anthropic
uv add langchain-aws          # AWS Bedrock
```

## Deploy (Part 2)

Part 2 deploys your agent to LangSmith. This requires the `langgraph` CLI:

```bash
uv tool install deepagents-cli
uv tool install 'langgraph-cli[inmem]'
```

Your `LANGSMITH_API_KEY` must have deployment permissions (`lsv2_sk_...` service key, not a personal token).

## Project Structure

```
workshop/
├── notebooks/
│   └── workshop.ipynb          # Main workshop notebook
├── agents/
│   └── deep_agent/             # Deployable agent (used in Part 2)
│       ├── agent.py
│       ├── AGENTS.md
│       ├── deepagents.toml
│       └── skills/
│           ├── linkedin-post/
│           └── twitter-post/
├── utils/
│   └── models.py               # Centralized model config
├── pyproject.toml
└── .env.example
```

## Memory-backed deployment script

This repo also includes a one-file deployment script that creates a deep agent with a
`CompositeBackend` and Context Hub-backed `/memories/`, then wires a LangSmith issues board.

```bash
uv run python agents/memory_backed_agent/deploy_memory_backed_agent.py \
  --agent-name my-agent
```

See [`agents/memory_backed_agent/README.md`](agents/memory_backed_agent/README.md) for details.

**Deploy fails with 403 / permission denied**
Your LangSmith API key needs deployment permissions. Use a service key (`lsv2_sk_...`), not a personal access token (`lsv2_pt_...`).
