# 临时的 path hack，为了能找到 config
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import RAW_DIR


def generate_chaos():
    print("😈 [Script] Generating Dirty Data...")

    # 1. 基础数据
    data = {
        "Region": ["NORTH", " North ", "south", "West", "East"],
        "Salesperson": ["John", "MIKE", "sara", "Tom", "Amy"],
        "Sales": ["$1,000", "200", "$3,500.50", "N/A", "500 (Pending)"],
        "Calls": [10, np.nan, 30, 40, 50],
        "Date": ["2024-01-01", "2024/01/02", "Invalid", "2024-01-04", "2024-01-05"],
    }

    df = pd.DataFrame(data)

    # 2. 制造重复
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    # 3. 保存
    file_path = RAW_DIR / "dirty_real_sales.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ Generated: {file_path}")
    print(df)


if __name__ == "__main__":
    generate_chaos()
