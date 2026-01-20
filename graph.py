from __future__ import annotations

import copy

from matrix import Matrix


class Graph:
    data: list[list[float]]

    def __init__(self, data: list[list[float]] | None = None) -> None:
        if data is None:
            self.data = []
        else:
            self.data = data

    def get_neighbors(self, vertex: int) -> list[int]:
        neighbors = []
        for i in range(len(self.data[vertex])):
            if self.data[vertex][i] != 0:
                neighbors.append(i)
        return neighbors

    def get_degree(self, vertex: int) -> tuple[int, int]:
        out_degree = 0
        in_degree = 0
        vertices_count = len(self.data)
        for i in range(vertices_count):
            if self.data[vertex][i] != 0:
                out_degree += 1
        for j in range(vertices_count):
            if self.data[j][vertex] != 0:
                in_degree += 1
        return (out_degree, in_degree)

    def add_edge(self, start: int, end: int, weight: float = 1) -> None:
        self.data[start][end] = weight

    def remove_edge(self, start: int, end: int) -> None:
        self.data[start][end] = 0

    def count_edges(self) -> int:
        count = 0
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if self.data[i][j] != 0:
                    count += 1
        return count

    def is_complete(self) -> bool:
        vertices_count = len(self.data)
        for i in range(vertices_count):
            for j in range(vertices_count):
                if i != j:
                    if self.data[i][j] == 0:
                        return False
        return True

    def _reconstruct_path(self, parent: dict[int, int | None], end: int) -> list[int]:
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent[current]
        return path[::-1]

    def _reconstruct_path_with_state(
        self,
        parent: dict[tuple[int, str | None], tuple[int, str | None] | None],
        end: tuple[int, str | None],
    ) -> list[int]:
        path = []
        current = end
        while current is not None:
            station, line = current
            path.append(station)
            current = parent[current]
        return path[::-1]

    def _reconstruct_cpx_path(
        self, matrices: list[Matrix], k: int, start: int, end: int
    ) -> list[int]:
        """Reconstruct path from matrix powers. k is path length (number of edges)."""
        if k == 1:
            return [start, end]

        for m in range(len(matrices[0].data)):
            if matrices[0].data[start][m] != 0 and matrices[k - 2].data[m][end] != 0:
                rest_path = self._reconstruct_cpx_path(matrices, k - 1, m, end)
                return [start] + rest_path

        return []

    def find_shortest_path_cpx(self, start: int, end: int) -> list[int] | None:
        if start == end:
            return [start]
        adj_matrix = Matrix(copy.deepcopy(self.data))
        matrices = [Matrix(copy.deepcopy(self.data))]
        found = False
        limit = 10
        path_length = 0

        for i in range(limit):
            if matrices[-1].data[start][end] != 0:
                found = True
                path_length = i + 1
                break
            matrices.append(matrices[-1] * adj_matrix)

        if not found:
            return None
        return self._reconstruct_cpx_path(matrices, path_length, start, end)

    def find_shortest_path_bfs(self, start: int, end: int) -> list[int] | None:
        vertices_count = len(self.data)
        queue = [start]
        matrix = self.data
        memory: dict[int, int | None] = {start: None}
        found = False
        queue_index = 0
        while queue_index < len(queue):
            current = queue[queue_index]
            queue_index += 1
            if current == end:
                found = True
                break
            for i in range(vertices_count):
                if matrix[current][i] != 0 and i not in memory:
                    memory[i] = current
                    queue.append(i)
                    if i == end:
                        found = True
                        break
            if found:
                break
        if not found:
            return None
        return self._reconstruct_path(memory, end)

    def find_path_dfs(self, start: int, end: int) -> list[int] | None:
        vertices_count = len(self.data)
        stack = [start]
        matrix = self.data
        memory: dict[int, int | None] = {start: None}
        found = False
        while len(stack) > 0:
            current = stack.pop()
            if current == end:
                found = True
                break
            for i in range(vertices_count):
                if matrix[current][i] != 0 and i not in memory:
                    memory[i] = current
                    stack.append(i)
        if not found:
            return None
        return self._reconstruct_path(memory, end)

    def find_shortest_path_weight(
        self, start: int, end: int
    ) -> tuple[list[int], float] | tuple[None, float]:
        vertices_count = len(self.data)
        distances: dict[int, float] = {i: float("inf") for i in range(vertices_count)}
        distances[start] = 0
        visited = [False] * vertices_count
        parent: dict[int, int | None] = {start: None}
        for _ in range(vertices_count):
            min_dist = float("inf")
            current = -1
            for i in range(vertices_count):
                if not visited[i] and distances[i] < min_dist:
                    min_dist = distances[i]
                    current = i
            if current == -1 or distances[current] == float("inf"):
                break
            if current == end:
                break
            visited[current] = True
            for i in range(vertices_count):
                weight = self.data[current][i]
                if weight > 0 and not visited[i]:
                    new_dist = distances[current] + weight
                    if new_dist < distances[i]:
                        distances[i] = new_dist
                        parent[i] = current
        if end not in parent:
            return None, float("inf")
        return self._reconstruct_path(parent, end), distances[end]

    def find_shortest_path_weight_with_transfers(
        self,
        start: int,
        end: int,
        edge_to_line: dict[tuple[int, int], str],
        station_to_lines: dict[int, set[str]],
        transfer_time: dict[str, dict[tuple[str, str], float]],
        idx_to_name: dict[int, str],
    ) -> tuple[list[int], float]:
        vertices_count = len(self.data)

        distances: dict[tuple[int, str | None], float] = {(start, None): 0.0}
        parent: dict[tuple[int, str | None], tuple[int, str | None] | None] = {(start, None): None}
        visited: set[tuple[int, str | None]] = set()

        import heapq

        heap = [(0.0, start, None)]

        while heap:
            curr_time, curr_station, curr_line = heapq.heappop(heap)

            state = (curr_station, curr_line)
            if state in visited:
                continue
            visited.add(state)

            if curr_station == end:
                break

            for neighbor in self.get_neighbors(curr_station):
                edge_line = edge_to_line.get((curr_station, neighbor))
                if edge_line is None:
                    continue

                edge_weight = self.data[curr_station][neighbor]
                new_time = curr_time + edge_weight
                new_line = edge_line

                if curr_line is not None and curr_line != new_line:
                    station_name = idx_to_name.get(curr_station, "")
                    transfer_key = (curr_line, new_line)
                    penalty = transfer_time.get(station_name, {}).get(transfer_key, 0.0)
                    new_time += penalty

                new_state = (neighbor, new_line)
                if new_state not in distances or new_time < distances[new_state]:
                    distances[new_state] = new_time
                    parent[new_state] = state
                    heapq.heappush(heap, (new_time, neighbor, new_line))

        best_state = None
        best_time = float("inf")
        for (station, line), time in distances.items():
            if station == end and time < best_time:
                best_time = time
                best_state = (station, line)

        if best_state is None:
            return [], float("inf")

        path = self._reconstruct_path_with_state(parent, best_state)
        return path, best_time

    def minimum_spanning_tree_prim(
        self, weights: list[list[float]]
    ) -> tuple[list[list[float]], float]:
        n = len(weights)
        INF = float("inf")
        key = [INF] * n
        parent: list[int | None] = [None] * n
        mst_set = [False] * n
        key[0] = 0
        parent[0] = -1
        for _ in range(n):
            min_val = INF
            u = -1
            for v in range(n):
                if not mst_set[v] and key[v] < min_val:
                    min_val = key[v]
                    u = v
            if u == -1:
                break
            mst_set[u] = True
            for v in range(n):
                weight = weights[u][v]
                if weight > 0 and not mst_set[v] and weight < key[v]:
                    key[v] = weight
                    parent[v] = u
        mst_matrix: list[list[float]] = [[0.0] * n for _ in range(n)]
        total_weight = 0.0
        for i in range(1, n):
            parent_vertex = parent[i]
            if parent_vertex is not None:
                u, v = parent_vertex, i
                weight = weights[u][v]
                mst_matrix[u][v] = weight
                mst_matrix[v][u] = weight
                total_weight += weight
        return mst_matrix, total_weight

    def is_connected(self) -> bool:
        start_node = 0
        queue = [start_node]
        visited = {start_node}
        while queue:
            u = queue.pop(0)
            for v in range(len(self.data)):
                if self.data[u][v] > 0 and v not in visited:
                    visited.add(v)
                    queue.append(v)
        return len(visited) == len(self.data)

    def connected_components(self) -> list[list[int]]:
        matrix = self.data
        vertices_count = len(matrix)
        visited = [False] * vertices_count
        result = []
        for index in range(vertices_count):
            if not visited[index]:
                component = []
                queue = [index]
                visited[index] = True
                while queue:
                    u = queue.pop(0)
                    component.append(u)
                    for v in range(vertices_count):
                        if matrix[u][v] > 0 and not visited[v]:
                            visited[v] = True
                            queue.append(v)
                result.append(component)
        return result

    def is_bipartite_bfs(self) -> bool:
        matrix = self.data
        vertices_count = len(matrix)
        color: dict[int, int] = {}
        for start in range(vertices_count):
            if start not in color:
                color[start] = 0
                queue = [start]
                while queue:
                    u = queue.pop(0)
                    for v in range(vertices_count):
                        if matrix[u][v] != 0:
                            if v not in color:
                                color[v] = 1 - color[u]
                                queue.append(v)
                            elif color[v] == color[u]:
                                return False
        return True
