"""
演示数据生成脚本 / 샘플 데이터 생성 스크립트

中文：
如果还没有下载真实 Korea Tourism Data Lab 数据，可以先运行本脚本生成模拟数据，
用于测试整个分析流程是否能够正常运行。

한국어:
실제 Korea Tourism Data Lab 데이터를 아직 다운로드하지 못한 경우,
본 스크립트를 먼저 실행하여 샘플 데이터를 생성하고 전체 분석 흐름을 테스트할 수 있습니다.
"""

import numpy as np
import pandas as pd
from utils import DATA_RAW, save_csv

np.random.seed(42)

# 17개 광역시도 / 韩国 17 个广域市道
regions = [
    "서울특별시", "부산광역시", "대구광역시", "인천광역시", "광주광역시",
    "대전광역시", "울산광역시", "세종특별자치시", "경기도", "강원특별자치도",
    "충청북도", "충청남도", "전북특별자치도", "전라남도", "경상북도",
    "경상남도", "제주특별자치도"
]

# 2020년 1월부터 2025년 6월까지 월별 데이터 생성
# 生成 2020年1月 到 2025年6月 的月度数据
months = pd.date_range("2020-01-01", "2025-06-01", freq="MS")

base_visitors = {
    "서울특별시": 4200000, "부산광역시": 1700000, "대구광역시": 850000,
    "인천광역시": 1100000, "광주광역시": 600000, "대전광역시": 650000,
    "울산광역시": 450000, "세종특별자치시": 180000, "경기도": 3600000,
    "강원특별자치도": 1600000, "충청북도": 700000, "충청남도": 950000,
    "전북특별자치도": 780000, "전라남도": 920000, "경상북도": 1150000,
    "경상남도": 1300000, "제주특별자치도": 1500000
}

tourism_power = {
    "서울특별시": 1.25, "부산광역시": 1.15, "대구광역시": 0.80,
    "인천광역시": 0.90, "광주광역시": 0.75, "대전광역시": 0.78,
    "울산광역시": 0.72, "세종특별자치시": 0.55, "경기도": 1.05,
    "강원특별자치도": 1.20, "충청북도": 0.82, "충청남도": 0.90,
    "전북특별자치도": 0.86, "전라남도": 0.95, "경상북도": 0.96,
    "경상남도": 1.00, "제주특별자치도": 1.35
}

rows = []

for region in regions:
    for date in months:
        year = date.year
        month = date.month

        # 코로나19 이후 회복 패턴을 단순화하여 반영
        # 简化模拟 COVID-19 后的旅游恢复趋势
        if year == 2020:
            recovery = 0.58 + 0.02 * (month / 12)
        elif year == 2021:
            recovery = 0.66 + 0.05 * (month / 12)
        elif year == 2022:
            recovery = 0.78 + 0.08 * (month / 12)
        elif year == 2023:
            recovery = 0.93 + 0.05 * (month / 12)
        elif year == 2024:
            recovery = 1.03 + 0.04 * (month / 12)
        else:
            recovery = 1.08 + 0.02 * (month / 12)

        # 계절성 반영 / 加入季节性
        seasonality = 1.0 + 0.18 * np.sin((month - 1) / 12 * 2 * np.pi)

        if region in ["강원특별자치도", "제주특별자치도", "부산광역시"] and month in [7, 8]:
            seasonality += 0.25

        if region in ["서울특별시", "경기도"] and month in [4, 5, 10]:
            seasonality += 0.10

        visitor_count = base_visitors[region] * recovery * seasonality * np.random.normal(1, 0.07)
        visitor_count = max(visitor_count, 10000)

        unique_visitors = visitor_count * np.random.uniform(0.70, 0.88)
        avg_stay_time = np.random.normal(4.0, 0.6) * tourism_power[region]
        avg_lodging_days = np.random.normal(1.2, 0.25) * tourism_power[region]
        lodging_visitor_ratio = np.clip(np.random.normal(0.22, 0.07) * tourism_power[region], 0.05, 0.75)
        destination_search = visitor_count * np.random.uniform(0.06, 0.12)
        tourism_spending = visitor_count * np.random.uniform(38000, 72000) * tourism_power[region]

        rows.append({
            "date": date.strftime("%Y-%m"),
            "region": region,
            "visitor_count": round(visitor_count),
            "unique_visitors": round(unique_visitors),
            "tourism_spending": round(tourism_spending),
            "destination_search": round(destination_search),
            "avg_stay_time": round(avg_stay_time, 2),
            "avg_lodging_days": round(max(avg_lodging_days, 0.1), 2),
            "lodging_visitor_ratio": round(lodging_visitor_ratio, 3),
        })

tourism_df = pd.DataFrame(rows)
save_csv(tourism_df, DATA_RAW / "datalab" / "sample_korea_tourism_datalab.csv")

# KOSIS 보조변수 샘플 / KOSIS 辅助变量模拟数据
control_rows = []

for region in regions:
    pop = np.random.randint(500000, 14000000)
    grdp = pop * np.random.randint(25, 65) * 1_000_000
    control_rows.append({
        "region": region,
        "population": pop,
        "grdp": grdp,
        "accommodation_business_count": np.random.randint(250, 4500),
        "restaurant_business_count": np.random.randint(3000, 90000),
    })

controls = pd.DataFrame(control_rows)
save_csv(controls, DATA_RAW / "kosis" / "sample_region_controls.csv")

print("演示数据已生成。/ 샘플 데이터가 생성되었습니다.")
print("下一步运行：python src/02_load_datalab_files.py")
print("다음 단계 실행: python src/02_load_datalab_files.py")
