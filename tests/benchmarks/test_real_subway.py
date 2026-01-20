"""
Benchmarks for Beijing Subway pathfinding algorithms on real data.

This module provides pytest-benchmark tests using the actual Beijing Subway network
(~475 stations, ~950 track segments, 26 lines).

Tests include:
- Short routes (same line)
- Medium routes (1-2 transfers)
- Long routes (cross-city, multiple transfers)
- Hub-to-hub routes
- Real-world station pairs
"""

import pytest

from subway_navigation import BeijingSubwaySystem


@pytest.fixture(scope="module")
def subway_system():
    """
    Load the Beijing Subway system once for all benchmarks.
    This is expensive, so we reuse it across tests.
    """
    system = BeijingSubwaySystem()

    # Precompute A* heuristic table
    if system.heuristic_precompute is None:
        system.heuristic_precompute = system._precompute_heuristic()

    return system


# ============================================================================
# REAL-WORLD ROUTE BENCHMARKS - Dijkstra with Transfers
# ============================================================================


class TestRealSubwayDijkstra:
    """Benchmark Dijkstra with transfers on real Beijing Subway data."""

    def test_short_same_line_route(self, benchmark, subway_system):
        """Short route on same line: 苹果园 -> 八角游乐园 (1号线)."""
        start_id = subway_system.get_station_id("苹果园")
        end_id = subway_system.get_station_id("八角游乐园")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_weight_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
        )

        assert path is not None and len(path) > 0
        assert time > 0

    def test_medium_route_one_transfer(self, benchmark, subway_system):
        """Medium route with 1 transfer: 西直门 -> 复兴门."""
        start_id = subway_system.get_station_id("西直门")
        end_id = subway_system.get_station_id("复兴门")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_weight_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
        )

        assert path is not None and len(path) > 0
        assert time > 0

    def test_long_cross_city_route(self, benchmark, subway_system):
        """Long cross-city route: 西直门 -> 国贸."""
        start_id = subway_system.get_station_id("西直门")
        end_id = subway_system.get_station_id("国贸")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_weight_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
        )

        assert path is not None and len(path) > 0
        assert time > 0

    def test_hub_to_hub_route(self, benchmark, subway_system):
        """Route between major hubs: 天安门东 -> 北京站."""
        start_id = subway_system.get_station_id("天安门东")
        end_id = subway_system.get_station_id("北京站")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_weight_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
        )

        assert path is not None and len(path) > 0
        assert time > 0

    def test_complex_transfer_route(self, benchmark, subway_system):
        """Route requiring multiple transfers: 苹果园 -> 首都机场."""
        start_id = subway_system.get_station_id("苹果园")
        end_id = subway_system.get_station_id("大兴机场")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_weight_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
        )

        assert path is not None and len(path) > 0
        assert time > 0


# ============================================================================
# REAL-WORLD ROUTE BENCHMARKS - A* with Transfers
# ============================================================================


class TestRealSubwayAStar:
    """Benchmark A* with transfers on real Beijing Subway data."""

    def test_short_same_line_route(self, benchmark, subway_system):
        """Short route on same line: 苹果园 -> 八角游乐园 (1号线)."""
        start_id = subway_system.get_station_id("苹果园")
        end_id = subway_system.get_station_id("八角游乐园")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_astar_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
            subway_system.heuristic_precompute,
        )

        assert path is not None and len(path) > 0
        assert time > 0

    def test_medium_route_one_transfer(self, benchmark, subway_system):
        """Medium route with 1 transfer: 西直门 -> 复兴门."""
        start_id = subway_system.get_station_id("西直门")
        end_id = subway_system.get_station_id("复兴门")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_astar_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
            subway_system.heuristic_precompute,
        )

        assert path is not None and len(path) > 0
        assert time > 0

    def test_long_cross_city_route(self, benchmark, subway_system):
        """Long cross-city route: 西直门 -> 国贸."""
        start_id = subway_system.get_station_id("西直门")
        end_id = subway_system.get_station_id("国贸")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_astar_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
            subway_system.heuristic_precompute,
        )

        assert path is not None and len(path) > 0
        assert time > 0

    def test_hub_to_hub_route(self, benchmark, subway_system):
        """Route between major hubs: 天安门东 -> 北京站."""
        start_id = subway_system.get_station_id("天安门东")
        end_id = subway_system.get_station_id("北京站")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_astar_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
            subway_system.heuristic_precompute,
        )

        assert path is not None and len(path) > 0
        assert time > 0

    def test_complex_transfer_route(self, benchmark, subway_system):
        """Route requiring multiple transfers: 苹果园 -> 首都机场."""
        start_id = subway_system.get_station_id("苹果园")
        end_id = subway_system.get_station_id("大兴机场")
        assert start_id is not None and end_id is not None

        path, time = benchmark(
            subway_system.graph.find_shortest_path_astar_with_transfers,
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
            subway_system.heuristic_precompute,
        )

        assert path is not None and len(path) > 0
        assert time > 0


