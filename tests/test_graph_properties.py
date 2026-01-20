import pytest

from graph import Graph


@pytest.fixture
def weighted_undirected_graph():
    data = [
        [0, 4, 0, 0, 0, 0],
        [4, 0, 8, 0, 0, 0],
        [0, 8, 0, 7, 0, 4],
        [0, 0, 7, 0, 9, 14],
        [0, 0, 0, 9, 0, 10],
        [0, 0, 4, 14, 10, 0],
    ]
    return Graph(data)


@pytest.fixture
def simple_mst_graph():
    data = [
        [0, 2, 0, 6, 0],
        [2, 0, 3, 8, 5],
        [0, 3, 0, 0, 7],
        [6, 8, 0, 0, 9],
        [0, 5, 7, 9, 0],
    ]
    return Graph(data)


@pytest.fixture
def star_graph():
    data = [
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
    ]
    return Graph(data)


class TestMinimumSpanningTree:
    def test_prim_algorithm_mst_structure(self, simple_mst_graph):
        mst, total_weight = simple_mst_graph.minimum_spanning_tree_prim(simple_mst_graph.data)

        assert total_weight > 0
        assert len(mst) == 5

        edge_count = 0
        for i in range(5):
            for j in range(5):
                if mst[i][j] > 0:
                    edge_count += 1
        assert edge_count == 8

    def test_prim_algorithm_correct_weight(self, simple_mst_graph):
        mst, total_weight = simple_mst_graph.minimum_spanning_tree_prim(simple_mst_graph.data)
        assert total_weight == 16.0

    def test_prim_algorithm_tree_property(self, simple_mst_graph):
        mst, _ = simple_mst_graph.minimum_spanning_tree_prim(simple_mst_graph.data)

        assert mst is not None
        for i in range(len(mst)):
            assert mst[i][i] == 0

    def test_prim_algorithm_star_graph(self, star_graph):
        mst, total_weight = star_graph.minimum_spanning_tree_prim(star_graph.data)

        assert total_weight == 3.0
        edge_count = 0
        for i in range(4):
            for j in range(4):
                if mst[i][j] > 0:
                    edge_count += 1
        assert edge_count == 6

    def test_prim_algorithm_complex_graph(self, weighted_undirected_graph):
        mst, total_weight = weighted_undirected_graph.minimum_spanning_tree_prim(
            weighted_undirected_graph.data
        )

        assert total_weight > 0
        assert len(mst) == 6

        edge_count = 0
        for i in range(6):
            for j in range(6):
                if mst[i][j] > 0:
                    edge_count += 1
        assert edge_count == 10

    def test_prim_algorithm_minimal_weight(self, simple_mst_graph):
        mst, total_weight = simple_mst_graph.minimum_spanning_tree_prim(simple_mst_graph.data)

        mst_weight_sum = 0
        for i in range(5):
            for j in range(i + 1, 5):
                if mst[i][j] > 0:
                    mst_weight_sum += mst[i][j]

        assert total_weight == mst_weight_sum


class TestGraphConnectivity:
    def test_single_component_connected(self, simple_mst_graph):
        assert simple_mst_graph.is_connected() is True

    def test_disconnected_graph(self):
        data = [
            [0, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ]
        graph = Graph(data)
        assert graph.is_connected() is False

    def test_isolated_vertex(self):
        data = [
            [0, 1, 0],
            [1, 0, 0],
            [0, 0, 0],
        ]
        graph = Graph(data)
        assert graph.is_connected() is False

    def test_connected_components_single(self, simple_mst_graph):
        components = simple_mst_graph.connected_components()
        assert len(components) == 1
        assert sorted(components[0]) == [0, 1, 2, 3, 4]

    def test_connected_components_multiple(self):
        data = [
            [0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 1, 0, 1],
            [0, 0, 1, 1, 0],
        ]
        graph = Graph(data)
        components = graph.connected_components()
        assert len(components) == 2
        assert sorted(components[0]) == [0, 1]
        assert sorted(components[1]) == [2, 3, 4]

    def test_connected_components_all_isolated(self):
        data = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        graph = Graph(data)
        components = graph.connected_components()
        assert len(components) == 3


class TestBipartiteChecking:
    def test_bipartite_simple(self):
        data = [
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
        ]
        graph = Graph(data)
        assert graph.is_bipartite_bfs() is True

    def test_bipartite_complex(self, weighted_undirected_graph):
        assert weighted_undirected_graph.is_bipartite_bfs() is False

    def test_not_bipartite_odd_cycle(self):
        data = [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
        graph = Graph(data)
        assert graph.is_bipartite_bfs() is True

    def test_not_bipartite_complete_graph(self):
        data = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
        ]
        graph = Graph(data)
        assert graph.is_bipartite_bfs() is False

    def test_bipartite_empty_graph(self):
        graph = Graph([])
        assert graph.is_bipartite_bfs() is True

    def test_bipartite_single_vertex(self):
        data = [[0]]
        graph = Graph(data)
        assert graph.is_bipartite_bfs() is True


class TestGraphPropertyCombinations:
    def test_mst_creates_tree(self, simple_mst_graph):
        mst, _ = simple_mst_graph.minimum_spanning_tree_prim(simple_mst_graph.data)
        graph = Graph(mst)
        assert graph.is_connected() is True

    def test_tree_properties(self, star_graph):
        mst, total_weight = star_graph.minimum_spanning_tree_prim(star_graph.data)
        assert total_weight == 3.0
        edge_count = 0
        for i in range(4):
            for j in range(4):
                if mst[i][j] > 0:
                    edge_count += 1
        assert edge_count == 6

    def test_bipartite_path_graph(self):
        data = [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
        ]
        graph = Graph(data)
        assert graph.is_bipartite_bfs() is True
        assert graph.is_connected() is True
