import copy
import json
import os


class Matrix:
    def __init__(self, data=None, dim=None, init_value=0):
        if data == None and dim == None:
            raise ValueError("1-1: Lack enough variables")
        if data is not None:
            if not isinstance(data, list):
                raise TypeError("1-2: The data should be a nested list")
            else:
                for i in range(len(data)):
                    if i == 0:
                        if not isinstance(data[i], list):
                            raise TypeError("1-3: All the elements in 'data' should be a list")
                        else:
                            continue
                    else:
                        if (not isinstance(data[i], list)) or (len(data[i]) != len(data[i - 1])):
                            raise TypeError(
                                "1-4: All the elements in 'data' should be a list and they must have the same lenth to be a matrix"
                            )
                        else:
                            continue
            if len(data) == 0:
                self.data = []
                self.dim = (0, 0)
                self.init_value = init_value
            else:
                row_num = len(data)
                col_num = len(data[0])
                dim = (row_num, col_num)
        else:
            if not isinstance(dim, tuple):
                raise TypeError("1-5: The variable 'dim' should be a tuple")
            if len(dim) != 2:
                raise ValueError("1-6: The tuple 'dim' should contains two elements")
            m, n = dim
            if not (isinstance(m, int) and isinstance(n, int)):
                raise TypeError("1-7: The elements in 'dim' should be integers")
            data = [[init_value for _ in range(n)] for _ in range(m)]
        self.data = data
        self.dim = dim
        self.init_value = init_value

    def T(self):
        if not isinstance(self, Matrix):
            raise TypeError("5-1: Only Matrix objects can be transposed")
        res = []
        for i in range(len(self.data[0])):
            new_row = []
            for j in range(len(self.data)):
                new_row.append(self.data[j][i])
            res.append(new_row)
        return Matrix(res)

    def __pow__(self, n):
        if not isinstance(n, int):
            raise TypeError("11-1: Exponent must be an integer")
        if not isinstance(self, Matrix):
            raise TypeError("11-2: Only Matrix objects can be exponentiated")
        if len(self.data) == 0 or len(self.data[0]) == 0:
            raise ValueError("11-3: We do not accept empty matrix and list")
        if len(self.data) != len(self.data[0]):
            return ValueError("11-4: Only square matrix can be exponentiated")
        res = Matrix(data=self.data)
        for _ in range(n - 1):
            res = res * self
            res = Matrix(data=res.data)
        return res

    def __add__(self, other):
        if (not isinstance(self, Matrix)) or (not isinstance(other, Matrix)):
            raise TypeError("12-1: Only Matrix objects can be added")
        res = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data[0])):
                row.append(self.data[i][j] + other.data[i][j])
            res.append(row)
        return Matrix(data=res)

    def __mul__(self, other):
        if not (isinstance(self, Matrix) and isinstance(other, Matrix)):
            raise TypeError("4-1: Self and other should be Matrix obects")
        new_self = self.data
        new_other = (other.T()).data
        width = len(new_self[0])
        res = []
        for i in range(len(new_self)):
            new_row = []
            for j in range(len(new_other)):
                new_ele = 0
                for k in range(width):
                    new_ele += new_self[i][k] * new_other[j][k]
                new_row.append(new_ele)
            res.append(new_row)
        return Matrix(data=res)


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


