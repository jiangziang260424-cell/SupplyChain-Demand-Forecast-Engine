# src/feature_engineering.py

import pandas as pd
import numpy as np

def generate_sample_data() -> pd.DataFrame:
    """
    生成一份用于演示的供应链历史销量模拟数据
    """
    np.random.seed(42)
    date_range = pd.date_range(start="2026-01-01", periods=60, freq="D")
    
    data = []
    # 假设有两个仓库、两个 SKU
    warehouses = ["WH_North", "WH_South"]
    skus = ["SKU_001", "SKU_002"]
    
    for wh in warehouses:
        for sku in skus:
            # 基础销量 + 随机波动
            base_sales = np.random.randint(30, 80)
            sales_series = base_sales + np.random.poisson(lam=5, size=len(date_range))
            
            for date, sales in zip(date_range, sales_series):
                data.append({
                    "date": date,
                    "warehouse_id": wh,
                    "sku_id": sku,
                    "sales": int(sales)
                })
                
    df = pd.DataFrame(data)
    return df

def create_time_series_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    为历史销量数据构建时间序列特征（滞后特征与滚动均值）
    """
    df['date'] = pd.to_datetime(df['date'])
    # 按仓库和SKU分组排序
    df = df.sort_values(by=['warehouse_id', 'sku_id', 'date']).reset_index(drop=True)
    
    # 1. 滞后特征 (Lag Features)：前1天销量、前7天销量
    df['lag_1'] = df.groupby(['warehouse_id', 'sku_id'])['sales'].shift(1)
    df['lag_7'] = df.groupby(['warehouse_id', 'sku_id'])['sales'].shift(7)
    
    # 2. 滚动统计特征 (Rolling Features)：过去7天的平均销量
    df['rolling_mean_7'] = (
        df.groupby(['warehouse_id', 'sku_id'])['sales']
        .transform(lambda x: x.rolling(window=7).mean())
    )
    
    # 丢弃因计算滞后/滚动而产生的空值行
    df_cleaned = df.dropna().reset_index(drop=True)
    return df_cleaned

if __name__ == "__main__":
    print("正在生成模拟销量数据...")
    raw_df = generate_sample_data()
    print(f"原始数据行数: {len(raw_df)}")
    
    print("正在提取时间序列特征...")
    processed_df = create_time_series_features(raw_df)
    print(f"特征工程处理后的数据行数: {len(processed_df)}")
    print("特征数据预览：")
    print(processed_df.head())