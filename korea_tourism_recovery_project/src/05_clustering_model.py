"""
K-Means 聚类分析脚本
K-Means 군집분석 스크립트

中文：
根据旅游复苏指数、游客数、旅游支出、搜索量、停留时间等变量，
把韩国各地区分成不同旅游恢复/活跃类型。

한국어:
관광 회복지수, 방문자 수, 관광지출액, 검색건수, 체류시간 등을 기반으로
한국 지역을 여러 관광 회복/활성 유형으로 군집화합니다.
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from utils import DATA_PROCESSED, FIGURES, TABLES, save_csv

plt.rcParams["font.family"] = ["Malgun Gothic", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

path = DATA_PROCESSED / "tourism_recovery_dataset.csv"

if not path.exists():
    raise FileNotFoundError("tourism_recovery_dataset.csv가 없습니다. / 缺少 tourism_recovery_dataset.csv。")

annual = pd.read_csv(path, encoding="utf-8-sig")
latest_year = int(annual["year"].max())
df = annual[annual["year"] == latest_year].copy()

# 군집분석에 사용할 후보 변수 / 聚类分析候选变量
candidate_features = [
    "tourism_recovery_index",
    "visitor_count",
    "tourism_spending",
    "destination_search",
    "avg_stay_time",
    "avg_lodging_days",
    "tourism_spending_recovery_rate",
    "tourism_spending_growth_rate",
    "spending_per_visitor",
    "visitor_per_search",
    "tourism_consumption_share",
]

features = [c for c in candidate_features if c in df.columns]

if len(features) < 2:
    raise ValueError("군집분석에 사용할 변수가 부족합니다. / 可用于聚类的变量不足。")

X = df[features].fillna(df[features].median())

# 표준화 / 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K 후보 탐색 / 搜索合适的 K
max_k = min(8, len(df))
possible_k = range(2, max_k)

scores = []
inertias = []

for k in possible_k:
    model = KMeans(n_clusters=k, random_state=42, n_init=20)
    labels = model.fit_predict(X_scaled)
    inertias.append(model.inertia_)
    scores.append(silhouette_score(X_scaled, labels))

score_df = pd.DataFrame({
    "k": list(possible_k),
    "inertia": inertias,
    "silhouette": scores,
})

save_csv(score_df, TABLES / "kmeans_k_selection.csv")

best_k = int(score_df.sort_values("silhouette", ascending=False).iloc[0]["k"])

# 최적 K로 최종 군집분석 / 使用最佳 K 进行最终聚类
model = KMeans(n_clusters=best_k, random_state=42, n_init=30)
df["cluster"] = model.fit_predict(X_scaled)

cluster_result = df[["region", "year", "cluster"] + features].sort_values(["cluster", "tourism_recovery_index"])
save_csv(cluster_result, DATA_PROCESSED / "cluster_result.csv")

profile = df.groupby("cluster")[features].mean().reset_index()
profile["count"] = df.groupby("cluster").size().values
save_csv(profile, TABLES / "cluster_profile.csv")

# Silhouette 그래프 / 轮廓系数图
plt.figure(figsize=(8, 5))
plt.plot(score_df["k"], score_df["silhouette"], marker="o")
plt.title("Silhouette Score by K / K별 실루엣 점수")
plt.xlabel("K")
plt.ylabel("Silhouette Score")
plt.tight_layout()
plt.savefig(FIGURES / "05_kmeans_silhouette.png", dpi=200)
plt.close()

# Elbow 그래프 / Elbow 方法图
plt.figure(figsize=(8, 5))
plt.plot(score_df["k"], score_df["inertia"], marker="o")
plt.title("Elbow Method / 엘보우 방법")
plt.xlabel("K")
plt.ylabel("Inertia")
plt.tight_layout()
plt.savefig(FIGURES / "06_kmeans_elbow.png", dpi=200)
plt.close()

print(f"K-Means 완료 / K-Means 完成，best_k = {best_k}")
print(cluster_result[["region", "cluster", "tourism_recovery_index"]])
