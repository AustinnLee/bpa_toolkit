from pathlib import Path

import duckdb
import pandas as pd


def run_analysis():
    print("\n--- [Analyst] Starting SQL Analysis ---")

    # 1. 自动定位数据文件
    project_root = Path(__file__).resolve().parent.parent
    data_path = project_root / "data" / "processed" / "clean_real_sales.csv"

    # 2. 读取 Pandas DataFrame
    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} rows of clean data.")

    # 3. DuckDB SQL 查询
    # 业务问题：每个大区 (Region) 下，哪个县 (County) 的销售额最高？
    query = """
            SELECT
                region,
                county,
                SUM(sales) as total_revenue,
                -- 计算该县在整个大区里的销售占比
                ROUND(SUM(sales) / SUM(SUM(sales)) OVER (PARTITION BY region), 4) as region_share,
                -- 大区内排名
                RANK() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) as rank_in_region
            FROM df
            GROUP BY region, county
            ORDER BY region, total_revenue DESC \
            """

    # 4. 执行并转回 DataFrame
    result = duckdb.sql(query).df()

    print("\n>>> Analysis Result:")
    pd.set_option("display.max_columns", None)
    print(result)


if __name__ == "__main__":
    run_analysis()
