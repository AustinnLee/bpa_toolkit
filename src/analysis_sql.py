from datetime import datetime, timedelta

import duckdb
import numpy as np
import pandas as pd


def run_analysis():
    print(">>> [Consultant] Loading Business Data...")

    # 1. 模拟数据：生成 BBA 销售流水 (Mock Data)
    # 假设有 1000 条销售记录，涉及 3 个大区，10 个门店
    np.random.seed(42)
    dates = [datetime(2024, 1, 1) + timedelta(days=i) for i in range(10)]
    shops = [f"Shop_{i}" for i in range(1, 11)]
    regions = {
        "Shop_1": "North",
        "Shop_2": "North",
        "Shop_3": "North",
        "Shop_4": "East",
        "Shop_5": "East",
        "Shop_6": "East",
        "Shop_7": "South",
        "Shop_8": "South",
        "Shop_9": "South",
        "Shop_10": "South",
    }

    data = []
    for _ in range(100):  # 生成100条记录
        shop = np.random.choice(shops)
        data.append(
            {
                "date": np.random.choice(dates),
                "region": regions[shop],
                "shop_name": shop,
                "sales_amount": np.random.randint(1000, 50000),
            }
        )

    # 将列表转为 Pandas DataFrame
    # 这里的 df 只是中间载体，真正的计算交给 SQL
    df_sales = pd.DataFrame(data)

    print(f">>> [Data] Loaded {len(df_sales)} rows of raw sales data.")

    # 2. 核心：使用 DuckDB 直接查询 Pandas 变量 (df_sales)
    # DuckDB 的魔法：它可以直接把 Python 里的 df_sales 变量当作一张 SQL 表来查！

    print(">>> [Engine] Executing SQL Analysis (Window Functions)...")

    query = """
            WITH Daily_Sales AS (
                -- 第一步：先按 天+门店 汇总销售额
                SELECT
                    region,
                    shop_name,
                date,
                SUM(sales_amount) as daily_total
            FROM df_sales
            GROUP BY 1, 2, 3
                ),

                Analysis_Layer AS (
            -- 第二步：计算排名和环比 (Window Functions)
            SELECT
                *,

                -- KPI 1: 区域内排名 (按销售额降序)
                DENSE_RANK() OVER (
                PARTITION BY region, date
                ORDER BY daily_total DESC
                ) as region_rank,

                -- KPI 2: 获取“昨天”的销售额 (Lag Function)
                LAG(daily_total, 1) OVER (
                PARTITION BY shop_name
                ORDER BY date
                ) as yesterday_total
            FROM Daily_Sales
                )

            -- 第三步：输出最终报表
            SELECT
                *,
                -- KPI 3: 计算环比增长率 (Growth Rate)
                ROUND((daily_total - yesterday_total) / yesterday_total, 4) as growth_rate
            FROM Analysis_Layer
            ORDER BY region, date, region_rank \
            """

    # 执行 SQL，并将结果直接转回 Pandas DataFrame
    df_result = duckdb.sql(query).df()

    return df_result


if __name__ == "__main__":
    result = run_analysis()

    print("\n>>> [Report] Analysis Result (Top 10 rows):")
    # 打印的时候，设一下宽度，防止换行太难看
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    print(result.head(10))

    # 简单的质量检查
    print("\n>>> [QC] Data Quality Check:")
    print(f"Total Rows: {len(result)}")
    print(f"Missing Growth Rates (First Day): {result['growth_rate'].isna().sum()}")
