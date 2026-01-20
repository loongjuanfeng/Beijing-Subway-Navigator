import pytest

from graph import Graph


@pytest.fixture
def simple_path_graph():
    data = [
        [0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
    ]
    return Graph(data)


@pytest.fixture
def branching_graph():
    data = [
        [0.0, 1.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
    ]
    return Graph(data)


@pytest.fixture
def weighted_graph():
    data = [
        [0.0, 4.0, 0.0, 0.0],
        [0.0, 0.0, 2.0, 0.0],
        [0.0, 0.0, 0.0, 3.0],
        [0.0, 0.0, 0.0, 0.0],
    ]
    return Graph(data)


@pytest.fixture
def unreachable_graph():
    data = [
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0],
    ]
    return Graph(data)


class TestBFSPathfinding:
    def test_bfs_simple_path(self, simple_path_graph):
        path = simple_path_graph.find_shortest_path_bfs(0, 4)
        assert path == [0, 1, 2, 3, 4]

    def test_bfs_same_start_end(self, simple_path_graph):
        path = simple_path_graph.find_shortest_path_bfs(2, 2)
        assert path == [2]

    def test_bfs_branching_path(self, branching_graph):
        path = branching_graph.find_shortest_path_bfs(0, 4)
        assert path == [0, 1, 3, 4]

    def test_bfs_unreachable(self, unreachable_graph):
        path = unreachable_graph.find_shortest_path_bfs(0, 3)
        assert path is None

    def test_bfs_finds_shortest_in_edges(self, branching_graph):
        path1 = branching_graph.find_shortest_path_bfs(0, 3)
        path2 = branching_graph.find_shortest_path_bfs(0, 3)
        assert len(path1) == len(path2) == 3


class TestDFSPathfinding:
    def test_dfs_simple_path(self, simple_path_graph):
        path = simple_path_graph.find_path_dfs(0, 4)
        assert path == [0, 1, 2, 3, 4]

    def test_dfs_same_start_end(self, simple_path_graph):
        path = simple_path_graph.find_path_dfs(2, 2)
        assert path == [2]

    def test_dfs_branching_path(self, branching_graph):
        path = branching_graph.find_path_dfs(0, 4)
        assert path is not None
        assert path[0] == 0
        assert path[-1] == 4

    def test_dfs_unreachable(self, unreachable_graph):
        path = unreachable_graph.find_path_dfs(0, 3)
        assert path is None


class TestDijkstraPathfinding:
    def test_dijkstra_simple_path(self, weighted_graph):
        path, time = weighted_graph.find_shortest_path_weight(0, 3)
        assert path == [0, 1, 2, 3]
        assert time == 9.0

    def test_dijkstra_same_start_end(self, weighted_graph):
        path, time = weighted_graph.find_shortest_path_weight(2, 2)
        assert path == [2]
        assert time == 0.0

    def test_dijkstra_unreachable(self, unreachable_graph):
        path, time = unreachable_graph.find_shortest_path_weight(0, 3)
        assert path is None
        assert time == float("inf")

    def test_dijkstra_weighted_shortest_path(self):
        data = [
            [0.0, 1.0, 4.0, 0.0, 0.0],
            [0.0, 0.0, 2.0, 5.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 3.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
        ]
        graph = Graph(data)
        path, time = graph.find_shortest_path_weight(0, 3)
        assert path == [0, 1, 2, 3]
        assert time == 4.0


class TestCPXPathfinding:
    def test_cpx_simple_path(self, simple_path_graph):
        result = simple_path_graph.find_shortest_path_cpx(0, 4)
        assert result is not None
        assert result == [0, 1, 2, 3, 4]

    def test_cpx_same_start_end(self, simple_path_graph):
        result = simple_path_graph.find_shortest_path_cpx(2, 2)
        assert result == [2]

    def test_cpx_unreachable(self, unreachable_graph):
        result = unreachable_graph.find_shortest_path_cpx(0, 3)
        assert result is None

    def test_cpx_direct_edge(self):
        data = [[0.0, 1.0], [0.0, 0.0]]
        graph = Graph(data)
        result = graph.find_shortest_path_cpx(0, 1)
        assert result is not None
        assert result == [0, 1]


class TestPathComparison:
    def test_bfs_and_dijkstra_same_for_unweighted(self, branching_graph):
        bfs_path = branching_graph.find_shortest_path_bfs(0, 4)
        dijkstra_path, _ = branching_graph.find_shortest_path_weight(0, 4)
        assert bfs_path == dijkstra_path

    def test_dijkstra_considers_weights(self):
        data = [
            [0.0, 1.0, 10.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 0.0],
        ]
        graph = Graph(data)
        bfs_path = graph.find_shortest_path_bfs(0, 3)
        dijkstra_path, time = graph.find_shortest_path_weight(0, 3)
        assert bfs_path == [0, 1, 3]
        assert dijkstra_path == [0, 1, 3]
        assert time == 2.0


class TestTransferAwareRouting:
    def test_transfer_aware_simple_path_with_no_transfer(self):
        data = [
            [0.0, 2.0, 0.0, 0.0],
            [2.0, 0.0, 3.0, 0.0],
            [0.0, 3.0, 0.0, 4.0],
            [0.0, 0.0, 4.0, 0.0],
        ]
        graph = Graph(data)

        edge_to_line = {
            (0, 1): "L1",
            (1, 0): "L1",
            (1, 2): "L1",
            (2, 1): "L1",
            (2, 3): "L1",
            (3, 2): "L1",
        }
        station_to_lines = {0: {"L1"}, 1: {"L1"}, 2: {"L1"}, 3: {"L1"}}
        transfer_time = {}
        idx_to_name = {0: "A", 1: "B", 2: "C", 3: "D"}

        path, time = graph.find_shortest_path_weight_with_transfers(
            0, 3, edge_to_line, station_to_lines, transfer_time, idx_to_name
        )

        assert path == [0, 1, 2, 3]
        assert time == 9.0

    def test_transfer_aware_with_single_transfer(self):
        data = [
            [0.0, 2.0, 0.0, 0.0],
            [2.0, 0.0, 3.0, 0.0],
            [0.0, 3.0, 0.0, 2.0],
            [0.0, 0.0, 2.0, 0.0],
        ]
        graph = Graph(data)

        edge_to_line = {
            (0, 1): "L1",
            (1, 0): "L1",
            (1, 2): "L1",
            (2, 1): "L1",
            (2, 3): "L2",
            (3, 2): "L2",
        }
        station_to_lines = {0: {"L1"}, 1: {"L1"}, 2: {"L1", "L2"}, 3: {"L2"}}
        transfer_time = {"C": {("L1", "L2"): 5.0}}
        idx_to_name = {0: "A", 1: "B", 2: "C", 3: "D"}

        path, time = graph.find_shortest_path_weight_with_transfers(
            0, 3, edge_to_line, station_to_lines, transfer_time, idx_to_name
        )

        assert path == [0, 1, 2, 3]
        assert time == 12.0

    def test_transfer_aware_asymmetric_transfer_times(self):
        data = [
            [0.0, 2.0, 0.0, 0.0],
            [2.0, 0.0, 3.0, 0.0],
            [0.0, 3.0, 0.0, 2.0],
            [0.0, 0.0, 2.0, 0.0],
        ]
        graph = Graph(data)

        edge_to_line = {
            (0, 1): "L1",
            (1, 0): "L1",
            (1, 2): "L1",
            (2, 1): "L1",
            (2, 3): "L2",
            (3, 2): "L2",
        }
        station_to_lines = {0: {"L1"}, 1: {"L1"}, 2: {"L1", "L2"}, 3: {"L2"}}
        transfer_time = {"C": {("L1", "L2"): 5.0, ("L2", "L1"): 10.0}}
        idx_to_name = {0: "A", 1: "B", 2: "C", 3: "D"}

        path_forward, time_forward = graph.find_shortest_path_weight_with_transfers(
            0, 3, edge_to_line, station_to_lines, transfer_time, idx_to_name
        )

        path_reverse, time_reverse = graph.find_shortest_path_weight_with_transfers(
            3, 0, edge_to_line, station_to_lines, transfer_time, idx_to_name
        )

        assert path_forward == [0, 1, 2, 3]
        assert path_reverse == [3, 2, 1, 0]
        assert time_forward == 12.0
        assert time_reverse == 17.0

    def test_transfer_aware_multiple_transfers(self):
        data = [
            [0.0, 2.0, 0.0, 0.0, 0.0],
            [2.0, 0.0, 3.0, 0.0, 0.0],
            [0.0, 3.0, 0.0, 2.0, 0.0],
            [0.0, 0.0, 2.0, 0.0, 3.0],
            [0.0, 0.0, 0.0, 3.0, 0.0],
        ]
        graph = Graph(data)

        edge_to_line = {
            (0, 1): "L1",
            (1, 0): "L1",
            (1, 2): "L1",
            (2, 1): "L1",
            (2, 3): "L2",
            (3, 2): "L2",
            (3, 4): "L3",
            (4, 3): "L3",
        }
        station_to_lines = {0: {"L1"}, 1: {"L1"}, 2: {"L1", "L2"}, 3: {"L2", "L3"}, 4: {"L3"}}
        transfer_time = {"C": {("L1", "L2"): 5.0}, "D": {("L2", "L3"): 4.0}}
        idx_to_name = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

        path, time = graph.find_shortest_path_weight_with_transfers(
            0, 4, edge_to_line, station_to_lines, transfer_time, idx_to_name
        )

        assert path == [0, 1, 2, 3, 4]
        assert time == 19.0

    def test_transfer_aware_no_transfer_penalty_when_same_line(self):
        data = [
            [0.0, 2.0, 0.0, 0.0],
            [2.0, 0.0, 3.0, 0.0],
            [0.0, 3.0, 0.0, 4.0],
            [0.0, 0.0, 4.0, 0.0],
        ]
        graph = Graph(data)

        edge_to_line = {
            (0, 1): "L1",
            (1, 0): "L1",
            (1, 2): "L1",
            (2, 1): "L1",
            (2, 3): "L1",
            (3, 2): "L1",
        }
        station_to_lines = {0: {"L1"}, 1: {"L1", "L2"}, 2: {"L1", "L2"}, 3: {"L1"}}
        transfer_time = {"B": {("L1", "L2"): 5.0}, "C": {("L2", "L1"): 5.0}}
        idx_to_name = {0: "A", 1: "B", 2: "C", 3: "D"}

        path, time = graph.find_shortest_path_weight_with_transfers(
            0, 3, edge_to_line, station_to_lines, transfer_time, idx_to_name
        )

        assert path == [0, 1, 2, 3]
        assert time == 9.0

    def test_transfer_aware_unreachable_path(self):
        data = [
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 0.0, 0.0],
        ]
        graph = Graph(data)

        edge_to_line = {(0, 1): "L1", (1, 0): "L1", (2, 3): "L2", (3, 2): "L2"}
        station_to_lines = {0: {"L1"}, 1: {"L1"}, 2: {"L2"}, 3: {"L2"}}
        transfer_time = {}
        idx_to_name = {0: "A", 1: "B", 2: "C", 3: "D"}

        path, time = graph.find_shortest_path_weight_with_transfers(
            0, 3, edge_to_line, station_to_lines, transfer_time, idx_to_name
        )

        assert path == []
        assert time == float("inf")

    def test_transfer_aware_same_start_end(self):
        data = [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
        graph = Graph(data)

        edge_to_line = {(0, 1): "L1", (1, 0): "L1", (1, 2): "L2", (2, 1): "L2"}
        station_to_lines = {0: {"L1"}, 1: {"L1", "L2"}, 2: {"L2"}}
        transfer_time = {}
        idx_to_name = {0: "A", 1: "B", 2: "C"}

        path, time = graph.find_shortest_path_weight_with_transfers(
            1, 1, edge_to_line, station_to_lines, transfer_time, idx_to_name
        )

        assert path == [1]
        assert time == 0.0


class TestAStarPathfinding:
    def test_astar_optimality_vs_dijkstra(self, weighted_graph):
        path_d, time_d = weighted_graph.find_shortest_path_weight(0, 3)
        edge_to_line = {
            (0, 1): "L1",
            (1, 0): "L1",
            (1, 2): "L1",
            (2, 1): "L1",
            (2, 3): "L1",
            (3, 2): "L1",
        }
        path_a, time_a = weighted_graph.find_shortest_path_astar_with_transfers(
            0,
            3,
            edge_to_line,
            {i: set() for i in range(4)},
            {},
            {i: str(i) for i in range(4)},
            [[0.0] * 4 for _ in range(4)],
        )
        assert path_a == path_d
        assert abs(time_a - time_d) < 0.01

    def test_astar_transfer_aware_simple_path(self):
        data = [
            [0.0, 2.0, 0.0, 0.0],
            [2.0, 0.0, 3.0, 0.0],
            [0.0, 3.0, 0.0, 4.0],
            [0.0, 0.0, 4.0, 0.0],
        ]
        graph = Graph(data)

        edge_to_line = {
            (0, 1): "L1",
            (1, 0): "L1",
            (1, 2): "L1",
            (2, 1): "L1",
            (2, 3): "L1",
            (3, 2): "L1",
        }
        station_to_lines = {0: {"L1"}, 1: {"L1"}, 2: {"L1"}, 3: {"L1"}}
        transfer_time = {}
        idx_to_name = {0: "A", 1: "B", 2: "C", 3: "D"}
        heuristic_table = [[0.0] * 4 for _ in range(4)]

        path, time = graph.find_shortest_path_astar_with_transfers(
            0, 3, edge_to_line, station_to_lines, transfer_time, idx_to_name, heuristic_table
        )

        assert path == [0, 1, 2, 3]
        assert time == 9.0

    def test_astar_with_single_transfer(self):
        data = [
            [0.0, 2.0, 0.0, 0.0],
            [2.0, 0.0, 3.0, 0.0],
            [0.0, 3.0, 0.0, 2.0],
            [0.0, 0.0, 2.0, 0.0],
        ]
        graph = Graph(data)

        edge_to_line = {
            (0, 1): "L1",
            (1, 0): "L1",
            (1, 2): "L1",
            (2, 1): "L1",
            (2, 3): "L2",
            (3, 2): "L2",
        }
        station_to_lines = {0: {"L1"}, 1: {"L1"}, 2: {"L1", "L2"}, 3: {"L2"}}
        transfer_time = {"C": {("L1", "L2"): 5.0}}
        idx_to_name = {0: "A", 1: "B", 2: "C", 3: "D"}
        heuristic_table = [[0.0] * 4 for _ in range(4)]

        path, time = graph.find_shortest_path_astar_with_transfers(
            0, 3, edge_to_line, station_to_lines, transfer_time, idx_to_name, heuristic_table
        )

        assert path == [0, 1, 2, 3]
        assert time == 12.0

    def test_astar_unreachable(self, unreachable_graph):
        path, time = unreachable_graph.find_shortest_path_astar_with_transfers(
            0,
            3,
            {},
            {0: set(), 1: set(), 2: set(), 3: set()},
            {},
            {i: str(i) for i in range(4)},
            [[float("inf")] * 4 for _ in range(4)],
        )

        assert path == []
        assert time == float("inf")

    def test_astar_same_start_end(self, weighted_graph):
        path, time = weighted_graph.find_shortest_path_astar_with_transfers(
            2,
            2,
            {},
            {i: set() for i in range(5)},
            {},
            {i: str(i) for i in range(5)},
            [[0.0] * 5 for _ in range(5)],
        )

        assert path == [2]
        assert time == 0.0

    def test_astar_zero_heuristic_behaves_like_dijkstra(self, weighted_graph):
        path_d, time_d = weighted_graph.find_shortest_path_weight(0, 3)
        edge_to_line = {
            (0, 1): "L1",
            (1, 0): "L1",
            (1, 2): "L1",
            (2, 1): "L1",
            (2, 3): "L1",
            (3, 2): "L1",
        }
        path_a, time_a = weighted_graph.find_shortest_path_astar_with_transfers(
            0,
            3,
            edge_to_line,
            {i: set() for i in range(4)},
            {},
            {i: str(i) for i in range(4)},
            [[0.0] * 4 for _ in range(4)],
        )

        assert path_a == path_d
        assert abs(time_a - time_d) < 0.01