class BeijingSubwaySystem:
    def __init__(self):
        print("Initializing Beijing Subway Network Data...")
        self.stations = set()
        self.edges = []

        self.hell_stations = {"西直门", "东直门", "国贸", "望京西", "平安里"}

        try:
            with open("data/subway_lines.json", "r", encoding="utf-8") as f:
                subway_lines = json.load(f)

            for line_name, line_data in subway_lines.items():
                segments = line_data["segments"]
                for segment in segments:
                    u = segment["from"]
                    v = segment["to"]
                    t = segment["distance_minutes"]
                    self.stations.add(u)
                    self.stations.add(v)
                    self.edges.append((u, v, t))

        except FileNotFoundError as e:
            print(f"Error: Could not find data file - {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in data file - {e}")
            raise
        except Exception as e:
            print(f"Error: Unexpected error loading subway data - {e}")
            raise

        self.sorted_stations = sorted(list(self.stations))
        self.n = len(self.sorted_stations)
        self.name_to_idx = {name: i for i, name in enumerate(self.sorted_stations)}
        self.idx_to_name = {i: name for i, name in enumerate(self.sorted_stations)}

        matrix_data = [[0] * self.n for _ in range(self.n)]
        for u, v, t in self.edges:
            ui, vi = self.name_to_idx[u], self.name_to_idx[v]
            matrix_data[ui][vi] = t
            matrix_data[vi][ui] = t

        self.graph = Graph(matrix_data)
        print(
            f"Initialization Complete! Loaded {self.n} stations and {self.graph.count_edges() // 2} track segments."
        )

    def get_station_id(self, name):
        return self.name_to_idx.get(name)

    def print_path(self, path_indices, detail_type="simple"):
        if not path_indices:
            print("No path found.")
            return

        names = [self.idx_to_name[i] for i in path_indices]
        if detail_type == "simple":
            print(" -> ".join(names))

        detected_hell_stations = [name for name in names if name in self.hell_stations]
        if detected_hell_stations:
            print(
                f"This route involves stations known for difficult, long, or crowded transfers: {', '.join(detected_hell_stations)}"
            )
            print("Please prepare for long walks or stairs.")
            print("This route may not be the best route in real life.")

        return names

    def run_interactive(self):
        while True:
            print("\n" + "=" * 50)
            print("   Beijing Subway Graph Navigation System")
            print("=" * 50)
            print("1. [Dijkstra] Fastest Route (Time Weighted)")
            print("2. [BFS] Least Stops Route")
            print("3. [DFS] Random Exploration Path")
            print("4. [Prim] Calculate MST Cost (Total Network Length)")
            print("5. [Degree] Station Hub Analysis")
            print("6. [Matrix] Algebraic Connectivity Path (CPX Experiment)")
            print("7. [Components] Check Network Connectivity")
            print("8. [Simulation] Simulate Line Disruption (Remove Edge)")
            print("0. Exit")
            print("=" * 50)

            choice = input("Enter option number: ")

            if choice == "0":
                break

            elif choice in ["1", "2", "3", "6"]:
                start_name = input("Enter start station (e.g., 西直门): ")
                end_name = input("Enter end station (e.g., 国贸): ")

                s_id = self.get_station_id(start_name)
                e_id = self.get_station_id(end_name)

                if s_id is None or e_id is None:
                    print("Error: Station name does not exist. Please check your input.")
                    continue

                if choice == "1":
                    print(
                        f"\nCalculating fastest route from {start_name} to {end_name} (Dijkstra)..."
                    )
                    path, time = self.graph.find_shortest_path_weight(s_id, e_id)
                    if path:
                        print(f"Estimated Time: {time} minutes")
                        print("Route:")
                        self.print_path(path)
                    else:
                        print("Destination unreachable.")

                elif choice == "2":
                    print(
                        f"\nCalculating route with fewest stops from {start_name} to {end_name} (BFS)..."
                    )
                    path = self.graph.find_shortest_path_BFS(s_id, e_id)
                    if path:
                        print(f"Total Stops: {len(path)} stations")
                        self.print_path(path)

                elif choice == "3":
                    print(f"\nSearching for a feasible path (DFS)...")
                    path = self.graph.find_path_DFS(s_id, e_id)
                    self.print_path(path)

                elif choice == "6":
                    print(f"\n[Experimental] Computing path via Matrix Multiplication (CPX)...")
                    res = self.graph.find_shortest_path_CPX(s_id, e_id)
                    print(f"CPX Result: {res}")

            elif choice == "4":
                print("\nCalculating Minimum Spanning Tree (Prim's Algorithm)...")
                mst, cost = self.graph.minimum_spanning_tree_prim(self.graph.data)
                print(f"Minimum weighted length to connect all {self.n} stations: {cost}")

            elif choice == "5":
                name = input("Enter station name to query: ")
                sid = self.get_station_id(name)
                if sid is not None:
                    out_d, in_d = self.graph.get_degree(sid)
                    neighbors = self.graph.get_neighbors(sid)
                    n_names = [self.idx_to_name[i] for i in neighbors]
                    print(f"\nAnalysis for {name}:")
                    print(f"- Connectivity Degree: {out_d}")
                    print(f"- Neighboring Stations: {', '.join(n_names)}")
                    if out_d > 2:
                        print("- Verdict: This is a Transfer Hub.")
                    else:
                        print("- Verdict: Regular Stop.")

            elif choice == "7":
                print("\nAnalyzing network structure...")
                is_connected = self.graph.connectness()
                components = self.graph.connect_components()
                print(f"Is network fully connected: {is_connected}")
                print(f"Number of Connected Components: {len(components)}")
                if not is_connected:
                    print("Warning: Isolated station groups detected!")

                print("\nChecking Bipartite Property (BFS)...")
                is_bi = self.graph.is_bipartite_BFS()
                print(f"Is Bipartite Graph: {is_bi}")

            elif choice == "8":
                print("\nSimulating Construction/Failure Mode...")
                u_name = input("Enter disruption start station: ")
                v_name = input("Enter disruption end station: ")
                u, v = self.get_station_id(u_name), self.get_station_id(v_name)
                if u is not None and v is not None:
                    print(f"Cutting connection between {u_name} <-> {v_name}...")
                    self.graph.remove_edge(u, v)
                    self.graph.remove_edge(v, u)
                    print("Line segment disrupted. Please replan route to see effects.")

            else:
                print("Invalid input.")


if __name__ == "__main__":
    subway_system = BeijingSubwaySystem()
    try:
        subway_system.run_interactive()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
