import random
from pathlib import Path  # <--- 引入这个神器

import numpy as np
import pandas as pd


def poison_data():
    print(">>> [Chaos Engineer] Poisoning the clean data...")

    # === 关键修复开始 ===
    # 1. 获取当前脚本 (poison_data.py) 的绝对路径
    current_file = Path(__file__).resolve()

    # 2. 推算项目根目录 (src 的上一级)
    project_root = current_file.parent.parent

    # 3. 拼接出绝对路径 (Windows/Mac 通杀)
    input_path = project_root / "data" / "raw" / "real_sales.csv"
    output_path = project_root / "data" / "raw" / "dirty_real_sales.csv"

    print(f"Target Input Path: {input_path}")
    # === 关键修复结束 ===

    # 检查文件到底在不在，不在就报错并打印路径，方便调试
    if not input_path.exists():
        raise FileNotFoundError(f"真的找不到文件！请确认文件是否存在于: {input_path}")

    df = pd.read_csv(input_path)

    # 2. 破坏动作 A: 大小写混乱 (Inconsistent Casing)
    # 把 'region' 变成 'NORTH', 'North', 'north' 混杂
    print("- Mixing casing in Region...")
    df["region"] = df["region"].apply(
        lambda x: x.upper() if random.random() > 0.5 else x.lower()
    )

    # 3. 破坏动作 B: 污染数字列 (Dirty Currency)
    # 把 'sales' (数字) 变成字符串，混入 '$', ',' 和文字
    print("- Corrupting Sales column...")

    def dirty_sales(val):
        r = random.random()
        if r < 0.1:
            return np.nan  # 10% 缺失
        if r < 0.3:
            return f"${val}"  # 20% 带美元符号
        if r < 0.4:
            return f"{val} (Est)"  # 10% 带备注
        return val  # 剩下保持原样

    df["sales"] = df["sales"].apply(dirty_sales)

    # 4. 破坏动作 C: 制造重复行 (Duplicates)
    print("- Injecting duplicates...")
    df = pd.concat([df, df.iloc[:10]], ignore_index=True)  # 把前10行复制一遍贴到最后

    # 5. 破坏动作 D: 名字里的脏字符
    # 把 'salesperson' 加上一些莫名其妙的空格
    df["salesperson"] = df["salesperson"].apply(
        lambda x: f" {x} " if random.random() > 0.5 else x
    )

    # 6. 保存为脏数据

    df.to_csv(output_path, index=False)
    print(f">>> [Success] Created nasty data at: {output_path}")
    print(df.head(10))


if __name__ == "__main__":
    poison_data()
