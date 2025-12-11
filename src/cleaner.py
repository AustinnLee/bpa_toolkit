from pathlib import Path

import pandas as pd


class DataCleaner:
    def __init__(self, input_path: str):
        self.input_path = input_path
        self.df = None

    def load_csv(self):
        print(f"--- [Cleaner] Loading: {self.input_path} ---")
        self.df = pd.read_csv(self.input_path)
        print(f"Initial rows: {len(self.df)}")
        return self

    def normalize_text(self, cols: list):
        """修复大小写混乱 (e.g. 'NoRtH' -> 'North')"""
        print(f"Normalizing text for: {cols}")
        for col in cols:
            # str.title() 会把 "NORTH" 变成 "North"
            self.df[col] = self.df[col].astype(str).str.strip().str.title()
        return self

    def clean_sales(self):
        """修复脏金额 (e.g. '$45 (Est)' -> 45.0)"""
        print("Cleaning 'sales' column using Regex...")
        # 1. 强制转字符串
        s = self.df["sales"].astype(str)
        # 2. 提取数字 (匹配整数或小数)
        extracted = s.str.extract(r"(\d+\.?\d*)", expand=False)
        # 3. 转为 float
        self.df["sales"] = pd.to_numeric(extracted, errors="coerce")
        # 4. 填充空值 (用平均值填)
        mean_val = self.df["sales"].mean()
        self.df["sales"] = self.df["sales"].fillna(mean_val)
        return self

    def remove_duplicates(self):
        """删除重复行"""
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)
        print(f"Removed {before - after} duplicate rows.")
        return self

    def save(self, output_path: str):
        # 确保输出目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        self.df.to_csv(output_path, index=False)
        print(f"--- [Success] Clean data saved to: {output_path} ---")
        # 打印前5行看看效果
        print(self.df.head())
        return self.df


if __name__ == "__main__":
    # 使用绝对路径，防止找不到文件
    project_root = Path(__file__).resolve().parent.parent

    input_file = project_root / "data" / "raw" / "dirty_real_sales.csv"
    output_file = project_root / "data" / "processed" / "clean_real_sales.csv"

    cleaner = DataCleaner(str(input_file))

    (
        cleaner.load_csv()
        .normalize_text(cols=["region", "salesperson", "county"])  # 清洗这些文本列
        .clean_sales()  # 清洗金额列
        .remove_duplicates()  # 去重
        .save(str(output_file))
    )
