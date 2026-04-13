"""Deep Agent for LangGraph Studio.

A research agent built with Deep Agents that demonstrates:
- AGENTS.md for agent identity and instructions
- Skills for on-demand capabilities (LinkedIn, Twitter)
- Custom tools (Tavily search)
- Research subagent for delegated work
- Long-term memory via CompositeBackend
- Human-in-the-loop on file writes
"""

import os
from datetime import datetime

from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend, StoreBackend
from langchain_core.tools import tool
from tavily import TavilyClient

from utils.models import model

AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Tools ---

tavily_client = TavilyClient()


@tool(parse_docstring=True)
def tavily_search(query: str) -> str:
    """Search the web for information on a given query.

    Args:
        query: Search query to execute
    """
    search_results = tavily_client.search(query, max_results=3, topic="general")
    result_texts = []
    for result in search_results.get("results", []):
        url = result["url"]
        title = result["title"]
        content = result.get("content", "No content available")
        result_texts.append(f"## {title}\n**URL:** {url}\n\n{content}\n\n---\n")
    return f"Found {len(result_texts)} result(s) for '{query}':\n\n{''.join(result_texts)}"


# --- Research Subagent ---

research_subagent = {
    "name": "research-agent",
    "description": "Delegate research tasks. Give one topic at a time.",
    "system_prompt": f"""You are a research assistant. Today is {datetime.now().strftime('%Y-%m-%d')}.
Use tools to gather information. Structure findings with clear headings and inline citations.
Limit to 3 search calls.""",
    "tools": [tavily_search],
}


# --- Backend ---

def backend_factory(rt):
    """FilesystemBackend for disk access, /memories/ routed to StoreBackend."""
    return CompositeBackend(
        default=FilesystemBackend(root_dir=AGENT_DIR, virtual_mode=True),
        routes={"/memories/": StoreBackend(rt)},
    )


# --- Agent ---

agent = create_deep_agent(
    model=model,
    tools=[tavily_search],
    system_prompt="You are an expert research assistant.",
    memory=["./AGENTS.md"],
    skills=["./skills/"],
    subagents=[research_subagent],
    backend=backend_factory,
    interrupt_on={"write_file": True, "edit_file": True},
)
