# Code Review Workflow Engine

This project is a FastAPI-based graph execution engine that allows creating and running configurable graphs with tools and workflows. It provides endpoints for graph creation, execution, and state retrieval.

## Features

- Create custom graphs with nodes and tools
- Execute graphs with initial state
- Retrieve run states and logs
- Built-in code review workflow example

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository or download the project files.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

1. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

2. The server will start on `http://localhost:8000`.

3. Access the interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

- `POST /graph/create`: Create a new graph
- `POST /graph/run`: Run a graph with initial state
- `GET /graph/state/{run_id}`: Get the state of a run

## Example Usage

### Creating a Graph

```json
POST /graph/create
{
  "start_node": "extract",
  "nodes": {
    "extract": {
      "name": "extract",
      "tool_name": "extract_functions",
      "next": "complexity"
    },
    "complexity": {
      "name": "complexity",
      "tool_name": "check_complexity",
      "next": "issues"
    },
    "issues": {
      "name": "issues",
      "tool_name": "detect_issues",
      "next": "suggest"
    },
    "suggest": {
      "name": "suggest",
      "tool_name": "suggest_improvements",
      "next": null
    }
  }
}
```

### Running a Graph

```json
POST /graph/run
{
  "graph_id": "your_graph_id",
  "initial_state": {
    "code": "def hello():\n    print('Hello, World!')\n\ndef goodbye():\n    print('Goodbye!')"
  }
}
```

## Built-in Workflows

The project includes a code review workflow that analyzes code for functions, complexity, issues, and suggestions.

## Project Structure

- `main.py`: FastAPI application and endpoints
- `models.py`: Pydantic models for requests and responses
- `engine.py`: Graph execution logic
- `storage.py`: In-memory storage for graphs and runs
- `registry.py`: Tool registration system
- `workflows.py`: Predefined workflows and tools


## What I Would Improve With More Time

1. Add branching logic
- Support conditional routing like:
```json
"branches": { "high": "pathA", "low": "pathB" }
```
2. Async execution of nodes
- Allow long-running tools to run concurrently and   improve performance.

3. Real database storage
- Persist graphs and run logs using:
- SQLite
- PostgreSQL
Instead of in-memory dictionaries.

4. WebSocket streaming
- Stream node-by-node execution logs to UI (like LangGraph streaming updates).

5. Graph Editor UI
- A drag-and-drop visual interface to build graphs.

6. Stronger loop safety
Prevent infinite loops by:
- max step limit
- timeout handling

7. Error boundaries
- Isolate node failures and continue running alternative paths.

