"""
探索性数据分析与可视化脚本
탐색적 데이터 분석 및 시각화 스크립트

中文：
生成游客趋势、旅游消费、地区复苏指数排名等图表。

한국어:
방문자 추세, 관광지출액, 지역별 관광 회복지수 순위 등의 시각화를 생성합니다.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from utils import DATA_PROCESSED, FIGURES, TABLES, save_csv

# Windows에서 한글 표시를 위해 Malgun Gothic 사용
# Windows 下使用 Malgun Gothic 显示韩文
plt.rcParams["font.family"] = ["Malgun Gothic", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

annual_path = DATA_PROCESSED / "tourism_recovery_dataset.csv"

if not annual_path.exists():
    raise FileNotFoundError("tourism_recovery_dataset.csv가 없습니다. / 缺少 tourism_recovery_dataset.csv。")

annual = pd.read_csv(annual_path, encoding="utf-8-sig")

# 월별 데이터가 있으면 월별 추세 사용, 없으면 연도별 데이터 사용
# 如果有月度数据则使用月度趋势，否则使用年度数据
monthly_path = DATA_PROCESSED / "tourism_monthly_clean.csv"
real_monthly_path = DATA_PROCESSED / "national_monthly_real_trend.csv"

if monthly_path.exists():
    monthly = pd.read_csv(monthly_path, encoding="utf-8-sig", parse_dates=["date"])
    national = monthly.groupby("date", as_index=False).agg({
        "visitor_count": "sum",
        "tourism_spending": "sum",
    })
elif real_monthly_path.exists():
    national = pd.read_csv(real_monthly_path, encoding="utf-8-sig")
    if "date" in national.columns:
        national["date"] = pd.to_datetime(national["date"])
else:
    national = None

# 1. 월별 또는 연도별 방문자 추세 / 月度或年度游客趋势
if national is not None and "visitor_count" in national.columns:
    save_csv(national, TABLES / "national_monthly_trend.csv")

    plt.figure(figsize=(12, 6))
    plt.plot(national["date"], national["visitor_count"], marker="o")
    plt.title("Visitor Count Trend / 방문자 수 추세")
    plt.xlabel("Date / 날짜")
    plt.ylabel("Visitor Count / 방문자 수")
    plt.tight_layout()
    plt.savefig(FIGURES / "01_visitor_trend.png", dpi=200)
    plt.close()

if national is not None and "tourism_spending" in national.columns:
    plt.figure(figsize=(12, 6))
    plt.plot(national["date"], national["tourism_spending"], marker="o")
    plt.title("Tourism Spending Trend / 관광지출액 추세")
    plt.xlabel("Date / 날짜")
    plt.ylabel("Tourism Spending / 관광지출액")
    plt.tight_layout()
    plt.savefig(FIGURES / "02_spending_trend.png", dpi=200)
    plt.close()

# 2. 최신 연도 기준 지역별 관광 회복/활성 지수
# 最新年份地区旅游复苏/活跃度指数
latest_year = int(annual["year"].max())
latest = annual[annual["year"] == latest_year].copy()

ranking_cols = ["region", "year", "tourism_recovery_index"]
for c in ["visitor_count", "tourism_spending", "destination_search", "spending_per_visitor"]:
    if c in latest.columns:
        ranking_cols.append(c)

ranking = latest.sort_values("tourism_recovery_index", ascending=False)[ranking_cols]
save_csv(ranking, TABLES / "latest_year_recovery_ranking.csv")

plt.figure(figsize=(12, 7))
plot_df = ranking.sort_values("tourism_recovery_index")
plt.barh(plot_df["region"], plot_df["tourism_recovery_index"])
plt.title(f"Tourism Recovery/Activity Index by Region ({latest_year})\n지역별 관광 회복/활성 지수")
plt.xlabel("Index / 지수")
plt.tight_layout()
plt.savefig(FIGURES / "03_recovery_index_by_region.png", dpi=200)
plt.close()

# 3. 관광지출액 지역별 비교 / 各地区旅游支出额比较
if "tourism_spending" in latest.columns:
    spending_rank = latest.sort_values("tourism_spending", ascending=False)[["region", "tourism_spending"]]
    if "tourism_consumption_share" in latest.columns:
        spending_rank["tourism_consumption_share"] = latest.set_index("region").loc[spending_rank["region"], "tourism_consumption_share"].values

    save_csv(spending_rank, TABLES / "tourism_spending_concentration.csv")

    plt.figure(figsize=(12, 7))
    plot_df = spending_rank.sort_values("tourism_spending")
    plt.barh(plot_df["region"], plot_df["tourism_spending"])
    plt.title(f"Tourism Spending by Region ({latest_year})\n지역별 관광지출액")
    plt.xlabel("Tourism Spending / 관광지출액")
    plt.tight_layout()
    plt.savefig(FIGURES / "04_spending_by_region.png", dpi=200)
    plt.close()

print("EDA 시각화 완료 / EDA 可视化完成")
