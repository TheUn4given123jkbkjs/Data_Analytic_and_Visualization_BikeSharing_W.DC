"""
Người viết: TV5 (bản tối thiểu để chạy độc lập; nếu nhóm đã có common.py chung thì dùng bản của nhóm)
Mục đích : hằng số và hàm đọc dữ liệu dùng chung cho các file 0x_*.py
Đầu vào  : hour.csv (đặt cùng thư mục)
Đầu ra   : SEED, load_data()
"""
from pathlib import Path

import pandas as pd

SEED = 42
DATA_PATH = Path(__file__).parent / "hour.csv"


def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["dteday"])
    df["datetime"] = df["dteday"] + pd.to_timedelta(df["hr"], unit="h")
    return df
