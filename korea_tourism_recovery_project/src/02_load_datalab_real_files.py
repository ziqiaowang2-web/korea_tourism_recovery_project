"""
真实 Korea Tourism Data Lab 分文件读取脚本
실제 Korea Tourism Data Lab 분리 파일 읽기 스크립트

中文：
适用于从 Korea Tourism Data Lab 下载的多个真实 CSV 文件，例如：
- 방문자수.csv
- 관광지출액.csv
- 목적지검색건수.csv
- 방문자 체류특성.csv
- 지역 방문자수_관광지출액 추세.csv
- 표_관광지검색순위.csv
- 표_방문자수최다지역.csv

한국어:
Korea Tourism Data Lab에서 실제로 다운로드한 여러 CSV 파일을 읽는 스크립트입니다.
방문자수, 관광지출액, 목적지검색건수, 방문자 체류특성 등 분리된 파일을 자동으로 병합합니다.
"""

from collections import defaultdict
from pathlib import Path
import pandas as pd
import numpy as np

from utils import (
    DATA_RAW, DATA_PROCESSED, TABLES, read_table, normalize_column_name,
    standardize_region_name, parse_month, clean_numeric, save_csv
)

raw_dir = DATA_RAW / "datalab"
files = list(raw_dir.glob("*.csv")) + list(raw_dir.glob("*.xlsx")) + list(raw_dir.glob("*.xls"))

if not files:
    raise FileNotFoundError(
        "data/raw/datalab/ 폴더에 관광데이터랩 파일이 없습니다.\n"
        "data/raw/datalab/ 文件夹中没有旅游数据实验室文件。"
    )

# 다운로드 시각 prefix별로 파일을 묶습니다.
# 按下载时间前缀分组文件，例如 20260528234642_방문자수.csv
groups = defaultdict(list)
for file in files:
    prefix = file.stem.split("_")[0]
    groups[prefix].append(file)

annual_region_frames = []
monthly_trend_frames = []
attraction_rank_frames = []
visitor_top_frames = []
age_frames = []

def infer_year_from_group(group_files):
    """
    해당 파일 묶음의 기준 연도를 추정합니다.
    从同一批下载文件中推断数据年份。

    우선 '지역 방문자수_관광지출액 추세' 파일의 기준연월을 사용합니다.
    优先使用“地区访问者数_旅游支出额趋势”文件中的 기준연월。
    """
    years = []

    for file in group_files:
        if "추세" in file.name:
            tmp = read_table(file)
            tmp.columns = [normalize_column_name(c) for c in tmp.columns]
            if "date" in tmp.columns:
                dates = tmp["date"].apply(parse_month)
                years.extend(dates.dropna().dt.year.tolist())

    if years:
        return int(pd.Series(years).mode().iloc[0])

    # 추세 파일이 없으면 파일명 또는 현재 연도를 사용할 수밖에 없습니다.
    # 如果没有趋势文件，只能暂时使用当前年份作为默认值。
    return pd.Timestamp.today().year


