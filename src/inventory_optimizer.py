# src/inventory_optimizer.py

class InventoryOptimizer:
    """
    供应链库存优化与补货点计算类
    """
    def __init__(self, service_level_z: float = 1.65):
        # 默认服务水平对应的 Z 值（例如 95% 服务水平对应的 z 约为 1.65）
        self.z = service_level_z

    def calculate_safety_stock(self, demand_std: float, lead_time: int) -> float:
        """
        计算安全库存 (Safety Stock)
        公式: SS = Z * 需求标准差 * sqrt(提前期)
        """
        import math
        safety_stock = self.z * demand_std * math.sqrt(lead_time)
        return round(safety_stock, 2)

    def calculate_reorder_point(self, avg_daily_demand: float, lead_time: int, safety_stock: float) -> float:
        """
        计算再订货点 (Reorder Point, ROP)
        公式: ROP = 平均日需求量 * 提前期 + 安全库存
        """
        rop = (avg_daily_demand * lead_time) + safety_stock
        return round(rop, 2)

# 简单测试代码
if __name__ == "__main__":
    optimizer = InventoryOptimizer(service_level_z=1.65)
    # 假设某 SKU 日需求标准差为 12.5，供应商提前期为 5 天，平均日需求为 50
    ss = optimizer.calculate_safety_stock(demand_std=12.5, lead_time=5)
    rop = optimizer.calculate_reorder_point(avg_daily_demand=50, lead_time=5, safety_stock=ss)
    
    print(f"计算出的安全库存为: {ss}")
    print(f"计算出的再订货点 (ROP) 为: {rop}")