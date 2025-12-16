from src.config import RAW_DIR, PROCESSED_DIR
from src.core.cleaner import GenericCleaner


def run_bba_sales_etl():
    print("🚀 [Service] Starting BBA Sales Data Pipeline...")

    input_file = RAW_DIR / "dirty_real_sales.csv"
    output_file = PROCESSED_DIR / "clean_bba_sales.csv"

    # 1. 实例化通用清洗器
    cleaner = GenericCleaner()

    # 2. 定义 BBA 项目特有的清洗逻辑 (组装流水线)
    (
        cleaner.load_file(input_file)
        # 步骤 A: 把 "Product Line" 这种列名洗成 "product_line"
        .normalize_headers()
        # 步骤 B: 处理地区和人名的格式 (North, John Doe)
        .clean_text_columns(
            columns=["region", "salesperson", "county"], case_type="title"
        )
        # 步骤 C: 处理金额 "$100" -> 100.0
        .extract_numbers(columns=["sales", "calls"])
        # 步骤 D: 填充 sales 的空值为平均值，但删除 calls 为空的行
        .handle_missing_values(columns=["sales"], strategy="mean")
        .handle_missing_values(columns=["calls"], strategy="drop")
        # 步骤 E: 去重并保存
        .drop_duplicates()
        .save(output_file)
    )


if __name__ == "__main__":
    run_bba_sales_etl()
