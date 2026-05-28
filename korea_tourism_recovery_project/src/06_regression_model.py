"""
随机森林回归模型脚本
랜덤포레스트 회귀모형 스크립트

中文：
使用游客数、搜索量、停留时间等变量预测旅游支出额，
并输出模型评价指标和特征重要度。

한국어:
방문자 수, 검색건수, 체류시간 등의 변수를 사용하여 관광지출액을 예측하고,
모델 평가 지표와 변수 중요도를 출력합니다.
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from utils import DATA_PROCESSED, FIGURES, TABLES, save_csv

plt.rcParams["font.family"] = ["Malgun Gothic", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

path = DATA_PROCESSED / "tourism_recovery_dataset.csv"

if not path.exists():
    raise FileNotFoundError("tourism_recovery_dataset.csv가 없습니다. / 缺少 tourism_recovery_dataset.csv。")

df = pd.read_csv(path, encoding="utf-8-sig")

target = "tourism_spending"

candidate_features = [
    "visitor_count",
    "destination_search",
    "avg_stay_time",
    "avg_lodging_days",
    "tourism_spending_prev_year",
    "tourism_spending_recovery_rate",
    "tourism_spending_growth_rate",
    "spending_per_visitor",
    "visitor_per_search",
    "year",
]

features = [c for c in candidate_features if c in df.columns and c != target]

if target not in df.columns:
    raise ValueError("관광지출액 컬럼이 없습니다. / 缺少 tourism_spending 列。")

model_df = df[["region", target] + features].dropna().copy()

if len(model_df) < 10:
    print("데이터 수가 적어 회귀모형 평가는 참고용으로만 해석하세요.")
    print("数据量较少，回归模型结果仅供参考。")

if len(features) < 2:
    raise ValueError("회귀모형에 사용할 변수가 부족합니다. / 可用于回归的变量不足。")

X = model_df[features]
y = model_df[target]

# 데이터가 적을 수 있으므로 test_size를 작게 설정
# 真实下载数据可能只有 17 个地区，因此测试集比例设小一些
test_size = 0.25 if len(model_df) >= 20 else 0.30

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42
)

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    min_samples_leaf=1
)

model.fit(X_train, y_train)
pred = model.predict(X_test)

mae = mean_absolute_error(y_test, pred)
rmse = mean_squared_error(y_test, pred) ** 0.5
r2 = r2_score(y_test, pred)

metrics = pd.DataFrame([{
    "target": target,
    "model": "RandomForestRegressor",
    "MAE": mae,
    "RMSE": rmse,
    "R2": r2,
    "n_samples": len(model_df),
    "n_features": len(features),
}])

save_csv(metrics, TABLES / "regression_metrics.csv")

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

save_csv(importance, TABLES / "feature_importance.csv")

# 변수 중요도 시각화 / 特征重要度可视化
plt.figure(figsize=(9, 6))
plot_df = importance.sort_values("importance")
plt.barh(plot_df["feature"], plot_df["importance"])
plt.title("Feature Importance / 변수 중요도")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig(FIGURES / "07_feature_importance.png", dpi=200)
plt.close()

# 실제값 vs 예측값 / 实际值 vs 预测值
plt.figure(figsize=(7, 7))
plt.scatter(y_test, pred, alpha=0.7)
plt.title("Actual vs Predicted Tourism Spending\n실제 관광지출액 vs 예측 관광지출액")
plt.xlabel("Actual / 실제값")
plt.ylabel("Predicted / 예측값")

min_v = min(y_test.min(), pred.min())
max_v = max(y_test.max(), pred.max())
plt.plot([min_v, max_v], [min_v, max_v])

plt.tight_layout()
plt.savefig(FIGURES / "08_actual_vs_predicted.png", dpi=200)
plt.close()

print("회귀모형 학습 완료 / 回归模型训练完成")
print(metrics)
print(importance)
