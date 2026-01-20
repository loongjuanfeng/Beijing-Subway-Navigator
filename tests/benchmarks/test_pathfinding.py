"""
Comprehensive benchmarks for all pathfinding algorithms in the Beijing Subway Navigator.

This module provides pytest-benchmark tests for:
- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- Dijkstra (weighted shortest path)
- CPX (Matrix Power method)
- Dijkstra with transfers
- A* with transfers

Benchmarks cover various graph sizes and scenarios to measure algorithm performance.
"""

import pytest

from graph import Graph


# ============================================================================
# FIXTURES - Test Graphs of Different Sizes and Types
# ============================================================================


@pytest.fixture
def tiny_graph():
    """Tiny graph with 3 vertices."""
    data = [
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0],
    ]
    return Graph(data)


@pytest.fixture
def small_graph():
    """Small graph with 5 vertices - linear path."""
    data = [
        [0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
    ]
    return Graph(data)


@pytest.fixture
def medium_graph():
    """Medium graph with 10 vertices - branching structure."""
    data = [
        [0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ]
    return Graph(data)


@pytest.fixture
def dense_graph():
    """Dense graph with 15 vertices - many connections."""
    n = 15
    data = [[0.0] * n for _ in range(n)]
    # Create a highly connected graph
    for i in range(n):
        for j in range(i + 1, min(i + 4, n)):
            weight = (i + j) / 10.0 + 1.0
            data[i][j] = weight
    return Graph(data)


@pytest.fixture
def sparse_graph():
    """Sparse graph with 20 vertices - minimal connections."""
    n = 20
    data = [[0.0] * n for _ in range(n)]
    # Create a sparse linear path
    for i in range(n - 1):
        data[i][i + 1] = (i + 1) / 5.0 + 1.0
    return Graph(data)


@pytest.fixture
def complex_weighted_graph():
    """Complex weighted graph with multiple path options."""
    data = [
        [0.0, 1.0, 4.0, 0.0, 0.0],
        [0.0, 0.0, 2.0, 5.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 3.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
    ]
    return Graph(data)


@pytest.fixture
def transfer_aware_fixtures():
    """Provide fixtures for transfer-aware algorithms."""
    # Graph data
    data = [
        [0.0, 2.0, 0.0, 0.0, 0.0],
        [2.0, 0.0, 3.0, 0.0, 0.0],
        [0.0, 3.0, 0.0, 2.0, 0.0],
        [0.0, 0.0, 2.0, 0.0, 3.0],
        [0.0, 0.0, 0.0, 3.0, 0.0],
    ]

    edge_to_line = {
        (0, 1): "L1",
        (1, 0): "L1",
        (1, 2): "L1",
        (2, 1): "L1",
        (2, 3): "L2",
        (3, 2): "L2",
        (3, 4): "L2",
        (4, 3): "L2",
    }

    station_to_lines = {
        0: {"L1"},
        1: {"L1"},
        2: {"L1", "L2"},
        3: {"L2"},
        4: {"L2"},
    }

    transfer_time = {"C": {("L1", "L2"): 5.0, ("L2", "L1"): 5.0}}

    idx_to_name = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

    heuristic_table = [[0.0] * 5 for _ in range(5)]

    return {
        "graph": Graph(data),
        "edge_to_line": edge_to_line,
        "station_to_lines": station_to_lines,
        "transfer_time": transfer_time,
        "idx_to_name": idx_to_name,
        "heuristic_table": heuristic_table,
    }


# ============================================================================
# BFS BENCHMARKS
# ============================================================================


class TestBFSBenchmark:
    """Benchmarks for BFS pathfinding algorithm."""

    def test_bfs_tiny_graph(self, benchmark, tiny_graph):
        """BFS on tiny graph (3 vertices)."""
        result = benchmark(tiny_graph.find_shortest_path_bfs, 0, 2)
        assert result == [0, 1, 2]

    def test_bfs_small_graph(self, benchmark, small_graph):
        """BFS on small graph (5 vertices)."""
        result = benchmark(small_graph.find_shortest_path_bfs, 0, 4)
        assert result == [0, 1, 2, 3, 4]

    def test_bfs_medium_graph(self, benchmark, medium_graph):
        """BFS on medium graph (10 vertices, branching)."""
        result = benchmark(medium_graph.find_shortest_path_bfs, 0, 9)
        assert result is not None
        assert result[0] == 0 and result[-1] == 9

    def test_bfs_dense_graph(self, benchmark, dense_graph):
        """BFS on dense graph (15 vertices, many connections)."""
        result = benchmark(dense_graph.find_shortest_path_bfs, 0, 14)
        assert result is not None

    def test_bfs_sparse_graph(self, benchmark, sparse_graph):
        """BFS on sparse graph (20 vertices, linear path)."""
        result = benchmark(sparse_graph.find_shortest_path_bfs, 0, 19)
        assert result is not None
        assert len(result) == 20

    def test_bfs_same_node(self, benchmark, small_graph):
        """BFS when start == end."""
        result = benchmark(small_graph.find_shortest_path_bfs, 2, 2)
        assert result == [2]


# ============================================================================
# DFS BENCHMARKS
# ============================================================================


class TestDFSBenchmark:
    """Benchmarks for DFS pathfinding algorithm."""

    def test_dfs_tiny_graph(self, benchmark, tiny_graph):
        """DFS on tiny graph (3 vertices)."""
        result = benchmark(tiny_graph.find_path_dfs, 0, 2)
        assert result is not None
        assert result[0] == 0 and result[-1] == 2

    def test_dfs_small_graph(self, benchmark, small_graph):
        """DFS on small graph (5 vertices)."""
        result = benchmark(small_graph.find_path_dfs, 0, 4)
        assert result is not None
        assert result[0] == 0 and result[-1] == 4

    def test_dfs_medium_graph(self, benchmark, medium_graph):
        """DFS on medium graph (10 vertices, branching)."""
        result = benchmark(medium_graph.find_path_dfs, 0, 9)
        assert result is not None

    def test_dfs_dense_graph(self, benchmark, dense_graph):
        """DFS on dense graph (15 vertices, many connections)."""
        result = benchmark(dense_graph.find_path_dfs, 0, 14)
        assert result is not None

    def test_dfs_sparse_graph(self, benchmark, sparse_graph):
        """DFS on sparse graph (20 vertices, linear path)."""
        result = benchmark(sparse_graph.find_path_dfs, 0, 19)
        assert result is not None

    def test_dfs_same_node(self, benchmark, small_graph):
        """DFS when start == end."""
        result = benchmark(small_graph.find_path_dfs, 2, 2)
        assert result == [2]


# ============================================================================
# DIJKSTRA BENCHMARKS
# ============================================================================


class TestDijkstraBenchmark:
    """Benchmarks for Dijkstra's algorithm."""

    def test_dijkstra_tiny_graph(self, benchmark, tiny_graph):
        """Dijkstra on tiny graph (3 vertices)."""
        path, time = benchmark(tiny_graph.find_shortest_path_weight, 0, 2)
        assert path == [0, 1, 2]
        assert time == 2.0

    def test_dijkstra_small_graph(self, benchmark, small_graph):
        """Dijkstra on small graph (5 vertices)."""
        path, time = benchmark(small_graph.find_shortest_path_weight, 0, 4)
        assert path == [0, 1, 2, 3, 4]
        assert time == 4.0

    def test_dijkstra_medium_graph(self, benchmark, medium_graph):
        """Dijkstra on medium graph (10 vertices, branching)."""
        path, time = benchmark(medium_graph.find_shortest_path_weight, 0, 9)
        assert path is not None
        assert path[0] == 0 and path[-1] == 9

    def test_dijkstra_dense_graph(self, benchmark, dense_graph):
        """Dijkstra on dense graph (15 vertices, many connections)."""
        path, time = benchmark(dense_graph.find_shortest_path_weight, 0, 14)
        assert path is not None

    def test_dijkstra_sparse_graph(self, benchmark, sparse_graph):
        """Dijkstra on sparse graph (20 vertices, linear path)."""
        path, time = benchmark(sparse_graph.find_shortest_path_weight, 0, 19)
        assert path is not None

    def test_dijkstra_weighted_complex(self, benchmark, complex_weighted_graph):
        """Dijkstra on complex weighted graph."""
        path, time = benchmark(complex_weighted_graph.find_shortest_path_weight, 0, 4)
        assert path == [0, 1, 2, 3, 4]
        assert time == 7.0  # 1.0 + 2.0 + 1.0 + 3.0

    def test_dijkstra_same_node(self, benchmark, small_graph):
        """Dijkstra when start == end."""
        path, time = benchmark(small_graph.find_shortest_path_weight, 2, 2)
        assert path == [2]
        assert time == 0.0


# ============================================================================
# CPX (Matrix Power) BENCHMARKS
# ============================================================================


class TestCPXBenchmark:
    """Benchmarks for CPX (Matrix Power) pathfinding."""

    def test_cpx_tiny_graph(self, benchmark, tiny_graph):
        """CPX on tiny graph (3 vertices)."""
        result = benchmark(tiny_graph.find_shortest_path_cpx, 0, 2)
        assert result is not None
        assert result == [0, 1, 2]

    def test_cpx_small_graph(self, benchmark, small_graph):
        """CPX on small graph (5 vertices)."""
        result = benchmark(small_graph.find_shortest_path_cpx, 0, 4)
        assert result is not None
        assert result == [0, 1, 2, 3, 4]

    def test_cpx_medium_graph(self, benchmark, medium_graph):
        """CPX on medium graph (10 vertices, branching)."""
        result = benchmark(medium_graph.find_shortest_path_cpx, 0, 9)
        assert result is not None

    def test_cpx_same_node(self, benchmark, small_graph):
        """CPX when start == end."""
        result = benchmark(small_graph.find_shortest_path_cpx, 2, 2)
        assert result == [2]


# ============================================================================
# DIJKSTRA WITH TRANSFERS BENCHMARKS
# ============================================================================


class TestDijkstraWithTransfersBenchmark:
    """Benchmarks for Dijkstra with transfer penalties."""

    def test_dijkstra_transfers_no_transfer(self, benchmark, transfer_aware_fixtures):
        """Dijkstra with transfers: no line change."""
        graph = transfer_aware_fixtures["graph"]
        result = benchmark(
            graph.find_shortest_path_weight_with_transfers,
            0,
            2,
            transfer_aware_fixtures["edge_to_line"],
            transfer_aware_fixtures["station_to_lines"],
            transfer_aware_fixtures["transfer_time"],
            transfer_aware_fixtures["idx_to_name"],
        )
        path, time = result
        assert path == [0, 1, 2]
        assert time == 5.0

    def test_dijkstra_transfers_with_transfer(self, benchmark, transfer_aware_fixtures):
        """Dijkstra with transfers: with line change."""
        graph = transfer_aware_fixtures["graph"]
        result = benchmark(
            graph.find_shortest_path_weight_with_transfers,
            0,
            4,
            transfer_aware_fixtures["edge_to_line"],
            transfer_aware_fixtures["station_to_lines"],
            transfer_aware_fixtures["transfer_time"],
            transfer_aware_fixtures["idx_to_name"],
        )
        path, time = result
        assert path == [0, 1, 2, 3, 4]
        assert time == 15.0  # 2+3+5+2+3

    def test_dijkstra_transfers_same_node(self, benchmark, transfer_aware_fixtures):
        """Dijkstra with transfers: start == end."""
        graph = transfer_aware_fixtures["graph"]
        result = benchmark(
            graph.find_shortest_path_weight_with_transfers,
            2,
            2,
            transfer_aware_fixtures["edge_to_line"],
            transfer_aware_fixtures["station_to_lines"],
            transfer_aware_fixtures["transfer_time"],
            transfer_aware_fixtures["idx_to_name"],
        )
        path, time = result
        assert path == [2]
        assert time == 0.0


# ============================================================================
# A* WITH TRANSFERS BENCHMARKS
# ============================================================================


class TestAStarWithTransfersBenchmark:
    """Benchmarks for A* with transfer penalties."""

    def test_astar_transfers_no_transfer(self, benchmark, transfer_aware_fixtures):
        """A* with transfers: no line change."""
        graph = transfer_aware_fixtures["graph"]
        result = benchmark(
            graph.find_shortest_path_astar_with_transfers,
            0,
            2,
            transfer_aware_fixtures["edge_to_line"],
            transfer_aware_fixtures["station_to_lines"],
            transfer_aware_fixtures["transfer_time"],
            transfer_aware_fixtures["idx_to_name"],
            transfer_aware_fixtures["heuristic_table"],
        )
        path, time = result
        assert path == [0, 1, 2]
        assert time == 5.0

    def test_astar_transfers_with_transfer(self, benchmark, transfer_aware_fixtures):
        """A* with transfers: with line change."""
        graph = transfer_aware_fixtures["graph"]
        result = benchmark(
            graph.find_shortest_path_astar_with_transfers,
            0,
            4,
            transfer_aware_fixtures["edge_to_line"],
            transfer_aware_fixtures["station_to_lines"],
            transfer_aware_fixtures["transfer_time"],
            transfer_aware_fixtures["idx_to_name"],
            transfer_aware_fixtures["heuristic_table"],
        )
        path, time = result
        assert path == [0, 1, 2, 3, 4]
        assert time == 15.0

    def test_astar_transfers_same_node(self, benchmark, transfer_aware_fixtures):
        """A* with transfers: start == end."""
        graph = transfer_aware_fixtures["graph"]
        result = benchmark(
            graph.find_shortest_path_astar_with_transfers,
            2,
            2,
            transfer_aware_fixtures["edge_to_line"],
            transfer_aware_fixtures["station_to_lines"],
            transfer_aware_fixtures["transfer_time"],
            transfer_aware_fixtures["idx_to_name"],
            transfer_aware_fixtures["heuristic_table"],
        )
        path, time = result
        assert path == [2]
        assert time == 0.0


# ============================================================================
# ALGORITHM COMPARISON BENCHMARKS
# ============================================================================
# ALGORITHM COMPARISON BENCHMARKS
# ============================================================================


class TestAlgorithmComparisonCorrectness:
    """Verify algorithm correctness on same problems (not timing comparison)."""

    def test_compare_bfs_dijkstra_unweighted_correctness(self, complex_weighted_graph):
        """BFS vs Dijkstra on unweighted (same weight) paths."""
        bfs_result = complex_weighted_graph.find_shortest_path_bfs(0, 4)
        dijkstra_result = complex_weighted_graph.find_shortest_path_weight(0, 4)

        assert bfs_result is not None
        assert dijkstra_result[0] is not None

    def test_compare_dijkstra_astar_with_transfers_correctness(self, transfer_aware_fixtures):
        """Dijkstra vs A* with transfer penalties."""
        graph = transfer_aware_fixtures["graph"]

        dijkstra_result = graph.find_shortest_path_weight_with_transfers(
            0,
            4,
            transfer_aware_fixtures["edge_to_line"],
            transfer_aware_fixtures["station_to_lines"],
            transfer_aware_fixtures["transfer_time"],
            transfer_aware_fixtures["idx_to_name"],
        )

        astar_result = graph.find_shortest_path_astar_with_transfers(
            0,
            4,
            transfer_aware_fixtures["edge_to_line"],
            transfer_aware_fixtures["station_to_lines"],
            transfer_aware_fixtures["transfer_time"],
            transfer_aware_fixtures["idx_to_name"],
            transfer_aware_fixtures["heuristic_table"],
        )

        # Both should find optimal paths with same cost
        assert dijkstra_result[1] == astar_result[1]
        assert dijkstra_result[0] == astar_result[0]
