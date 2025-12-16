from pathlib import Path
from typing import List, Union, Any

import pandas as pd


class GenericCleaner:
    """
    通用数据清洗工具箱。
    不包含任何具体业务逻辑，只提供原子化的清洗功能。
    """

    def __init__(self, df: pd.DataFrame = None):
        # 支持传入 df，或者初始化为空后续 load
        self.df = df

    def load_file(
        self, file_path: Union[str, Path], encoding: str = "utf-8"
    ) -> "GenericCleaner":
        """加载 CSV 或 Excel"""
        path = Path(file_path)
        print(f"🔧 [Core] Loading: {path.name}")

        if path.suffix == ".csv":
            try:
                self.df = pd.read_csv(path, encoding=encoding)
            except UnicodeDecodeError:
                self.df = pd.read_csv(path, encoding="ISO-8859-1")
        elif path.suffix in [".xlsx", ".xls"]:
            self.df = pd.read_excel(path)
        else:
            raise ValueError("Unsupported file format")
        return self

    def normalize_headers(self) -> "GenericCleaner":
        """列名标准化：转小写，空格变下划线 (Product Name -> product_name)"""
        self.df.columns = (
            self.df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
        )
        return self

    def handle_missing_values(
        self, columns: List[str], strategy: str = "drop", fill_value: Any = 0
    ) -> "GenericCleaner":
        """
        处理缺失值 (NaN)。
        strategy: 'drop' (删除行), 'fill' (填充指定值), 'mean' (填充平均值)
        """
        for col in columns:
            if col not in self.df.columns:
                continue

            if strategy == "drop":
                self.df = self.df.dropna(subset=[col])
            elif strategy == "fill":
                self.df[col] = self.df[col].fillna(fill_value)
            elif strategy == "mean":
                mean_val = pd.to_numeric(self.df[col], errors="coerce").mean()
                self.df[col] = self.df[col].fillna(mean_val)
        return self

    def clean_text_columns(
        self, columns: List[str], case_type: str = "title"
    ) -> "GenericCleaner":
        """
        清洗文本列：去空格 + 大小写转换。
        case_type: 'lower', 'upper', 'title'
        """
        for col in columns:
            if col not in self.df.columns:
                continue

            s = self.df[col].astype(str).str.strip()
            if case_type == "lower":
                self.df[col] = s.str.lower()
            elif case_type == "upper":
                self.df[col] = s.str.upper()
            elif case_type == "title":
                self.df[col] = s.str.title()
        return self

    def extract_numbers(self, columns: List[str]) -> "GenericCleaner":
        """
        从脏字符串中提取数字 (例如 "$1,200.50 (Est)" -> 1200.50)。
        """
        for col in columns:
            if col not in self.df.columns:
                continue

            # 1. 转字符串，去逗号
            s = self.df[col].astype(str).str.replace(",", "", regex=False)
            # 2. 正则提取
            extracted = s.str.extract(r"(\d+\.?\d*)", expand=False)
            # 3. 转数字
            self.df[col] = pd.to_numeric(extracted, errors="coerce")
        return self

    def convert_dates(self, columns: List[str]) -> "GenericCleaner":
        """将列转换为标准日期格式"""
        for col in columns:
            if col not in self.df.columns:
                continue
            self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
        return self

    def drop_duplicates(self) -> "GenericCleaner":
        """去重"""
        self.df = self.df.drop_duplicates()
        return self

    def get_data(self) -> pd.DataFrame:
        """返回处理好的 DataFrame"""
        return self.df

    def save(self, output_path: Union[str, Path]):
        """保存文件"""
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(p, index=False)
        print(f"✅ [Core] Saved to: {p}")
