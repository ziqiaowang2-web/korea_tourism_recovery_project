"""
数据清洗与指标构建脚本 / 데이터 정제 및 지표 생성 스크립트

中文：
适用于通用月度数据 tourism_monthly_raw_merged.csv。
如果你使用真实分文件数据，请运行 03_clean_merge_data_v2.py。

한국어:
일반 월별 데이터 tourism_monthly_raw_merged.csv를 정제하는 스크립트입니다.
실제 분리 파일 데이터를 사용한다면 03_clean_merge_data_v2.py를 실행하세요.
"""

import pandas as pd
import numpy as np
from utils import DATA_PROCESSED, DATA_RAW, read_table, normalize_column_name, standardize_region_name, minmax, save_csv

input_path = DATA_PROCESSED / "tourism_monthly_raw_merged.csv"

if not input_path.exists():
    raise FileNotFoundError("먼저 python src/02_load_datalab_files.py 를 실행하세요. / 请先运行 02_load_datalab_files.py")

df = pd.read_csv(input_path, encoding="utf-8-sig", parse_dates=["date"])

# 기본 데이터 품질 처리 / 基础数据质量处理
df = df.dropna(subset=["date", "region"]).copy()
df["region"] = df["region"].apply(standardize_region_name)

numeric_cols = [
    "visitor_count", "unique_visitors", "tourism_spending",
    "destination_search", "avg_stay_time", "avg_lodging_days",
    "lodging_visitor_ratio"
]
numeric_cols = [c for c in numeric_cols if c in df.columns]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[df[col] < 0, col] = np.nan
    df[col] = df.groupby("region")[col].transform(lambda s: s.fillna(s.median()))
    df[col] = df[col].fillna(df[col].median())

# 연도/월 변수 생성 / 生成年份和月份变量
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["quarter"] = df["date"].dt.quarter

# 연도-지역 단위로 집계 / 聚合为 年份-地区 单位
annual = df.groupby(["region", "year"], as_index=False).agg({
    c: "mean" for c in numeric_cols
})

# 2020~2021년을 기준값으로 사용 / 使用 2020~2021 作为基准期
baseline_years = [2020, 2021]
baseline = annual[annual["year"].isin(baseline_years)].groupby("region", as_index=False).agg({
    c: "mean" for c in numeric_cols
})
baseline = baseline.rename(columns={c: f"{c}_baseline" for c in numeric_cols})
annual = annual.merge(baseline, on="region", how="left")

for col in numeric_cols:
    base_col = f"{col}_baseline"
    rec_col = f"{col}_recovery_rate"
    annual[rec_col] = annual[col] / annual[base_col].replace(0, np.nan)
    annual[rec_col] = annual[rec_col].replace([np.inf, -np.inf], np.nan)
    annual[rec_col] = annual[rec_col].fillna(annual[rec_col].median())

# 관광 회복지수 가중치 / 旅游复苏指数权重
weights = {
    "visitor_count_recovery_rate": 0.30,
    "tourism_spending_recovery_rate": 0.30,
    "lodging_visitor_ratio_recovery_rate": 0.15,
    "avg_stay_time_recovery_rate": 0.15,
    "destination_search_recovery_rate": 0.10,
}

available_weights = {k: v for k, v in weights.items() if k in annual.columns}
weight_sum = sum(available_weights.values())

annual["tourism_recovery_index"] = 0.0

for col, weight in available_weights.items():
    annual["tourism_recovery_index"] += minmax(annual[col]) * (weight / weight_sum)

annual["tourism_consumption_share"] = annual.groupby("year")["tourism_spending"].transform(lambda s: s / s.sum())

save_csv(df, DATA_PROCESSED / "tourism_monthly_clean.csv")
save_csv(annual, DATA_PROCESSED / "tourism_recovery_dataset.csv")
save_csv(annual.sort_values(["year", "tourism_recovery_index"], ascending=[True, False]), DATA_PROCESSED / "tourism_recovery_index_by_region.csv")

print("데이터 정제 완료 / 数据清洗完成")
print(annual.head())
