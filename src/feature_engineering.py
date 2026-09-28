import pandas as pd
import numpy as np

def generate_sample_sales_data():
    """
    生成模拟的供应链多仓库、多 SKU 历史销量数据集
    """
    np.random.seed(42)
    date_range = pd.date_range(start="2026-01-01", end="2026-06-30", freq="D")
    warehouses = ["WH_North", "WH_South", "WH_East"]
    skus = ["SKU_001", "SKU_002", "SKU_003"]
    
    data = []
    for wh in warehouses:
        for sku in skus:
            # 基础销量加一些随机波动与周期性
            base_sales = np.random.randint(50, 150)
            noise = np.random.normal(0, 10, len(date_range))
            sales = base_sales + noise + 5 * np.sin(np.arange(len(date_range)) * 2 * np.pi / 7)
            sales = np.clip(sales, 10, None).astype(int)
            
            for date, qty in zip(date_range, sales):
                data.append({
                    "date": date,
                    "warehouse_id": wh,
                    "sku_id": sku,
                    "sales_qty": qty
                })
                
    df = pd.DataFrame(data)
    return df

def process_sales_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    时间序列特征工程：按仓库和SKU分组计算滞后特征与滚动均值
    """
    df = df.sort_values(by=["warehouse_id", "sku_id", "date"])
    
    # 计算 7 天滞后特征与 7 天移动平均滚动特征
    df['lag_1'] = df.groupby(['warehouse_id', 'sku_id'])['sales_qty'].shift(1)
    df['rolling_mean_7'] = (
        df.groupby(['warehouse_id', 'sku_id'])['sales_qty']
        .transform(lambda x: x.rolling(window=7, min_periods=1).mean())
    )
    
    return df