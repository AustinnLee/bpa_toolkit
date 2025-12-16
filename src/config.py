from pathlib import Path

# === 路径锚点 ===
# 无论在哪个电脑，src/config.py 的上一级就是 src，再上一级就是项目根目录
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent

# === 数据目录结构 ===
DATA_DIR = PROJECT_ROOT / "data"

# 原始数据目录
RAW_DIR = DATA_DIR / "raw"

# 清洗后数据目录
PROCESSED_DIR = DATA_DIR / "processed"

# 对账专用目录 (刚才漏掉的就是这一行)
RECON_DATA_DIR = DATA_DIR / "reconciliation"

# === 确保目录存在 ===
# 自动创建所有定义的文件夹
for d in [RAW_DIR, PROCESSED_DIR, RECON_DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)
