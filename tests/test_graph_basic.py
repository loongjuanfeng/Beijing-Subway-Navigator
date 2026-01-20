import pytest

from graph import Graph


@pytest.fixture
def empty_graph():
    return Graph()


@pytest.fixture
def simple_graph():
    data = [
        [0.0, 1.0, 1.0, 0.0],
        [0.0, 0.0, 1.0, 1.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 0.0],
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
def undirected_graph():
    data = [
        [0.0, 1.0, 1.0, 0.0],
        [1.0, 0.0, 1.0, 0.0],
        [1.0, 1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, 0.0],
    ]
    return Graph(data)


@pytest.fixture
def complete_graph():
    n = 4
    data = [[1.0 if i != j else 0.0 for j in range(n)] for i in range(n)]
    return Graph(data)


class TestGraphInitialization:
    def test_empty_graph_creation(self, empty_graph):
        assert empty_graph.data == []

    def test_graph_with_data_creation(self, simple_graph):
        assert len(simple_graph.data) == 4
        assert simple_graph.data[0][1] == 1

    def test_none_data_creates_empty_graph(self):
        graph = Graph(None)
        assert graph.data == []


class TestGraphEdges:
    def test_add_edge(self, empty_graph):
        empty_graph.data = [[0, 0], [0, 0]]
        empty_graph.add_edge(0, 1, 2.5)
        assert empty_graph.data[0][1] == 2.5

    def test_add_edge_with_default_weight(self, simple_graph):
        simple_graph.add_edge(0, 2, 3.0)
        assert simple_graph.data[0][2] == 3.0

    def test_remove_edge(self, simple_graph):
        simple_graph.remove_edge(0, 1)
        assert simple_graph.data[0][1] == 0

    def test_count_edges(self, simple_graph):
        assert simple_graph.count_edges() == 5

    def test_count_edges_empty_graph(self, empty_graph):
        assert empty_graph.count_edges() == 0


class TestGraphNeighborsAndDegree:
    def test_get_neighbors(self, simple_graph):
        neighbors = simple_graph.get_neighbors(0)
        assert sorted(neighbors) == [1, 2]

    def test_get_neighbors_no_edges(self, simple_graph):
        neighbors = simple_graph.get_neighbors(3)
        assert neighbors == []

    def test_get_degree_directed_graph(self, simple_graph):
        out_degree, in_degree = simple_graph.get_degree(1)
        assert out_degree == 2
        assert in_degree == 1

    def test_get_degree_undirected_graph(self, undirected_graph):
        out_degree, in_degree = undirected_graph.get_degree(1)
        assert out_degree == 2
        assert in_degree == 2


class TestGraphProperties:
    def test_is_complete_true(self, complete_graph):
        assert complete_graph.is_complete() is True

    def test_is_complete_false(self, simple_graph):
        assert simple_graph.is_complete() is False

    def test_is_connected_true(self, undirected_graph):
        assert undirected_graph.is_connected() is True

    def test_is_connected_false(self):
        data = [
            [0.0, 1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
        graph = Graph(data)
        assert graph.is_connected() is False

    def test_connected_components_one_component(self, undirected_graph):
        components = undirected_graph.connected_components()
        assert len(components) == 1
        assert sorted(components[0]) == [0, 1, 2, 3]

    def test_connected_components_multiple(self):
        data = [
            [0.0, 1.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0],
            [0.0, 0.0, 1.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 1.0, 0.0],
        ]
        graph = Graph(data)
        components = graph.connected_components()
        assert len(components) == 2
        assert sorted(components[0]) == [0, 1]
        assert sorted(components[1]) == [2, 3, 4]

    def test_is_bipartite_true(self):
        data = [
            [0.0, 1.0, 1.0, 0.0],
            [1.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 1.0],
            [0.0, 1.0, 1.0, 0.0],
        ]
        graph = Graph(data)
        assert graph.is_bipartite_bfs() is True

    def test_is_bipartite_false(self):
        data = [
            [0.0, 1.0, 1.0, 0.0],
            [1.0, 0.0, 1.0, 1.0],
            [1.0, 1.0, 0.0, 1.0],
            [0.0, 1.0, 1.0, 0.0],
        ]
        graph = Graph(data)
        assert graph.is_bipartite_bfs() is False
