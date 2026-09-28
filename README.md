# SupplyChain-Demand-Forecast-Engine (智能供应链库存优化与需求预测引擎)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-orange.svg)](https://pandas.pydata.org/)
[![pyECharts](https://img.shields.io/badge/pyECharts-Visualization-green.svg)](https://pyecharts.org/)

## 📌 项目背景
在现代供应链管理中，“断货引发的销售损失”与“库存积压导致的资金占用”是企业面临的核心痛点。本项目基于 Python 开发了一套轻量级的**智能供应链库存优化与需求预测系统**，旨在通过时间序列特征工程与面向对象（OOP）算法模型，帮助企业实现精细化的库存补货与安全库存科学计算。

---

## 🚀 核心功能模块
1. **时间序列特征工程 (`src/feature_engineering.py`)**：
   * 基于 `Pandas` 对多仓库、多 SKU 的历史销量数据进行清洗。
   * 自动构建滞后特征（Lag Features, 如 `lag_1`, `lag_7`）及移动平均滚动特征（Rolling Mean）。
2. **面向对象库存策略引擎 (`src/inventory_optimizer.py`)**：
   * 采用面向对象设计模式封装安全库存（Safety Stock, SS）与再订货点（Reorder Point, ROP）计算逻辑，支持自定义服务水平系数（$Z$ 值）。
3. **动态业务可视化大屏 (`app.py`)**：
   * 整合 `pyECharts` 动态生成多维销量趋势与滚动均值对比图表，直观呈现业务运营指标。

---

## 🛠️ 项目目录结构
```text
SupplyChain-Demand-Forecast-Engine/
│
├── data/                    # 存放原始或模拟销量数据集
├── docs/                    # 存放 pyECharts 生成的交互式可视化大屏 HTML
├── src/                     # 源代码目录
│   ├── __init__.py
│   ├── feature_engineering.py # 时间序列特征提取模块
│   └── inventory_optimizer.py # 面向对象库存优化核心类
│
├── app.py                   # 主运行程序（串联全流程与可视化输出）
├── requirements.txt         # 项目依赖包
└── README.md                # 项目说明文档