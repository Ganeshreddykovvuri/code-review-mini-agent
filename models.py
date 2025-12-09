from typing import Dict, List, Literal, Optional, Any
from pydantic import BaseModel


class NodeConfig(BaseModel):
    name: str
    tool_name: Optional[str] = None
    next: Optional[str] = None
    branches: Optional[Dict[str, str]] = None
    loop_condition: Optional[str] = None


class GraphConfig(BaseModel):
    id: str
    start_node: str
    nodes: Dict[str, NodeConfig]


class GraphCreateRequest(BaseModel):
    id: str
    start_node: str
    nodes: Dict[str, NodeConfig]


class GraphCreateResponse(BaseModel):
    graph_id: str
    message: str


class RunState(BaseModel):
    run_id: str
    graph_id: str
    current_node: Optional[str]
    state: Dict[str, Any]
    log: List[Dict[str, Any]]
    status: Literal["running", "completed", "failed"]


class GraphRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


class GraphRunResponse(BaseModel):
    run_id: str
    final_state: Dict[str, Any]
    log: List[Dict[str, Any]]
    status: Literal["running", "completed", "failed"]


class RunStateResponse(BaseModel):
    run_id: str
    state: Dict[str, Any]
    status: Literal["running", "completed", "failed"]
    log: List[Dict[str, Any]]
