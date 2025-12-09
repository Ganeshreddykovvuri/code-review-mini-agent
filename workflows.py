from typing import Dict
from models import GraphConfig, NodeConfig
from registry import register_tool
from storage import save_graph


def extract_functions_tool(state: dict) -> dict:
    code = state.get("code", "")
    function_count = code.count("def ")
    return {"function_count": function_count}


def check_complexity_tool(state: dict) -> dict:
    code = state.get("code", "")
    lines = len(code.splitlines())
    function_count = max(1, state.get("function_count", 1))
    complexity = lines * function_count
    return {"complexity": complexity}


def detect_issues_tool(state: dict) -> dict:
    code = state.get("code", "")
    issues = 0
    if "print(" in code:
        issues += 1
    if "TODO" in code:
        issues += 1
    return {"issues": issues}


def suggest_improvements_tool(state: dict) -> dict:
    complexity = state.get("complexity", 0)
    issues = state.get("issues", 0)

    suggestions = []
    if complexity > 200:
        suggestions.append("Break large functions into smaller ones.")
    if issues > 0:
        suggestions.append("Resolve TODOs and remove debug prints.")

    quality_score = max(0, 100 - complexity // 5 - issues * 10)

    return {
        "suggestions": suggestions,
        "quality_score": quality_score,
    }


def register_code_review_workflow() -> None:
    # register tools
    register_tool("extract_functions", extract_functions_tool)
    register_tool("check_complexity", check_complexity_tool)
    register_tool("detect_issues", detect_issues_tool)
    register_tool("suggest_improvements", suggest_improvements_tool)

    # create default graph
    graph = GraphConfig(
        id="code_review",
        start_node="extract",
        nodes={
            "extract": NodeConfig(
                name="extract",
                tool_name="extract_functions",
                next="complexity",
            ),
            "complexity": NodeConfig(
                name="complexity",
                tool_name="check_complexity",
                next="issues",
            ),
            "issues": NodeConfig(
                name="issues",
                tool_name="detect_issues",
                next="suggest",
            ),
            "suggest": NodeConfig(
                name="suggest",
                tool_name="suggest_improvements",
                next=None,
                loop_condition="state['quality_score'] < state.get('threshold', 80)",
            ),
        },
    )

    save_graph(graph)
