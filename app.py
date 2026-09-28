import os
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
from src.feature_engineering import generate_sample_sales_data, process_sales_features
from src.inventory_optimizer import InventoryOptimizer

def main():
    print("=== 智能供应链库存优化与需求预测系统启动 ===")
    
    # 1. 生成或加载模拟销量数据
    df = generate_sample_sales_data()
    
    # 2. 执行时间序列特征工程（计算滞后特征、滚动均值等）
    df_processed = process_sales_features(df)
    print(f"数据预处理完成，有效样本量: {len(df_processed)}")
    
    # 3. 针对特定仓库与 SKU 进行库存优化决策（以 WH_North 和 SKU_001 为例）
    target_wh = "WH_North"
    target_sku = "SKU_001"
    
    sku_df = df_processed[(df_processed['warehouse_id'] == target_wh) & (df_processed['sku_id'] == target_sku)]
    
    if sku_df.empty:
        print(f"未找到仓库 {target_wh} 下的 {target_sku} 数据")
        return

    # 实例化库存优化器（设置提前期 L = 5 天，目标服务水平 95% 对应的 Z = 1.65）
    optimizer = InventoryOptimizer(lead_time_days=5, service_level_z=1.65)
    
    # 计算均值、标准差、安全库存与再订货点
    mean_demand = sku_df['sales_qty'].mean()
    std_demand = sku_df['sales_qty'].std()
    safety_stock = optimizer.calculate_safety_stock(std_demand)
    reorder_point = optimizer.calculate_reorder_point(mean_demand, safety_stock)
    
    print(f"\n--- 【{target_wh} - {target_sku} 库存决策报告】 ---")
    print(f"平均日需求量: {mean_demand:.2f}")
    print(f"需求标准差: {std_demand:.2f}")
    print(f"计算安全库存 (SS): {safety_stock:.2f}")
    print(f"计算再订货点 (ROP): {reorder_point:.2f}")
    
    # 4. 业务可视化：利用 pyECharts 生成动态销量趋势与滚动均值图表
    dates = sku_df['date'].astype(str).tolist()
    sales_values = sku_df['sales_qty'].tolist()
    rolling_values = sku_df['rolling_mean_7'].fillna(0).tolist()
    
    line = Line()
    line.add_xaxis(dates)
    # 注意这里修改为了 linestyle_opts
    line.add_yaxis("实际销量", sales_values, is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2))
    line.add_yaxis("7天滚动均值", rolling_values, is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=2, color="orange"))
    
    line.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{target_wh} - {target_sku} 需求预测与滚动均值分析",
            subtitle="Smart Supply Chain Inventory System"
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        yaxis_opts=opts.AxisOpts(name="销量 (件)")
    )
    
    # 5. 输出可视化大屏 HTML 文件
    os.makedirs("docs", exist_ok=True)
    output_path = "docs/demand_forecast_dashboard.html"
    line.render(output_path)
    print(f"\n[成功] 可视化大屏已生成，请在本地浏览器中打开: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()