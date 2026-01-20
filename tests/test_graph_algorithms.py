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
        [0.0, 4.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 2.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 3.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
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
        path, time = weighted_graph.find_shortest_path_weight(0, 4)
        assert path == [0, 1, 2, 3, 4]
        assert time == 10.0

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
        assert "Path exists" in result[0]

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
        assert len(result) > 0 and "Path exists" in str(result[0])


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
