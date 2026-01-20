import json
import os

from graph import Graph


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