# ============================================================================
# BFS BENCHMARKS - Station Count Optimization
# ============================================================================


class TestRealSubwayBFS:
    """Benchmark BFS (fewest stations) on real Beijing Subway data."""

    def test_bfs_short_route(self, benchmark, subway_system):
        """BFS short route: 苹果园 -> 八角游乐园."""
        start_id = subway_system.get_station_id("苹果园")
        end_id = subway_system.get_station_id("八角游乐园")
        assert start_id is not None and end_id is not None

        path = benchmark(subway_system.graph.find_shortest_path_bfs, start_id, end_id)

        assert path is not None and len(path) > 0

    def test_bfs_long_route(self, benchmark, subway_system):
        """BFS long route: 西直门 -> 国贸."""
        start_id = subway_system.get_station_id("西直门")
        end_id = subway_system.get_station_id("国贸")
        assert start_id is not None and end_id is not None

        path = benchmark(subway_system.graph.find_shortest_path_bfs, start_id, end_id)

        assert path is not None and len(path) > 0


# ============================================================================
# DFS BENCHMARKS - Random Exploration
# ============================================================================


class TestRealSubwayDFS:
    """Benchmark DFS (any path) on real Beijing Subway data."""

    def test_dfs_short_route(self, benchmark, subway_system):
        """DFS short route: 苹果园 -> 八角游乐园."""
        start_id = subway_system.get_station_id("苹果园")
        end_id = subway_system.get_station_id("八角游乐园")
        assert start_id is not None and end_id is not None

        path = benchmark(subway_system.graph.find_path_dfs, start_id, end_id)

        assert path is not None and len(path) > 0

    def test_dfs_long_route(self, benchmark, subway_system):
        """DFS long route: 西直门 -> 国贸."""
        start_id = subway_system.get_station_id("西直门")
        end_id = subway_system.get_station_id("国贸")
        assert start_id is not None and end_id is not None

        path = benchmark(subway_system.graph.find_path_dfs, start_id, end_id)

        assert path is not None and len(path) > 0


# ============================================================================
# ALGORITHM COMPARISON BENCHMARKS - Real Data
# ============================================================================


class TestRealSubwayComparisonCorrectness:
    """Verify Dijkstra vs A* correctness on real Beijing Subway data."""

    def test_compare_dijkstra_astar_short_correctness(self, subway_system):
        """Compare Dijkstra vs A* on short route."""
        start_id = subway_system.get_station_id("苹果园")
        end_id = subway_system.get_station_id("八角游乐园")
        assert start_id is not None and end_id is not None

        dijkstra_result = subway_system.graph.find_shortest_path_weight_with_transfers(
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
        )

        astar_result = subway_system.graph.find_shortest_path_astar_with_transfers(
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
            subway_system.heuristic_precompute,
        )

        # Both should find paths with same cost (optimal)
        assert dijkstra_result[0] is not None
        assert astar_result[0] is not None
        assert abs(dijkstra_result[1] - astar_result[1]) < 0.01

    def test_compare_dijkstra_astar_long_correctness(self, subway_system):
        """Compare Dijkstra vs A* on long cross-city route."""
        start_id = subway_system.get_station_id("西直门")
        end_id = subway_system.get_station_id("国贸")
        assert start_id is not None and end_id is not None

        dijkstra_result = subway_system.graph.find_shortest_path_weight_with_transfers(
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
        )

        astar_result = subway_system.graph.find_shortest_path_astar_with_transfers(
            start_id,
            end_id,
            subway_system.edge_to_line,
            subway_system.station_to_lines_idx,
            subway_system.transfer_time,
            subway_system.idx_to_name,
            subway_system.heuristic_precompute,
        )

        # Both should find paths with same cost (optimal)
        assert dijkstra_result[0] is not None
        assert astar_result[0] is not None
        assert abs(dijkstra_result[1] - astar_result[1]) < 0.01