for prefix, group_files in groups.items():
    print(f"\n[GROUP] {prefix}")

    year = infer_year_from_group(group_files)
    print(f"추정 기준연도 / 推断年份: {year}")

    region_df = None

    for file in group_files:
        print(f"[READ] {file.name}")
        df = read_table(file)
        df.columns = [normalize_column_name(c) for c in df.columns]

        # 지역명 정리 / 地区名称标准化
        if "region" in df.columns:
            df["region"] = df["region"].apply(standardize_region_name)

        # 1. 방문자수 파일 / 访问人数文件
        if "방문자수" in file.name and "추세" not in file.name and "표_" not in file.name and "성" not in file.name:
            use = df[["region", "visitor_count"]].copy()
            use["visitor_count"] = clean_numeric(use["visitor_count"])
            region_df = use if region_df is None else region_df.merge(use, on="region", how="outer")

        # 2. 관광지출액 파일 / 旅游支出额文件
        elif "관광지출액" in file.name and "추세" not in file.name and "표_" not in file.name:
            cols = ["region", "tourism_spending"]
            if "tourism_spending_prev_year" in df.columns:
                cols.append("tourism_spending_prev_year")
            use = df[cols].copy()
            for col in use.columns:
                if col != "region":
                    use[col] = clean_numeric(use[col])
            region_df = use if region_df is None else region_df.merge(use, on="region", how="outer")

        # 3. 목적지검색건수 파일 / 目的地搜索量文件
        elif "목적지검색건수" in file.name:
            use = df[["region", "destination_search"]].copy()
            use["destination_search"] = clean_numeric(use["destination_search"])
            region_df = use if region_df is None else region_df.merge(use, on="region", how="outer")

        # 4. 방문자 체류특성 파일 / 游客停留特征文件
        elif "방문자 체류특성" in file.name:
            # 시군구 단위 데이터를 시도 단위로 평균 집계
            # 将市郡区级别数据按市道平均汇总
            use = df.copy()
            numeric_cols = [c for c in ["avg_stay_time", "avg_lodging_days"] if c in use.columns]
            for col in numeric_cols:
                use[col] = clean_numeric(use[col])

            if "region" in use.columns and numeric_cols:
                use = use.groupby("region", as_index=False)[numeric_cols].mean()
                region_df = use if region_df is None else region_df.merge(use, on="region", how="outer")

        # 5. 월별 추세 파일 / 月度趋势文件
        elif "추세" in file.name:
            use = df.copy()
            if "date" in use.columns:
                use["date"] = use["date"].apply(parse_month)

            for col in [
                "visitor_count", "visitor_count_prev", "visitor_growth_rate",
                "tourism_spending", "tourism_spending_prev", "spending_growth_rate"
            ]:
                if col in use.columns:
                    use[col] = clean_numeric(use[col])

            use["source_group"] = prefix
            monthly_trend_frames.append(use)

        # 6. 관광지 검색순위 파일 / 旅游地搜索排名文件
        elif "관광지검색순위" in file.name:
            use = df.copy()
            use["source_group"] = prefix
            use["year"] = year
            attraction_rank_frames.append(use)

        # 7. 방문자수 최다지역 파일 / 访问人数增长 Top 地区文件
        elif "방문자수최다지역" in file.name:
            use = df.copy()
            use["year"] = year
            use["source_group"] = prefix
            visitor_top_frames.append(use)

        # 8. 성·연령별 방문자 파일 / 性别年龄访问者文件
        elif "연령별" in file.name or "성" in file.name:
            use = df.copy()
            use["year"] = year
            use["source_group"] = prefix
            age_frames.append(use)

    if region_df is not None:
        region_df["year"] = year
        region_df["date"] = pd.to_datetime(f"{year}-01-01")
        annual_region_frames.append(region_df)

if not annual_region_frames:
    raise ValueError(
        "지역 단위 방문자수/관광지출액/검색건수 파일을 찾지 못했습니다.\n"
        "未找到地区级访问人数/旅游支出额/搜索量文件。"
    )

annual = pd.concat(annual_region_frames, ignore_index=True)

# 같은 지역-연도가 여러 번 있으면 평균으로 집계
# 如果同一地区-年份重复，使用平均值聚合
numeric_cols = [c for c in annual.columns if c not in ["region", "year", "date"]]
for col in numeric_cols:
    annual[col] = clean_numeric(annual[col])

annual = annual.groupby(["region", "year"], as_index=False)[numeric_cols].mean()
annual["date"] = pd.to_datetime(annual["year"].astype(str) + "-01-01")

# 전년도 관광지출액이 있으면 관광지출액 회복률 또는 증가율 계산
# 如果有去年旅游支出额，则计算旅游支出恢复率/增长率
if "tourism_spending_prev_year" in annual.columns:
    annual["tourism_spending_recovery_rate"] = annual["tourism_spending"] / annual["tourism_spending_prev_year"].replace(0, np.nan)

# 단일연도 데이터는 월별 추세가 전국 단위이므로 지역별 월 데이터는 만들 수 없습니다.
# 单一年份数据的月度趋势是全国级，因此无法生成地区月度数据。
# 그래도 기존 분석 스크립트와 연결하기 위해 연도 단위 데이터를 저장합니다.
# 为了连接后续分析脚本，保存年度地区数据。
save_csv(annual, DATA_PROCESSED / "tourism_recovery_dataset.csv")
save_csv(annual, DATA_PROCESSED / "tourism_annual_real_merged.csv")

# 월별 전국 추세 저장 / 保存全国月度趋势
if monthly_trend_frames:
    monthly = pd.concat(monthly_trend_frames, ignore_index=True)
    save_csv(monthly, DATA_PROCESSED / "national_monthly_real_trend.csv")

# 부가 데이터 저장 / 保存辅助数据
if attraction_rank_frames:
    save_csv(pd.concat(attraction_rank_frames, ignore_index=True), TABLES / "attraction_search_rank_raw.csv")

if visitor_top_frames:
    save_csv(pd.concat(visitor_top_frames, ignore_index=True), TABLES / "visitor_top_regions_raw.csv")

if age_frames:
    save_csv(pd.concat(age_frames, ignore_index=True), TABLES / "age_gender_visitors_raw.csv")

print("\n실제 관광데이터랩 파일 병합 완료 / 真实旅游数据实验室文件合并完成")
print(annual.head())
print("\n다음 단계 / 下一步：python src/03_clean_merge_data_v2.py")
