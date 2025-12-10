from fastapi import FastAPI, HTTPException
from models import (
    GraphCreateRequest,
    GraphCreateResponse,
    GraphRunRequest,
    GraphRunResponse,
    RunStateResponse,
    RunState,
    GraphConfig,
)
from storage import save_graph, get_graph, save_run, get_run
from engine import run_to_completion
from workflows import register_code_review_workflow
import uuid

app = FastAPI()


@app.on_event("startup")
def startup_event():
    # register tools and default "code_review" graph
    register_code_review_workflow()


@app.post("/graph/create", response_model=GraphCreateResponse)
async def create_graph(request: GraphCreateRequest):
    graph = GraphConfig(
        id=request.id,
        start_node=request.start_node,
        nodes=request.nodes,
    )
    save_graph(graph)
    return GraphCreateResponse(
        graph_id=graph.id,
        message="Graph created successfully",
    )


@app.post("/graph/run", response_model=GraphRunResponse)
async def run_graph(request: GraphRunRequest):
    try:
        graph = get_graph(request.graph_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Graph not found")

    run_id = str(uuid.uuid4())
    run_state = RunState(
        run_id=run_id,
        graph_id=graph.id,
        current_node=graph.start_node,
        state=dict(request.initial_state),
        log=[],
        status="running",
    )

    final_state = run_to_completion(run_state, graph)
    save_run(final_state)

    return GraphRunResponse(
        run_id=final_state.run_id,
        final_state=final_state.state,
        log=final_state.log,
        status=final_state.status,
    )


@app.get("/graph/state/{run_id}", response_model=RunStateResponse)
async def get_run_state(run_id: str):
    try:
        run_state = get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Run not found")

    return RunStateResponse(
        run_id=run_state.run_id,
        state=run_state.state,
        status=run_state.status,
        log=run_state.log,
    )

# To run the app, use the command:
# uvicorn main:app --reload
