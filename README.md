# 🚇 Beijing Subway Graph Navigation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

> **A terminal-based navigation system for the Beijing Subway, built from scratch using custom Matrix and Graph implementations.**

## 📖 About The Project

This project simulates the Beijing Subway network as a weighted undirected graph. unlike standard navigation tools that rely on libraries like `networkx` or `numpy`, this project implements **core linear algebra and graph theory concepts from scratch**.

It features a custom `Matrix` class for algebraic operations and a `Graph` class capable of complex topological analysis, including shortest path finding, minimum spanning tree calculation, and network resilience testing.

### 📊 Data Source & Format

The subway network data is stored in JSON format for easy maintenance and updates:

**Data Files:**
- `data/subway_lines.json` - Contains all 26 subway lines with stations and segment distances
- `data/interchange_stations.json` - Transfer station data (available for future use)

**Data Structure:**
```json
{
  "1号线": {
    "name": "1号线",
    "stations": ["苹果园", "古城", "八角游乐园", ...],
    "segments": [
      {"from": "苹果园", "to": "古城", "distance_minutes": 3.0},
      ...
    ],
    "total_stations": 36
  }
}
```

**Source Data:**
The edge weights (travel times between stations) are based on:
* **Source:** [北京地铁区间用时地图 250124版本 - 哔哩哔哩](https://search.bilibili.com/all?keyword=北京地铁区间用时地图%20250124版本)

## ⚠️ Limitations

* **No Transfer Time Estimation:**
    The current algorithm calculates travel time based solely on station-to-station track intervals. It **does not account for the walking time required to transfer between lines**.
    * *Consequence:* The system treats transfers as instantaneous (zero-cost). This may result in recommended routes that are mathematically fastest on the rails but practically slower due to **extremely long walking distances** at complex transfer hubs (e.g., swapping lines at *Xizhimen* or *Ping'anli*).

## ✨ Key Features

The system offers an interactive CLI with the following capabilities:

* **⏱️ Fastest Route (Dijkstra):** Calculates the path with the minimum travel time using edge weights.
* **🛑 Least Stops (BFS):** Finds the route with the fewest number of station transfers using Breadth-First Search.
* **🌐 Network Cost (Prim's MST):** Computes the Minimum Spanning Tree to determine the minimum total length required to connect all stations.
* **🔍 Hub Analysis (Degree Centrality):** Identifies transfer hubs versus regular stops based on vertex degree.
* **🧪 Experimental Routing (Matrix Power):** Checks path existence via adjacency matrix multiplication (CPX method).
* **🚧 Disruption Simulation:** Allows users to dynamically remove edges (tracks) to simulate engineering failures and observe network effects.
* **⚠️ "Hell Station" Detection:** Automatically warns users if their route passes through notorious transfer stations (e.g., Xizhimen, Dongzhimen).

## 🛠 Technical Implementation

This project is built purely in **Python** with no external dependencies.

* **Custom Matrix Class:** Supports addition, multiplication, transposition, and exponentiation.
* **Graph Class:** Implements adjacency matrices.
* **Algorithms:**
    * Dijkstra's Algorithm (Weighted Shortest Path)
    * Breadth-First Search (BFS)
    * Depth-First Search (DFS)
    * Prim's Algorithm (MST)
    * Connected Components Analysis

## ⚡ Getting Started

### Prerequisites
* Python 3.x installed on your machine.

### Installation
1.  Clone the repository or download the source code.
2.  Ensure `subway_navigation.py` and the `data/` directory are in your working directory.
3.  The `data/` folder contains JSON files with all subway line information.

### Usage
Run the script directly in your terminal:

```bash
python subway_navigation.py
```

Follow the interactive menu prompts:

```text
==================================================
   Beijing Subway Graph Navigation System
==================================================
1. [Dijkstra] Fastest Route (Time Weighted)
2. [BFS] Least Stops Route
3. [DFS] Random Exploration Path
4. [Prim] Calculate MST Cost (Total Network Length)
5. [Degree] Station Hub Analysis
...

```

## 🚀 Example

**Finding the fastest route from "西直门" (Xizhimen) to "国贸" (Guomao):**

```text
Enter option number: 1
Enter start station: 西直门
Enter end station: 国贸

Calculating fastest route...
Estimated Time: 28 minutes
Route: 西直门 -> 车公庄 -> 平安里 -> 南锣鼓巷 -> 东四 -> 朝阳门 -> 建国门 -> 永安里 -> 国贸
This route involves stations known for difficult transfers: 西直门, 平安里, 国贸
Please prepare for long walks or stairs.

```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
