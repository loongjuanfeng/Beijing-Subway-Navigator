# Benchmark Guide for Beijing Subway Navigator

This directory contains comprehensive pytest-benchmark tests for all pathfinding algorithms.

## Overview

Two benchmark test files are provided:

1. **`test_pathfinding.py`** - Benchmarks on synthetic test graphs
   - Tests all 6 pathfinding algorithms
   - Various graph sizes: tiny (3 vertices), small (5), medium (10), dense (15), sparse (20)
   - Multiple scenarios: simple paths, branching structures, complex weighted graphs

2. **`test_real_subway.py`** - Benchmarks on real Beijing Subway data
   - Tests on actual network: ~389 stations, ~463 track segments, 26 lines
   - Real-world routes: short same-line, medium transfers, long cross-city, complex multi-transfer
   - Algorithm comparison benchmarks to verify optimality

## Algorithms Benchmarked

| Algorithm | Purpose | Benchmark Count |
|------------|---------|-----------------|
| BFS | Fewest stations (unweighted) | 6 |
| DFS | Any path (exploration) | 5 |
| Dijkstra | Minimum travel time (weighted) | 6 |
| CPX | Matrix power method (experimental) | 4 |
| Dijkstra with transfers | Fastest route with line change penalties | 3 |
| A* with transfers | Heuristic-guided fastest route | 5 |

**Total: 29 benchmarks**

## Running Benchmarks

### Run All Benchmarks

```bash
# Run all benchmarks with full output
uv run pytest tests/benchmarks/ -v

# Run benchmarks only (skip non-benchmark tests)
uv run pytest tests/benchmarks/ --benchmark-only

# Run specific benchmark file
uv run pytest tests/benchmarks/test_pathfinding.py -v
uv run pytest tests/benchmarks/test_real_subway.py -v
```

### Run with Performance Summary

```bash
# Generate performance summary table
uv run pytest tests/benchmarks/ --benchmark-only

# Save benchmark results for comparison
uv run pytest tests/benchmarks/ --benchmark-save=benchmark_results.json

# Load and compare with previous results
uv run pytest tests/benchmarks/ --benchmark-autosave --benchmark-compare=benchmark_results.json
```

### Run with Custom Settings

```bash
# Increase rounds for more accurate results (default is auto-detected)
uv run pytest tests/benchmarks/ --benchmark-min-rounds=10

# Change warmup (helps with JIT compilation)
uv run pytest tests/benchmarks/ --benchmark-warmup

# Enable garbage collection during benchmarks
uv run pytest tests/benchmarks/ --benchmark-enable-gc

# Sort by different metrics
uv run pytest tests/benchmarks/ --benchmark-only --benchmark-sort=mean
uv run pytest tests/benchmarks/ --benchmark-only --benchmark-sort=stddev
```

## Understanding Benchmark Output

### Sample Output Table

```
Name (time in us)                                    Min        Max        Mean       StdDev      Median       IQR         OPS          Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------------
test_bfs_tiny_graph                                 0.50        1.20       0.89        0.91        0.41         1,123,456.7  5       1,234,567
test_dijkstra_tiny_graph                              1.37        4.50       2.87        2.99        1.16         348,432.1    7       987,654
test_astar_transfers_with_transfer                   3.81       101.75      47.62       49.02       19.25        20,998.2      8       562,321
```

### Key Metrics

- **Min/Max**: Minimum and maximum execution time
- **Mean**: Average execution time
- **StdDev**: Standard deviation (lower is better)
- **Median**: Middle value (more stable than mean)
- **IQR**: Interquartile range
- **OPS**: Operations per second (higher is better)
- **Rounds**: Number of benchmark iterations
- **Iterations**: Total iterations across all rounds

## Benchmark Scenarios

### Synthetic Graphs (test_pathfinding.py)

| Graph | Vertices | Purpose | Algorithm Suitability |
|--------|-----------|---------|-----------------------|
| Tiny | 3 | Basic functionality | All |
| Small | 5 | Simple paths | All |
| Medium | 10 | Branching choices | All |
| Dense | 15 | Many connections | BFS/DFS (for exploration), Dijkstra/A* (weighted), CPX |
| Sparse | 20 | Linear structure | All |
| Complex Weighted | 5 | Weighted paths | Dijkstra/A* |

### Real Subway Data (test_real_subway.py)

| Route Type | Example | Complexity | Purpose |
|------------|---------|-----------|---------|
| Short same-line | 苹果园 → 八角游乐园 | Low | Baseline performance |
| Medium (1 transfer) | 西直门 → 复兴门 | Medium | Transfer handling |
| Long cross-city | 西直门 → 国贸 | High | Realistic queries |
| Hub-to-hub | 天安门东 → 北京站 | Medium | Major station routing |
| Complex multi-transfer | 苹果园 → 大兴机场 | Very High | Worst-case scenario |

## Algorithm Comparison

To compare algorithms:

```bash
# Run all and sort by mean time
uv run pytest tests/benchmarks/ --benchmark-only --benchmark-sort=mean
```

Expected performance characteristics:

| Algorithm | Time Complexity | Use Case | Expected Speed |
|------------|----------------|----------|---------------|
| BFS | O(V+E) | Unweighted shortest path | Fastest for unweighted |
| DFS | O(V+E) | Any path exploration | Variable, depends on graph structure |
| Dijkstra | O(E log V) | Weighted shortest path | Fast for small graphs |
| Dijkstra + Transfers | O(E log V) | Subway routing | Handles line changes |
| A* + Transfers | O(E log V) | Subway routing with heuristics | Faster than Dijkstra for long routes |
| CPX | O(n³) | Connectivity check | Experimental, slower |

## Coverage Note

Benchmarks are excluded from coverage requirements. Coverage is only enforced for main test suite:

```bash
# Run main tests (no benchmarks) with coverage
uv run pytest tests/ --ignore=tests/benchmarks/

# This ensures 80% coverage requirement is met
```

## Tips for Accurate Benchmarking

1. **Run multiple times**: Use `--benchmark-min-rounds` for stability
2. **Warm up**: Use `--benchmark-warmup` for consistent performance
3. **Minimize system noise**: Close other applications during benchmarks
4. **Compare over time**: Save results with `--benchmark-save` and compare changes
5. **Real-world relevance**: Focus on `test_real_subway.py` results for production insights

## Troubleshooting

### Benchmark fixture not used error

If you see `PytestBenchmarkWarning: Benchmark fixture was not used at all in this test!`:
- Ensure the test calls `benchmark(function, args...)`
- Comparison tests cannot use benchmark twice (pytest-benchmark limitation)
- Use separate tests for each algorithm instead

### Station not found errors

If benchmarks fail with station lookup errors:
- Check station names match `data/subway_lines.json`
- Real subway data uses "大兴机场", not "首都机场"
