"""
最终结果输出脚本
최종 결과 출력 스크립트

中文：
生成最终汇总表、HTML 地图和简要结果摘要。

한국어:
최종 요약표, HTML 지도, 간단한 결과 요약 문서를 생성합니다.
"""

import pandas as pd
import folium
from utils import DATA_PROCESSED, OUTPUTS, MAPS, TABLES, save_csv

annual_path = DATA_PROCESSED / "tourism_recovery_dataset.csv"
cluster_path = DATA_PROCESSED / "cluster_result.csv"

if not annual_path.exists():
    raise FileNotFoundError("tourism_recovery_dataset.csv가 없습니다. / 缺少 tourism_recovery_dataset.csv。")

annual = pd.read_csv(annual_path, encoding="utf-8-sig")
latest_year = int(annual["year"].max())
latest = annual[annual["year"] == latest_year].copy()

# 군집 결과가 있으면 병합 / 如果存在聚类结果，则合并
if cluster_path.exists():
    cluster = pd.read_csv(cluster_path, encoding="utf-8-sig")
    latest = latest.merge(cluster[["region", "cluster"]], on="region", how="left")

# 지도 표시용 광역시도 중심 좌표 / 地图显示用的广域市道中心坐标
coords = {
    "서울특별시": [37.5665, 126.9780],
    "부산광역시": [35.1796, 129.0756],
    "대구광역시": [35.8714, 128.6014],
    "인천광역시": [37.4563, 126.7052],
    "광주광역시": [35.1595, 126.8526],
    "대전광역시": [36.3504, 127.3845],
    "울산광역시": [35.5384, 129.3114],
    "세종특별자치시": [36.4800, 127.2890],
    "경기도": [37.4138, 127.5183],
    "강원특별자치도": [37.8228, 128.1555],
    "충청북도": [36.6357, 127.4917],
    "충청남도": [36.5184, 126.8000],
    "전북특별자치도": [35.7175, 127.1530],
    "전라남도": [34.8679, 126.9910],
    "경상북도": [36.4919, 128.8889],
    "경상남도": [35.4606, 128.2132],
    "제주특별자치도": [33.4996, 126.5312],
}

# Folium 지도 생성 / 创建 Folium 地图
m = folium.Map(location=[36.4, 127.8], zoom_start=7)

for _, row in latest.iterrows():
    region = row["region"]

    if region not in coords:
        continue

    score = row.get("tourism_recovery_index", 0)
    spending = row.get("tourism_spending", 0)
    visitors = row.get("visitor_count", 0)
    search = row.get("destination_search", 0)
    cluster = row.get("cluster", "NA")

    radius = 6 + float(score) * 18

    popup = (
        f"<b>{region}</b><br>"
        f"Year: {latest_year}<br>"
        f"Recovery/Activity Index: {score:.3f}<br>"
        f"Visitors: {visitors:,.0f}<br>"
        f"Spending: {spending:,.0f}<br>"
        f"Search Count: {search:,.0f}<br>"
        f"Cluster: {cluster}"
    )

    folium.CircleMarker(
        location=coords[region],
        radius=radius,
        popup=popup,
        fill=True,
        fill_opacity=0.65,
    ).add_to(m)

map_path = MAPS / "tourism_recovery_map.html"
m.save(str(map_path))
print(f"[SAVE] {map_path}")

# 최종 요약표 / 最终汇总表
summary_cols = [
    "region", "year", "tourism_recovery_index",
    "visitor_count", "tourism_spending", "destination_search",
    "avg_stay_time", "avg_lodging_days",
    "tourism_consumption_share", "spending_per_visitor"
]

summary_cols = [c for c in summary_cols if c in latest.columns]

if "cluster" in latest.columns:
    summary_cols.append("cluster")

summary = latest[summary_cols].sort_values("tourism_recovery_index", ascending=False)
save_csv(summary, TABLES / "final_summary_table.csv")

# 간단한 마크다운 요약 작성 / 生成简要 Markdown 摘要
top5 = summary.head(5)[["region", "tourism_recovery_index"]].to_string(index=False)
bottom5 = summary.tail(5)[["region", "tourism_recovery_index"]].to_string(index=False)

report = f"""
# Final Output Summary / 최종 결과 요약

Analysis year / 분석 연도: {latest_year}

## Top 5 regions by tourism recovery/activity index
## 관광 회복/활성 지수 상위 5개 지역

{top5}

## Bottom 5 regions by tourism recovery/activity index
## 관광 회복/활성 지수 하위 5개 지역

{bottom5}

## Generated files / 생성된 파일

- outputs/maps/tourism_recovery_map.html
- outputs/tables/final_summary_table.csv
- outputs/figures/*.png
"""

(OUTPUTS / "final_output_summary.md").write_text(report, encoding="utf-8")

print(report)
print("최종 결과 생성 완료 / 最终结果生成完成")
