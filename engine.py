from datetime import datetime
from typing import Any
from models import RunState, GraphConfig
from registry import get_tool


def _evaluate_loop_condition(expr: str, state: dict) -> bool:
    try:
        return bool(eval(expr, {}, {"state": state}))
    except Exception:
        return False


def run_step(run_state: RunState, graph: GraphConfig) -> RunState:
    if run_state.current_node is None:
        run_state.status = "completed"
        return run_state

    node_name = run_state.current_node
    node_cfg = graph.nodes[node_name]

    # 1. Call tool if defined
    if node_cfg.tool_name:
        tool = get_tool(node_cfg.tool_name)
        updates = tool(run_state.state) or {}
        run_state.state.update(updates)

    # 2. Decide next node
    next_node: str | None = None

    # Loop condition
    if node_cfg.loop_condition:
        if _evaluate_loop_condition(node_cfg.loop_condition, run_state.state):
            next_node = node_name  # loop on same node

    if not next_node:
        next_node = node_cfg.next

    # 3. Log step
    run_state.log.append(
        {
            "node": node_name,
            "state": dict(run_state.state),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    )

    # 4. Update run state
    run_state.current_node = next_node
    if next_node is None:
        run_state.status = "completed"

    return run_state


def run_to_completion(run_state: RunState, graph: GraphConfig) -> RunState:
    while run_state.status == "running" and run_state.current_node is not None:
        run_state = run_step(run_state, graph)
    return run_state

