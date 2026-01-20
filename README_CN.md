# 🚇 北京地铁图导航系统

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/coverage-99.55%25-success)
![Status](https://img.shields.io/badge/status-active-success)

> **基于纯Python实现的终端版北京地铁导航系统，使用自定义Matrix和Graph实现。**

## 📖 项目概述

将北京地铁网络模拟为加权无向图，不使用numpy或networkx等外部依赖。从零实现核心图论算法，包括Dijkstra、BFS、DFS、Prim最小生成树和CPX（矩阵幂）寻路算法。

**网络规模：** 26条地铁线路，约475个站点，约950个区间

### 数据来源
通行时间来源于 [北京地铁区间用时地图 250124版本](https://search.bilibili.com/all?keyword=北京地铁区间用时地图%20250124版本)

## ✨ 特性

| 功能 | 算法 | 描述 |
|---------|-----------|-------------|
| ⏱️ 最快路线 | Dijkstra | 最短通行时间（时间加权）|
| 🛑 最少站点 | BFS | 经过站点最少 |
| 🧪 随机路径 | DFS | 任意可行路径（探索）|
| 🔬 CPX 检查 | 矩阵幂 | 代数连通性路径检查（实验性）|
| 🌐 网络成本 | Prim最小生成树 | 连接所有站点的最小总长度 |
| 🔍 枢纽分析 | 度中心性 | 识别换乘枢纽和普通站点 |
| 📊 连通性 | BFS/DFS | 检查网络连通性和分量 |
| 🚧 模拟中断 | 边删除 | 模拟轨道故障 |
| ⚠️ 地狱站点 | 自定义集合 | 警告困难换乘 |

### 🌍 国际化支持

通过 GNU gettext 支持英文和中文：
```bash
LANGUAGE=zh python subway_navigation.py  # 中文
LANGUAGE=en python subway_navigation.py  # 英文
```

添加新语言参见 [I18N_USAGE.md](./I18N_USAGE.md)。

## ⚠️ 局限性

**历史限制（已解决）：** 早期版本将换乘视为零成本，可能推荐在复杂枢纽（西直门、东直门）换乘，尽管需要步行8分钟以上。地狱站点警告是唯一的缓解措施。

**当前实现：** `interchange_stations.json` 中的换乘时间已集成到路线计算中。Dijkstra算法通过线路状态跟踪在切换线路时应用换乘惩罚，提供更准确的通行时间估计。完全支持非对称换乘时间（例如：复兴门：2号线→1号线=0.42分钟 vs 1号线→2号线=2.5分钟）。

## 🛠 技术栈

**核心：** Python 3.12+ （无运行时依赖）

**开发工具：**
- `pytest` — 测试框架
- `pytest-cov` — 覆盖率报告（99.55%）
- `pytest-xdist` — 并行测试执行
- `pytest-benchmark` — 性能基准测试
- `ruff` — 代码检查和格式化
- `uv` — 包管理器

**自定义实现：**
- `Matrix` 类 — 线性代数运算
- `Graph` 类 — 邻接矩阵 + 15+ 算法

## ⚡ 快速开始

### 前置要求
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) （推荐）

### 安装

```bash
# 克隆仓库
git clone <repo-url>
cd Beijing-Subway-Navigator

# 使用 uv 安装开发依赖
uv sync
```

### 运行

```bash
# 直接执行
python subway_navigation.py

# 使用 uv
uv run python subway_navigation.py

# 选择语言
LANGUAGE=zh uv run python subway_navigation.py
```

### 交互式菜单

```
==================================================
   北京地铁图导航系统
==================================================
1. [Dijkstra] 最快路线（时间加权）
2. [BFS] 最少站点路线
3. [DFS] 随机探索路径
4. [Prim] 计算MST成本（网络总长度）
5. [Degree] 站点枢纽分析
6. [Matrix] 代数连通性路径（CPX实验）
7. [Components] 检查网络连通性
8. [Simulation] 模拟线路中断（删除边）
0. 退出
==================================================
```

## 🧪 测试

**覆盖率：** 99.55% （220/221条语句）— 强制最低要求：80%

```bash
# 运行所有测试
uv run pytest

# 详细输出
uv run pytest -v

# 指定测试文件
uv run pytest tests/test_graph_algorithms.py

# 生成覆盖率报告
uv run pytest --cov=graph --cov-report=term-missing

# 并行执行（更快）
uv run pytest -n auto

# 生成HTML覆盖率报告
uv run pytest --cov=graph --cov-report=html
# 在浏览器中打开 htmlcov/index.html
```

参见 [tests/README.md](./tests/README.md) 获取详细测试文档。

## ⚡ 性能基准测试

使用 pytest-benchmark 对所有寻路算法进行全面的性能基准测试。

### 基准测试覆盖范围

**43个基准测试**涵盖所有寻路算法：
- **test_pathfinding.py**：32个合成图基准测试（tiny、small、medium、dense、sparse、复杂加权）
- **test_real_subway.py**：15个真实北京地铁数据基准测试（约389个站点，约463个区间）

### 基准测试算法

| 算法 | 用途 | 测试数量 |
|------------|---------|--------|
| BFS | 最少站点（无权重）| 6 |
| DFS | 任意路径（探索）| 5 |
| Dijkstra | 最短通行时间（加权）| 6 |
| CPX | 矩阵幂方法（实验性）| 4 |
| Dijkstra with transfers | 带线路切换惩罚的最快路线 | 3 |
| A* with transfers | 启发式引导的最快路线 | 5 |
| 算法正确性 | 验证算法之间的最优性 | 4 |

### 运行基准测试

```bash
# 运行所有基准测试
uv run pytest tests/benchmarks/ -v

# 只运行基准测试（跳过非基准测试）
uv run pytest tests/benchmarks/ --benchmark-only

# 运行特定基准测试文件
uv run pytest tests/benchmarks/test_pathfinding.py -v
uv run pytest tests/benchmarks/test_real_subway.py -v

# 生成性能摘要表
uv run pytest tests/benchmarks/ --benchmark-only

# 保存基准测试结果用于比较
uv run pytest tests/benchmarks/ --benchmark-save=benchmark_results.json

# 与之前的结果比较
uv run pytest tests/benchmarks/--benchmark-compare=benchmark_results.json

# 增加轮数以提高准确性
uv run pytest tests/benchmarks/ --benchmark-min-rounds=10

# 启用预热用于JIT编译
uv run pytest tests/benchmarks/ --benchmark-warmup
```

### 基准测试场景

**合成图（test_pathfinding.py）**
- 超小图（3个顶点）：基础功能测试
- 小型图（5个顶点）：简单路径验证
- 中型图（10个顶点）：分支结构测试
- 稠密图（15个顶点）：高度连通网络压力测试
- 稀疏图（20个顶点）：线性结构测试
- 复杂加权图：算法比较测试

**真实地铁数据（test_real_subway.py）**
- 短途同线路：苹果园 → 八角游乐园（基准性能）
- 中途1次换乘：西直门 → 复兴门（换乘处理）
- 长途跨城：西直门 → 国贸（真实查询）
- 枢纽到枢纽：天安门东 → 北京站（主要站点路由）
- 复杂多次换乘：苹果园 → 大兴机场（最坏情况场景）

参见 [tests/benchmarks/README.md](./tests/benchmarks/README.md) 获取详细的基准测试文档。

## 📁 项目结构

```
Beijing-Subway-Navigator/
├── subway_navigation.py    # 主入口和CLI（343行）
├── graph.py                # Graph类和算法（248行）
├── matrix.py               # Matrix类（107行）
├── pyproject.toml          # 项目配置
├── babel.cfg               # i18n提取配置
├── data/                   # 地铁网络数据
│   ├── subway_lines.json           # 26条线路和区间
│   └── interchange_stations.json   # 换乘时间数据（集成到路由中）
├── locale/                 # 翻译（en/zh）
│   └── messages.pot
└── tests/                  # 测试套件（99.55%覆盖率）
    ├── test_graph_basic.py
    ├── test_graph_algorithms.py
    ├── test_graph_properties.py
    └── benchmarks/              # 性能基准测试（43个测试）
        ├── test_pathfinding.py   # 合成图基准测试
        ├── test_real_subway.py   # 真实地铁路数据基准测试
        └── README.md           # 基准测试文档
```

## 🚀 示例用法

**从西直门到国贸查找最快路线：**

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

## 📊 数据格式

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

修改 `data/subway_lines.json` 以更新网络数据。

## 🤝 贡献指南

欢迎贡献！请：
1. 运行测试：`uv run pytest`
2. 确保覆盖率保持在 80% 以上
3. 遵循代码风格：`uv run ruff format .`

## 📄 许可证

MIT
