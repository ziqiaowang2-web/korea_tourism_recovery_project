"""
通用旅游数据读取脚本 / 일반 관광데이터 읽기 스크립트

中文：
适用于已经整理成一个综合表的 Korea Tourism Data Lab CSV/Excel。
如果你下载的是多个分开的真实文件，如 방문자수、관광지출액、목적지검색건수，
请运行 02_load_datalab_real_files.py。

한국어:
하나의 통합된 Korea Tourism Data Lab CSV/Excel 파일을 읽는 스크립트입니다.
방문자수, 관광지출액, 목적지검색건수처럼 여러 파일로 나누어 다운로드한 경우에는
02_load_datalab_real_files.py를 실행하세요.
"""

import pandas as pd
from utils import (
    DATA_RAW, DATA_PROCESSED, read_table, normalize_column_name,
    standardize_region_name, parse_month, clean_numeric, save_csv
)

raw_dir = DATA_RAW / "datalab"

# datalab 폴더 안의 CSV/Excel 파일 목록 / datalab 文件夹中的 CSV/Excel 文件列表
files = list(raw_dir.glob("*.csv")) + list(raw_dir.glob("*.xlsx")) + list(raw_dir.glob("*.xls"))

if not files:
    raise FileNotFoundError(
        "data/raw/datalab/ 폴더에 CSV 또는 Excel 파일이 없습니다.\n"
        "data/raw/datalab/ 文件夹中没有 CSV 或 Excel 文件。\n"
        "먼저 데이터를 넣거나 python src/00_generate_sample_data.py 를 실행하세요."
    )

dfs = []

for file in files:
    print(f"[READ] {file}")
    df = read_table(file)
    df.columns = [normalize_column_name(c) for c in df.columns]
    df["source_file"] = file.name
    dfs.append(df)

tourism = pd.concat(dfs, ignore_index=True)

if "region" not in tourism.columns:
    raise ValueError("지역 컬럼을 찾지 못했습니다. / 未找到地区列。")

if "date" not in tourism.columns:
    raise ValueError("날짜 컬럼을 찾지 못했습니다. / 未找到日期列。")

tourism["region"] = tourism["region"].apply(standardize_region_name)
tourism["date"] = tourism["date"].apply(parse_month)

numeric_candidates = [
    "visitor_count", "unique_visitors", "tourism_spending",
    "destination_search", "avg_stay_time", "avg_lodging_days",
    "lodging_visitor_ratio"
]

for col in numeric_candidates:
    if col in tourism.columns:
        tourism[col] = clean_numeric(tourism[col])

# 필요한 컬럼만 유지 / 只保留需要的列
keep_cols = ["date", "region"] + [c for c in numeric_candidates if c in tourism.columns]
tourism = tourism[keep_cols].copy()

# 같은 지역-월이 중복되면 집계 / 如果同一地区-月份重复，则聚合
agg_map = {}
for col in numeric_candidates:
    if col in tourism.columns:
        if col in ["avg_stay_time", "avg_lodging_days", "lodging_visitor_ratio"]:
            agg_map[col] = "mean"
        else:
            agg_map[col] = "sum"

tourism = tourism.groupby(["date", "region"], as_index=False).agg(agg_map)
tourism = tourism.sort_values(["region", "date"]).reset_index(drop=True)

save_csv(tourism, DATA_PROCESSED / "tourism_monthly_raw_merged.csv")

print("통합 데이터 저장 완료 / 综合数据保存完成")
print(tourism.head())
