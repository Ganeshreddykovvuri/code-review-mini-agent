from typing import Dict
from models import GraphConfig, RunState

GRAPHS: Dict[str, GraphConfig] = {}
RUNS: Dict[str, RunState] = {}


def save_graph(graph: GraphConfig) -> None:
    GRAPHS[graph.id] = graph


def get_graph(graph_id: str) -> GraphConfig:
    if graph_id not in GRAPHS:
        raise KeyError(f"Graph with id '{graph_id}' not found")
    return GRAPHS[graph_id]


def save_run(run: RunState) -> None:
    RUNS[run.run_id] = run


def get_run(run_id: str) -> RunState:
    if run_id not in RUNS:
        raise KeyError(f"Run with id '{run_id}' not found")
    return RUNS[run_id]
