"""
真实数据清洗与指标构建脚本
실제 데이터 정제 및 지표 생성 스크립트

中文：
用于处理 02_load_datalab_real_files.py 生成的真实年度地区数据。
它会构建旅游复苏/活跃度指标、消费集中度、增长率等指标。

한국어:
02_load_datalab_real_files.py가 생성한 실제 연도-지역 데이터를 처리합니다.
관광 회복/활성 지수, 소비 집중도, 증가율 등의 지표를 생성합니다.

修正说明 / 수정 내용:
pandas 3.x 版本中 pd.to_numeric(errors="ignore") 已不可用，
因此改为只对需要的数值列执行 errors="coerce"。
pandas 3.x에서는 pd.to_numeric(errors="ignore")가 더 이상 지원되지 않으므로,
필요한 숫자 컬럼에 대해서만 errors="coerce"를 적용하도록 수정했습니다.
"""

import pandas as pd
import numpy as np
from utils import DATA_PROCESSED, minmax, save_csv

input_path = DATA_PROCESSED / "tourism_recovery_dataset.csv"

if not input_path.exists():
    raise FileNotFoundError(
        "먼저 python src/02_load_datalab_real_files.py 를 실행하세요.\n"
        "请先运行 python src/02_load_datalab_real_files.py"
    )

df = pd.read_csv(input_path, encoding="utf-8-sig")

# 연도가 없으면 날짜에서 생성 / 如果没有 year，则从 date 生成
if "year" not in df.columns:
    if "date" in df.columns:
        df["year"] = pd.to_datetime(df["date"], errors="coerce").dt.year
    else:
        raise ValueError("year/date 컬럼이 없습니다. / 缺少 year/date 列。")

# 숫자형으로 변환할 후보 컬럼 / 需要转换为数值型的候选列
numeric_cols = [
    "visitor_count",
    "visitor_count_prev",
    "visitor_growth_rate",
    "tourism_spending",
    "tourism_spending_prev",
    "tourism_spending_prev_year",
    "tourism_spending_recovery_rate",
    "tourism_spending_growth_rate",
    "destination_search",
    "avg_stay_time",
    "avg_lodging_days",
    "lodging_visitor_ratio",
    "population",
    "grdp",
    "accommodation_business_count",
    "restaurant_business_count",
]

# 실제 존재하는 숫자 후보만 사용 / 只处理实际存在的数值候选列
numeric_cols = [c for c in numeric_cols if c in df.columns]

# 숫자 컬럼 정리 / 数值列处理
for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[df[col] < 0, col] = np.nan

    # 전체가 결측이면 0으로 채우고, 아니면 중앙값으로 보정
    # 如果整列都是缺失，则填 0；否则用中位数补充
    if df[col].isna().all():
        df[col] = 0
    else:
        df[col] = df[col].fillna(df[col].median())

# 전년도 관광지출액이 있으면 증가율 계산 / 如果有去年旅游支出额，则计算增长率
if "tourism_spending" in df.columns and "tourism_spending_prev_year" in df.columns:
    df["tourism_spending_recovery_rate"] = (
        df["tourism_spending"] / df["tourism_spending_prev_year"].replace(0, np.nan)
    )
    df["tourism_spending_growth_rate"] = (
        (df["tourism_spending"] - df["tourism_spending_prev_year"])
        / df["tourism_spending_prev_year"].replace(0, np.nan)
    )

# 관광 회복/활성 지수 구성 요소
# 旅游复苏/活跃度指数构成要素
index_components = []

if "visitor_count" in df.columns:
    df["visitor_score"] = minmax(df["visitor_count"])
    index_components.append(("visitor_score", 0.30))

if "tourism_spending" in df.columns:
    df["spending_score"] = minmax(df["tourism_spending"])
    index_components.append(("spending_score", 0.30))

if "destination_search" in df.columns:
    df["search_score"] = minmax(df["destination_search"])
    index_components.append(("search_score", 0.20))

if "avg_stay_time" in df.columns:
    df["stay_time_score"] = minmax(df["avg_stay_time"])
    index_components.append(("stay_time_score", 0.10))

if "avg_lodging_days" in df.columns:
    df["lodging_score"] = minmax(df["avg_lodging_days"])
    index_components.append(("lodging_score", 0.10))

if not index_components:
    raise ValueError(
        "관광 회복/활성 지수를 계산할 수 있는 컬럼이 없습니다.\n"
        "没有可用于计算旅游复苏/活跃度指数的列。"
    )

# 관광 회복지수라는 이름은 유지하되, 단일연도에서는 관광 활성도에 가까움
# 保持 tourism_recovery_index 名称；若只有单一年份，它更接近旅游活跃度指数
weight_sum = sum(w for _, w in index_components)
df["tourism_recovery_index"] = 0.0

for col, weight in index_components:
    df["tourism_recovery_index"] += df[col] * (weight / weight_sum)

# 관광소비 집중도 / 旅游消费集中度
if "tourism_spending" in df.columns:
    df["tourism_consumption_share"] = df.groupby("year")["tourism_spending"].transform(
        lambda s: s / s.sum() if s.sum() != 0 else 0
    )

# 방문자 대비 소비액 / 游客人均旅游支出
if "visitor_count" in df.columns and "tourism_spending" in df.columns:
    df["spending_per_visitor"] = df["tourism_spending"] / df["visitor_count"].replace(0, np.nan)

# 검색 대비 방문 전환 지표 / 搜索转化为访问的粗略指标
if "destination_search" in df.columns and "visitor_count" in df.columns:
    df["visitor_per_search"] = df["visitor_count"] / df["destination_search"].replace(0, np.nan)

# 무한대 및 결측값 보정 / 修正无穷大和缺失值
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        if df[col].isna().all():
            df[col] = 0
        else:
            df[col] = df[col].fillna(df[col].median())

save_csv(df, DATA_PROCESSED / "tourism_recovery_dataset.csv")
save_csv(
    df.sort_values(["year", "tourism_recovery_index"], ascending=[True, False]),
    DATA_PROCESSED / "tourism_recovery_index_by_region.csv"
)

print("실제 데이터 정제 및 지표 생성 완료 / 真实数据清洗与指标生成完成")
print(df.head())
