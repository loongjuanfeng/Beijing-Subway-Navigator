# Test Suite for Graph Module

This directory contains comprehensive tests for the `graph.py` module using pytest.

## Test Structure

### Test Files

- **`test_graph_basic.py`**: Tests for basic graph operations
  - Graph initialization and construction
  - Edge operations (add, remove, count)
  - Neighbor queries and degree calculations
  - Basic graph properties (completeness, connectivity)

- **`test_graph_algorithms.py`**: Tests for pathfinding algorithms
  - BFS (Breadth-First Search) shortest path
  - DFS (Depth-First Search) path finding
  - Dijkstra's algorithm for weighted shortest paths
  - Matrix Power (CPX) method
  - Algorithm comparison tests

- **`test_graph_properties.py`**: Tests for advanced graph properties
  - Prim's algorithm for Minimum Spanning Tree (MST)
  - Graph connectivity analysis
  - Connected component detection
  - Bipartite graph checking
  - Combined property validation

## Running Tests

### Run all tests
```bash
uv run pytest
```

### Run with verbose output
```bash
uv run pytest -v
```

### Run specific test file
```bash
uv run pytest tests/test_graph_basic.py
```

### Run specific test class or method
```bash
uv run pytest tests/test_graph_algorithms.py::TestBFSPathfinding
uv run pytest tests/test_graph_algorithms.py::TestBFSPathfinding::test_bfs_simple_path
```

### Run with coverage report
```bash
uv run pytest --cov=graph --cov-report=term-missing
```

### Generate HTML coverage report
```bash
uv run pytest --cov=graph --cov-report=html
# Open htmlcov/index.html in a browser
```

### Run tests in parallel (faster)
```bash
uv run pytest -n auto
```

## Test Coverage

Current coverage: **99.55%** (220/221 statements)

Coverage requirements:
- Minimum: 80%
- Current: 99.55%

## Test Fixtures

Common test fixtures used across test files:
- `empty_graph`: Graph with no data
- `simple_graph`: Basic directed graph
- `weighted_graph`: Graph with weighted edges
- `undirected_graph`: Symmetric adjacency matrix
- `complete_graph`: Fully connected graph
- `branching_graph`: Graph with multiple path options
- `unreachable_graph`: Graph with disconnected components

## CI/CD Integration

The test suite is configured to fail if coverage drops below 80%:

```toml
[tool.pytest.ini_options]
addopts = [
    "--cov=graph",
    "--cov-fail-under=80",
]
```

## Writing New Tests

1. Create a new test file or add to existing test files
2. Use descriptive test names following `test_<functionality>` pattern
3. Use fixtures to share common test data
4. Add docstrings for complex test scenarios
5. Run tests locally before committing

Example:
```python
def test_new_feature(simple_graph):
    result = simple_graph.new_method()
    assert result is not None
    assert len(result) > 0
```
