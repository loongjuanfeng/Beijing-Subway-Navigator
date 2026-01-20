# 🚇 Beijing Subway Graph Navigation

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/coverage-99.55%25-success)
![Status](https://img.shields.io/badge/status-active-success)

> **Terminal-based Beijing Subway navigator with custom Matrix and Graph implementations.**

## 📖 Overview

Simulates Beijing's subway network as a weighted undirected graph using pure Python—no numpy, no networkx. Implements core graph theory algorithms from scratch including Dijkstra, BFS, DFS, Prim's MST, and CPX (Matrix Power) pathfinding.

**Network Scale:** 26 subway lines, ~475 stations, ~950 track segments

### Data Source
Travel times sourced from [北京地铁区间用时地图 250124版本](https://search.bilibili.com/all?keyword=北京地铁区间用时地图%20250124版本)

## ✨ Features

| Feature | Algorithm | Description |
|---------|-----------|-------------|
| ⏱️ Fastest Route | Dijkstra | Minimum travel time (time-weighted) |
| 🛑 Least Stops | BFS | Fewest stations visited |
| 🧪 Random Path | DFS | Any feasible path (exploration) |
| 🔬 CPX Check | Matrix Power | Algebraic connectivity path check (experimental) |
| 🌐 Network Cost | Prim's MST | Minimum length to connect all stations |
| 🔍 Hub Analysis | Degree Centrality | Identifies transfer hubs vs regular stops |
| 📊 Connectivity | BFS/DFS | Check network connectedness and components |
| 🚧 Disruption | Edge Removal | Simulate track failures |
| ⚠️ Hell Stations | Custom Set | Warns about difficult transfers |

### 🌍 Internationalization

Supports English and Chinese via GNU gettext:
```bash
LANGUAGE=zh python subway_navigation.py  # Chinese
LANGUAGE=en python subway_navigation.py  # English
```

See [I18N_USAGE.md](./I18N_USAGE.md) for adding new languages.

## ⚠️ Limitations

**Historical Limitation (Now Resolved):** Earlier versions treated transfers as zero-cost, which could recommend transfers at complex hubs (西直门, 东直门) despite 8+ minute walks. Hell station warnings were the only mitigation.

**Current Implementation:** Transfer times from `interchange_stations.json` are now integrated into route calculations. Dijkstra's algorithm with line state tracking applies transfer penalties when switching lines, providing more accurate travel time estimates. Asymmetric transfer times (e.g., 复兴门: 2号线→1号线=0.42min vs 1号线→2号线=2.5min) are fully supported.

## 🛠 Technical Stack

**Core:** Python 3.12+ (no runtime dependencies)

**Dev:**
- `pytest` — Testing framework
- `pytest-cov` — Coverage reporting (99.55%)
- `pytest-xdist` — Parallel test execution
- `ruff` — Linting & formatting
- `uv` — Package manager

**Custom Implementations:**
- `Matrix` class — Linear algebra operations
- `Graph` class — Adjacency matrix + 15+ algorithms

## ⚡ Getting Started

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended)

### Installation

```bash
# Clone repository
git clone <repo-url>
cd Beijing-Subway-Navigator

# Install dev dependencies with uv
uv sync
```

### Running

```bash
# Direct execution
python subway_navigation.py

# With uv
uv run python subway_navigation.py

# With language selection
LANGUAGE=zh uv run python subway_navigation.py
```

### Interactive Menu

```
==================================================
   Beijing Subway Graph Navigation System
==================================================
1. [Dijkstra] Fastest Route (Time Weighted)
2. [BFS] Least Stops Route
3. [DFS] Random Exploration Path
4. [Prim] Calculate MST Cost (Total Network Length)
5. [Degree] Station Hub Analysis
6. [Matrix] Algebraic Connectivity Path (CPX Experiment)
7. [Components] Check Network Connectivity
8. [Simulation] Simulate Line Disruption (Remove Edge)
0. Exit
==================================================
```

## 🧪 Testing

**Coverage:** 99.55% (220/221 statements) — Enforced minimum: 80%

```bash
# Run all tests
uv run pytest

# Verbose output
uv run pytest -v

# Specific test file
uv run pytest tests/test_graph_algorithms.py

# With coverage report
uv run pytest --cov=graph --cov-report=term-missing

# Parallel execution (faster)
uv run pytest -n auto

# Generate HTML coverage
uv run pytest --cov=graph --cov-report=html
# Open htmlcov/index.html in browser
```

See [tests/README.md](./tests/README.md) for detailed test documentation.

## 📁 Project Structure

```
Beijing-Subway-Navigator/
├── subway_navigation.py    # Main entry point & CLI (343 lines)
├── graph.py                # Graph class + algorithms (248 lines)
├── matrix.py               # Matrix class (107 lines)
├── pyproject.toml          # Project config
├── babel.cfg               # i18n extraction config
├── data/                   # Subway network data
│   ├── subway_lines.json           # 26 lines + segments
│   └── interchange_stations.json   # Transfer time data (integrated into routing)
├── locale/                 # Translations (en/zh)
│   └── messages.pot
└── tests/                  # Test suite (99.55% coverage)
    ├── test_graph_basic.py
    ├── test_graph_algorithms.py
    └── test_graph_properties.py
```

## 🚀 Example Usage

**Finding fastest route from 西直门 to 国贸:**

```text
Enter option number: 1
Enter start station: 西直门
Enter end station: 国贸

Calculating fastest route...
Estimated Time: 28 minutes
Route: 西直门 -> 车公庄 -> 平安里 -> 南锣鼓巷 -> 东四 -> 朝阳门 -> 建国门 -> 永安里 -> 国贸
⚠️ This route involves stations known for difficult transfers: 西直门, 平安里, 国贸
Please prepare for long walks or stairs.
```

## 📊 Data Format

```json
{
  "1号线": {
    "name": "1号线",
    "stations": ["苹果园", "古城", "八角游乐园", ...],
    "segments": [
      {"from": "苹果园", "to": "古城", "distance_minutes": 3.0},
      ...
    ],
    "total_stations": 35
  }
}
```

Modify `data/subway_lines.json` to update network data.

## 🤝 Contributing

Contributions welcome! Please:
1. Run tests: `uv run pytest`
2. Ensure coverage stays >80%
3. Follow code style: `uv run ruff format .`

## 📄 License

MIT
