import math

class InventoryOptimizer:
    """
    面向对象供应链库存优化器：用于计算安全库存与再订货点
    """
    def __init__(self, lead_time_days: int = 5, service_level_z: float = 1.65):
        self.lead_time_days = lead_time_days
        self.service_level_z = service_level_z
        
    def calculate_safety_stock(self, std_demand: float) -> float:
        """
        计算安全库存 (Safety Stock, SS)
        公式: SS = Z * sqrt(L) * sigma
        """
        safety_stock = self.service_level_z * math.sqrt(self.lead_time_days) * std_demand
        return safety_stock
        
    def calculate_reorder_point(self, mean_demand: float, safety_stock: float) -> float:
        """
        计算再订货点 (Reorder Point, ROP)
        公式: ROP = 平均日需求量 * 提前期 + 安全库存
        """
        reorder_point = (mean_demand * self.lead_time_days) + safety_stock
        return reorder_point