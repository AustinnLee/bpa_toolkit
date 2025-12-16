import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Path fix
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import RAW_DIR


def generate_inventory():
    print("🏭 Generating Inventory Data...")

    models = ["C-Class", "E-Class", "S-Class", "GLC", "GLE", "EQE"]
    colors = ["Black", "White", "Silver", "Blue"]

    data = []
    today = datetime.now()

    for i in range(200):  # 生成200台车
        model = random.choice(models)
        # 模拟入库时间：有的刚来，有的来了很久(滞销)
        days_in_stock = random.randint(1, 150)
        entry_date = today - timedelta(days=days_in_stock)

        cost = random.randint(30000, 80000)

        data.append(
            {
                "VIN": f"WDB{random.randint(10000, 99999)}",  # 车架号
                "Model": model,
                "Color": random.choice(colors),
                "Cost_Price": cost,
                "Entry_Date": entry_date.strftime("%Y-%m-%d"),
                "Days_In_Stock": days_in_stock,
                "Status": "In Stock",  # 默认在库
            }
        )

    df = pd.DataFrame(data)

    # 保存
    save_path = RAW_DIR / "inventory_mock.csv"
    df.to_csv(save_path, index=False)
    print(f"✅ Inventory data saved to {save_path}")


if __name__ == "__main__":
    generate_inventory()
