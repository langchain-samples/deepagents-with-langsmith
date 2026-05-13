# memory-backed-agent

Deploy a Deep Agent that uses Context Hub for durable memory and LangSmith Engine
for automated issue discovery from production traces.

This example is intentionally one file: `deploy_memory_backed_agent.py`, which:

- keeps thread-scoped state in `StateBackend`
- routes `/memories/` to `ContextHubBackend` for durable, versioned memory
- deploys the graph with `langgraph deploy`
- wires LangSmith issues analysis to the same Context Hub repo handle

## Continual learning with Context Hub

Production agents hit edge cases that initial context does not cover.

In this pattern, the same repo handle backs both `/memories/` and LangSmith
Engine, so issue triage and context updates stay connected.

## How LangSmith Engine identifies issues

After deployment, the script upserts the LangSmith issues board for the tracing
project:

LangSmith Engine then runs on a schedule, analyzes traces, and files issues
against the same Context Hub repo handle your agent uses for `/memories/`.

## Required environment variables

- `LANGSMITH_API_KEY` (or `LANGCHAIN_API_KEY`)
- `ANTHROPIC_API_KEY` (unless `DEEPAGENT_MODEL` points to a different provider and that provider key is set)

Use a LangSmith service key (`lsv2_sk_...`) with deploy permissions.

## Optional environment variables

- `DEEPAGENT_MODEL` (default: `anthropic:claude-sonnet-4-6`)
- `LANGSMITH_ENDPOINT` or `LANGCHAIN_ENDPOINT` (default: `https://api.smith.langchain.com`)
- `LANGSMITH_TENANT_ID`

## Run

From the repository root:

```bash
uv sync
uv run python agents/memory_backed_agent/deploy_memory_backed_agent.py --agent-name my-agent
```

## What `--agent-name` controls

`--agent-name` (default: `my-agent`) is reused for:

- deployed graph name (`langgraph deploy --name ...`)
- Context Hub repo handle used by `/memories/`
- tracing project lookup used for issues-board wiring

## Deployment flow

1. Builds `agent` with `CompositeBackend(default=StateBackend(), routes={"/memories/": ContextHubBackend(agent_name)})`.
2. Runs `langgraph deploy` for this file.
3. Ensures the Context Hub repo exists for `{agent_name}` and creates it with `source="internal"` when missing.
4. Resolves the deployed tracing project id from the project name.
5. Calls `POST /v1/platform/sessions/{session_id}/issues-agent`.
6. If create returns `409`, calls `PATCH` to update `context_hub_repo_handle`.
