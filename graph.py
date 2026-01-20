import copy

from matrix import Matrix


class Graph:
    def __init__(self, data=[]):
        self.data = data

    def get_neighbors(self, vertex):
        neighbors = []
        for i in range(len(self.data[vertex])):
            if self.data[vertex][i] != 0:
                neighbors.append(i)
        return neighbors

    def get_degree(self, vertex):
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

    def add_edge(self, start, end, weight=1):
        self.data[start][end] = weight

    def remove_edge(self, start, end):
        self.data[start][end] = 0

    def count_edges(self):
        count = 0
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if self.data[i][j] != 0:
                    count += 1
        return count

    def is_complete(self):
        vertices_count = len(self.data)
        for i in range(vertices_count):
            for j in range(vertices_count):
                if i != j:
                    if self.data[i][j] == 0:
                        return False
        return True

    def find_shortest_path_CPX(self, start, end):
        vertices_count = len(self.data)
        if start == end:
            return [start]
        adj_matrix = Matrix(copy.deepcopy(self.data))
        matrices = [Matrix(copy.deepcopy(self.data))]
        found = False
        limit = 10

        for i in range(limit):
            if matrices[-1].data[start][end] != 0:
                found = True
                break
            matrices.append(matrices[-1] * adj_matrix)

        if not found:
            return None
        return ["Path exists (Computed via Matrix Power)"]

    def find_shortest_path_BFS(self, start, end):
        vertices_count = len(self.data)
        queue = [start]
        mat = self.data
        memory = {start: None}
        found = False
        idx = 0
        while idx < len(queue):
            curr = queue[idx]
            idx += 1
            if curr == end:
                found = True
                break
            for i in range(vertices_count):
                if mat[curr][i] != 0 and i not in memory:
                    memory[i] = curr
                    queue.append(i)
                    if i == end:
                        found = True
                        break
            if found:
                break
        if not found:
            return None
        path = []
        index = end
        while index is not None:
            path.append(index)
            index = memory[index]
        return path[::-1]

    def find_path_DFS(self, start, end):
        vertices_count = len(self.data)
        stack = [start]
        mat = self.data
        memory = {start: None}
        found = False
        while len(stack) > 0:
            curr = stack.pop()
            if curr == end:
                found = True
                break
            for i in range(vertices_count):
                if mat[curr][i] != 0 and i not in memory:
                    memory[i] = curr
                    stack.append(i)
        if not found:
            return None
        path = []
        curr_node = end
        while curr_node is not None:
            path.append(curr_node)
            curr_node = memory[curr_node]
        return path[::-1]

    def find_shortest_path_weight(self, start, end):
        vertices_count = len(self.data)
        distances = {i: float("inf") for i in range(vertices_count)}
        distances[start] = 0
        visited = [False] * vertices_count
        parent = {start: None}
        for _ in range(vertices_count):
            min_dist = float("inf")
            curr = -1
            for i in range(vertices_count):
                if not visited[i] and distances[i] < min_dist:
                    min_dist = distances[i]
                    curr = i
            if curr == -1 or distances[curr] == float("inf"):
                break
            if curr == end:
                break
            visited[curr] = True
            for i in range(vertices_count):
                weight = self.data[curr][i]
                if weight > 0 and not visited[i]:
                    new_dist = distances[curr] + weight
                    if new_dist < distances[i]:
                        distances[i] = new_dist
                        parent[i] = curr
        if end not in parent:
            return None, float("inf")
        path = []
        curr_node = end
        while curr_node is not None:
            path.append(curr_node)
            curr_node = parent[curr_node]
        return path[::-1], distances[end]

    def minimum_spanning_tree_prim(self, weights):
        n = len(weights)
        INF = float("inf")
        key = [INF] * n
        parent = [None] * n
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
                w = weights[u][v]
                if w > 0 and not mst_set[v] and w < key[v]:
                    key[v] = w
                    parent[v] = u
        mst_matrix = [[0] * n for _ in range(n)]
        total_weight = 0
        for i in range(1, n):
            if parent[i] is not None:
                u, v = parent[i], i
                weight = weights[u][v]
                mst_matrix[u][v] = weight
                mst_matrix[v][u] = weight
                total_weight += weight
        return mst_matrix, total_weight

    def connectness(self):
        start_node = 0
        q = [start_node]
        visited = {start_node}
        while q:
            u = q.pop(0)
            for v in range(len(self.data)):
                if self.data[u][v] > 0 and v not in visited:
                    visited.add(v)
                    q.append(v)
        return len(visited) == len(self.data)

    def connect_components(self):
        mat = self.data
        vertices_count = len(mat)
        visited = [False] * vertices_count
        res = []
        for index in range(vertices_count):
            if not visited[index]:
                component = []
                q = [index]
                visited[index] = True
                while q:
                    u = q.pop(0)
                    component.append(u)
                    for v in range(vertices_count):
                        if mat[u][v] > 0 and not visited[v]:
                            visited[v] = True
                            q.append(v)
                res.append(component)
        return res

    def is_bipartite_BFS(self):
        mat = self.data
        vertices_count = len(mat)
        color = {}
        for start in range(vertices_count):
            if start not in color:
                color[start] = 0
                queue = [start]
                while queue:
                    u = queue.pop(0)
                    for v in range(vertices_count):
                        if mat[u][v] != 0:
                            if v not in color:
                                color[v] = 1 - color[u]
                                queue.append(v)
                            elif color[v] == color[u]:
                                return False
        return True
