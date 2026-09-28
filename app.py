# app.py

import os
from src.feature_engineering import generate_sample_data, create_time_series_features
from src.inventory_optimizer import InventoryOptimizer
from pyecharts.charts import Line
from pyecharts import options as opts

def main():
    print("=== 智能供应链库存优化与需求预测系统启动 ===")
    
    # 1. 加载模拟数据并进行特征工程
    raw_df = generate_sample_data()
    df = create_time_series_features(raw_df)
    print(f"数据预处理完成，有效样本量: {len(df)}")
    
    # 2. 实例化面向对象的库存优化器
    optimizer = InventoryOptimizer(service_level_z=1.65) # 95% 服务水平
    
    # 以北仓库 (WH_North) 的 SKU_001 为例计算安全库存与再订货点
    sample_sku_df = df[(df['warehouse_id'] == 'WH_North') & (df['sku_id'] == 'SKU_001')]
    
    demand_std = sample_sku_df['sales'].std()       # 销量标准差
    avg_daily_demand = sample_sku_df['sales'].mean()# 平均日需求
    lead_time = 5                                   # 假设供应商提前期为 5 天
    
    safety_stock = optimizer.calculate_safety_stock(demand_std, lead_time)
    reorder_point = optimizer.calculate_reorder_point(avg_daily_demand, lead_time, safety_stock)
    
    print(f"\n--- 【WH_North - SKU_001 库存决策报告】 ---")
    print(f"平均日需求量: {avg_daily_demand:.2f}")
    print(f"需求标准差: {demand_std:.2f}")
    print(f"计算安全库存 (SS): {safety_stock}")
    print(f"计算再订货点 (ROP): {reorder_point}")
    
    # 3. 使用 pyECharts 生成销量趋势可视化图表
    os.makedirs("docs", exist_ok=True)
    
    dates = sample_sku_df['date'].dt.strftime('%Y-%m-%d').tolist()
    sales_values = sample_sku_df['sales'].tolist()
    rolling_values = sample_sku_df['rolling_mean_7'].round(2).tolist()
    
    line = (
        Line()
        .add_xaxis(dates)
        .add_yaxis("实际销量", sales_values, is_smooth=True, line_style_opts=opts.LineStyleOpts(width=2))
        .add_yaxis("7天滚动均值", rolling_values, is_smooth=True, line_style_opts=opts.LineStyleOpts(width=2, color="orange"))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="供应链 SKU 销量与趋势监测大屏", subtitle="WH_North - SKU_001"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            xaxis_opts=opts.AxisOpts(name="日期", boundary_scale=False),
            yaxis_opts=opts.AxisOpts(name="销量"),
        )
    )
    
    # 将图表输出为 HTML 文件保存在 docs 目录中
    output_html = "docs/demand_forecast_dashboard.html"
    line.render(output_html)
    print(f"\n可视化大屏已成功生成并保存至: {output_html}")
    print("=== 系统运行圆满结束 ===")

if __name__ == "__main__":
    main()