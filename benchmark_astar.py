#!/usr/bin/env python3
"""
Benchmark script comparing Dijkstra vs A* performance.
"""

import time
from subway_navigation import BeijingSubwaySystem


def benchmark_route(system, start_name, end_name):
    start_id = system.get_station_id(start_name)
    end_id = system.get_station_id(end_name)

    if start_id is None or end_id is None:
        print(f"Error: Station not found")
        return None, None

    print(f"\n{'=' * 60}")
    print(f"Route: {start_name} → {end_name}")
    print(f"{'=' * 60}")

    # Benchmark Dijkstra
    print("\n[Dijkstra] Running...")
    t0 = time.time()
    path_d, time_d = system.graph.find_shortest_path_weight_with_transfers(
        start_id,
        end_id,
        system.edge_to_line,
        system.station_to_lines_idx,
        system.transfer_time,
        system.idx_to_name,
    )
    dijkstra_time = (time.time() - t0) * 1000
    print(f"  Time: {dijkstra_time:.2f}ms")
    print(f"  Estimated travel time: {time_d:.1f} minutes")
    print(f"  Stations: {len(path_d)}")

    # Benchmark A*
    print("\n[A*] Running...")
    t0 = time.time()
    path_a, time_a = system.graph.find_shortest_path_astar_with_transfers(
        start_id,
        end_id,
        system.edge_to_line,
        system.station_to_lines_idx,
        system.transfer_time,
        system.idx_to_name,
        system.heuristic_precompute,
    )
    astar_time = (time.time() - t0) * 1000
    print(f"  Time: {astar_time:.2f}ms")
    print(f"  Estimated travel time: {time_a:.1f} minutes")
    print(f"  Stations: {len(path_a)}")

    # Verify optimality
    print(f"\n[Verification]")
    if abs(time_d - time_a) < 0.01:
        print(f"  ✓ A* found optimal path (same cost as Dijkstra)")
        speedup = ((dijkstra_time - astar_time) / dijkstra_time) * 100
        if speedup > 0:
            print(f"  Speedup: {speedup:.1f}% faster than Dijkstra")
        else:
            print(f"  Same speed as Dijkstra")
    else:
        print(f"  ✗ A* suboptimal! Dijkstra={time_d:.2f}, A*={time_a:.2f}")

    return (dijkstra_time, astar_time), (path_d, path_a)


if __name__ == "__main__":
    print("Beijing Subway Navigator - Dijkstra vs A* Benchmark")
    print("=" * 60)

    system = BeijingSubwaySystem()

    # Trigger A* heuristic precomputation for benchmarking
    if system.heuristic_precompute is None:
        print("Precomputing A* heuristic table for benchmark...")
        system.heuristic_precompute = system._precompute_heuristic()

    # Test routes of varying distances
    test_routes = [
        ("西直门", "国贸"),  # Long cross-city route
        ("天安门东", "北京站"),  # Medium route
        ("苹果园", "八角游乐园"),  # Short route on same line
        ("西直门", "复兴门"),  # Short transfer route
    ]

    results = []
    for start, end in test_routes:
        times, paths = benchmark_route(system, start, end)
        if times:
            results.append((start, end, times[0], times[1], paths[0], paths[1]))

    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")

    print(f"\n{'Route':<30} {'Dijkstra(ms)':<15} {'A*(ms)':<15} {'Speedup':<12} {'Optimal':<10}")
    print(f"{'-' * 60}")
    for start, end, t_d, t_a, path_d, path_a in results:
        speedup = ((t_d - t_a) / t_d * 100) if t_d > 0 else 0
        optimal = (
            "✓"
            if abs(len(path_d) - len(path_a)) == 0
            and abs(
                system.graph.data[path_d[0]][path_d[1]] - system.graph.data[path_a[0]][path_a[1]]
            )
            < 0.01
            else "✗"
        )
        print(f"{start:8} → {end:8} {t_d:10.2f} {t_a:10.2f} {speedup:>6.1f}% {optimal}")
