# 한국 지역별 관광 회복력 및 관광소비 불균형 분석

# 韩国地区旅游复苏能力与旅游消费不均衡分析

## 1. 프로젝트 개요 / 项目概要

본 프로젝트는 Korea Tourism Data Lab의 관광 빅데이터를 활용하여 2020년부터 2025년까지 한국 관광 수요의 회복 추세와 지역별 관광소비 불균형을 분석한 프로젝트이다. 분석 대상은 전국 17개 광역시도이며, 총 102개의 지역-연도 단위 데이터를 구성하였다.

방문자 수, 관광지출액, 목적지 검색건수, 평균 체류시간, 평균 숙박일 등의 변수를 통합하여 지역별 관광 회복/활성 지수를 산출하였다. 또한 K-Means 군집분석을 통해 지역 관광 유형을 구분하고, Random Forest 회귀모형을 활용하여 관광지출액에 영향을 미치는 주요 변수를 확인하였다.

本项目使用 Korea Tourism Data Lab 的旅游大数据，分析 2020 年至 2025 年韩国旅游需求恢复趋势及地区旅游消费不均衡现象。分析对象为韩国 17 个广域市道，共构建 102 条“地区-年度”单位数据。

项目整合访问人数、旅游支出额、目的地搜索量、平均停留时间、平均住宿天数等指标，构建地区旅游复苏/活跃度指数，并通过 K-Means 聚类和 Random Forest 回归模型分析地区旅游结构和旅游支出的主要影响因素。

---

## 2. 연구 주제 / 研究题目

한국 지역별 관광 회복력 및 관광소비 불균형 분석: 관광 빅데이터 기반 지역 활성화 전략 제안

韩国地区旅游复苏能力与旅游消费不均衡分析：基于旅游大数据的区域活性化策略研究

---

## 3. 데이터 / 数据

주요 데이터는 Korea Tourism Data Lab에서 다운로드한 CSV 파일을 사용하였다. 원본 데이터는 `data/raw/datalab/` 폴더에 저장하고, 전처리 후 생성된 데이터는 `data/processed/` 폴더에 저장된다.

主要数据来自 Korea Tourism Data Lab 下载的 CSV 文件。原始数据放置在 `data/raw/datalab/` 文件夹中，处理后的数据保存在 `data/processed/` 文件夹中。

### 데이터 범위 / 数据范围

| 항목 / 项目           | 내용 / 内容             |
| ----------------- | ------------------- |
| 데이터 기간 / 数据期间     | 2020.01 ~ 2025.12   |
| 분석 지역 / 分析地区      | 17개 광역시도 / 17 个广域市道 |
| 분석 단위 / 分析单位      | 지역-연도 단위 / 地区-年度单位  |
| 전체 샘플 수 / 样本数     | 102개 / 102 条        |
| 최종 분석 연도 / 最终分析年份 | 2025년 / 2025 年      |

2026년 자료는 일부 월만 존재하므로 최종 분석에서는 제외하였다. 최종 분석은 완전 연도 자료인 2020년부터 2025년까지의 데이터만 사용하였다.

由于 2026 年数据只包含部分月份，因此未纳入最终分析。最终分析只使用 2020 年至 2025 年的完整年度数据。

### 사용한 주요 변수 / 使用的主要变量

| 구분 / 类别     | 변수 / 变量                              |
| ----------- | ------------------------------------ |
| 방문 / 访问     | 방문자 수 / visitor_count                |
| 소비 / 消费     | 관광지출액 / tourism_spending             |
| 검색 / 搜索     | 목적지 검색건수 / destination_search        |
| 체류 / 停留     | 평균 체류시간 / avg_stay_time              |
| 숙박 / 住宿     | 평균 숙박일 / avg_lodging_days            |
| 파생변수 / 派生变量 | 관광 회복/활성 지수 / tourism_recovery_index |
| 파생변수 / 派生变量 | 관광소비 비중 / tourism_consumption_share  |

데이터셋 URL:
https://datalab.visitkorea.or.kr/datalab/portal/loc/getAreaDataForm.do

---

## 4. 프로젝트 구조 / 项目结构

```text
korea_tourism_recovery_project/
├─ app.py
├─ run_real_data.bat
├─ run_dashboard.bat
├─ requirements.txt
├─ src/
│  ├─ 02_load_datalab_real_files.py
│  ├─ 03_clean_merge_data_v2.py
│  ├─ 04_eda_visualization.py
│  ├─ 05_clustering_model.py
│  ├─ 06_regression_model.py
│  └─ 07_make_final_outputs.py
├─ data/
│  ├─ raw/datalab/
│  └─ processed/
└─ outputs/
   ├─ figures/
   ├─ tables/
   └─ maps/
```

---

## 5. 실행 환경 / 运行环境

본 프로젝트는 Windows와 PyCharm 환경을 기준으로 구성하였다. Python 3.10 이상 환경에서 실행할 수 있다.

本项目主要面向 Windows 和 PyCharm 环境，建议使用 Python 3.10 以上版本运行。

```bash
pip install -r requirements.txt
pip install streamlit
```

`requirements.txt`에 다음 항목이 포함되어 있지 않다면 추가한다.

如果 `requirements.txt` 中没有以下内容，请补充：

```text
streamlit>=1.30.0
```

---

## 6. 분석 실행 방법 / 分析运行方法

Korea Tourism Data Lab에서 다운로드한 실제 CSV 데이터를 사용하는 경우 아래 순서대로 실행한다.

使用 Korea Tourism Data Lab 下载的真实 CSV 数据时，按以下顺序运行：

```bash
python src/02_load_datalab_real_files.py
python src/03_clean_merge_data_v2.py
python src/04_eda_visualization.py
python src/05_clustering_model.py
python src/06_regression_model.py
python src/07_make_final_outputs.py
```

또는 Windows 환경에서 다음 파일을 실행할 수 있다.

也可以在 Windows 中直接运行：

```bash
run_real_data.bat
```

### 주의 / 注意

* 실제 분석 시 `data/raw/datalab/` 폴더에 다운로드한 CSV 파일을 넣는다.
  真实分析时，将下载的 CSV 文件放入 `data/raw/datalab/`。

* 최종 분석에서는 2020년부터 2025년까지의 완전 연도 데이터만 사용한다.
  最终分析只使用 2020 年至 2025 年的完整年度数据。

* 2026년 일부 월 데이터는 최종 지역별 비교와 군집분석에서 제외한다.
  2026 年部分月份数据不用于最终地区比较和聚类分析。

---

## 7. 대시보드 실행 / 前端页面运行

Streamlit을 사용하여 분석 결과를 웹 대시보드로 확인할 수 있다.

可以使用 Streamlit 前端页面查看分析结果。

```bash
streamlit run app.py
```

또는 다음 파일을 실행한다.

或直接运行：

```bash
run_dashboard.bat
```

대시보드는 다음 결과 파일을 읽어 화면에 표시한다.

前端页面会读取以下结果文件并展示：

```text
outputs/figures/
outputs/tables/
outputs/maps/
data/processed/
```

---

## 8. 주요 결과 파일 / 主要结果文件

| 파일 / 文件                                               | 내용 / 内容                                |
| ----------------------------------------------------- | -------------------------------------- |
| `data/processed/tourism_recovery_dataset.csv`         | 최종 분석 데이터 / 最终分析数据                     |
| `data/processed/tourism_recovery_index_by_region.csv` | 지역별 관광 회복/활성 지수 / 地区旅游复苏活跃度指数          |
| `data/processed/cluster_result.csv`                   | 지역별 군집분석 결과 / 地区聚类结果                   |
| `outputs/tables/final_summary_table.csv`              | 지역별 최종 요약표 / 地区最终汇总表                   |
| `outputs/tables/latest_year_recovery_ranking.csv`     | 2025년 관광 회복/활성 지수 순위 / 2025 年旅游复苏活跃度排名 |
| `outputs/tables/tourism_spending_concentration.csv`   | 관광소비 집중도 / 旅游消费集中度                     |
| `outputs/tables/cluster_profile.csv`                  | 군집별 평균 특성 / 聚类画像                       |
| `outputs/tables/regression_metrics.csv`               | 회귀모형 평가 결과 / 回归模型评价结果                  |
| `outputs/tables/feature_importance.csv`               | 변수 중요도 / 特征重要度                         |
| `outputs/maps/tourism_recovery_map.html`              | 관광 회복/활성 지도 / 旅游复苏活跃度地图                |
| `outputs/figures/`                                    | 분석 시각화 이미지 / 分析图表                      |

---

## 9. 분석 방법 / 分析方法

1. Korea Tourism Data Lab CSV 파일을 연도별로 다운로드하였다.
   按年度下载 Korea Tourism Data Lab 的 CSV 文件。

2. 파일명 접두어와 기준연월 정보를 활용하여 연도별 데이터를 구분하였다.
   根据文件名前缀和基准年月信息区分年度数据。

3. 방문자 수, 관광지출액, 목적지 검색건수, 평균 체류시간, 평균 숙박일 데이터를 지역 기준으로 통합하였다.
   以地区为单位整合访问人数、旅游支出额、目的地搜索量、平均停留时间、平均住宿天数等数据。

4. 결측값 처리, 수치형 변환, 파생변수 생성을 수행하였다.
   进行缺失值处理、数值型转换和派生变量生成。

5. Min-Max 정규화를 통해 관광 회복/활성 지수를 계산하였다.
   使用 Min-Max 标准化计算旅游复苏/活跃度指数。

6. K-Means 군집분석으로 지역 관광 유형을 구분하였다.
   使用 K-Means 聚类划分地区旅游类型。

7. Random Forest 회귀모형으로 관광지출액에 영향을 미치는 주요 변수를 확인하였다.
   使用 Random Forest 回归模型分析影响旅游支出的主要变量。

8. Folium과 Streamlit을 활용하여 지도와 대시보드를 구성하였다.
   使用 Folium 和 Streamlit 展示地图与前端页面。

---

## 10. 주요 분석 결과 / 主要分析结果

### 10.1 전국 관광 추세 / 全国旅游趋势

2020년 이후 전국 방문자 수와 관광지출액은 월별 변동은 있으나 전반적으로 증가하는 추세를 보였다. 이는 코로나19 이후 국내 관광 수요와 관광소비가 점진적으로 회복되었음을 보여준다.

2020 年以后，全国访问人数和旅游支出虽然存在月度波动，但整体呈上升趋势，说明 COVID-19 后韩国国内旅游需求和旅游消费逐步恢复。

### 10.2 지역별 관광 회복/활성 지수 / 地区旅游复苏活跃度指数

2025년 기준 관광 회복/활성 지수 상위 지역은 다음과 같다.

2025 年旅游复苏/活跃度指数前五地区如下：

| 순위 / 排名 | 지역 / 地区 |
| ------- | ------- |
| 1       | 경기도     |
| 2       | 서울특별시   |
| 3       | 인천광역시   |
| 4       | 제주특별자치도 |
| 5       | 부산광역시   |

하위 지역은 충청북도, 광주광역시, 대전광역시, 울산광역시, 전북특별자치도 순으로 나타났다.

排名较低的地区依次为忠清北道、光州广域市、大田广域市、蔚山广域市、全北特别自治道。

### 10.3 관광소비 집중도 / 旅游消费集中度

관광지출액 기준으로 서울특별시와 경기도의 비중이 매우 높게 나타났다. 두 지역의 관광소비 비중 합계는 약 53.5%로, 전체 관광소비의 절반 이상이 수도권에 집중되어 있음을 확인하였다.

从旅游支出额来看，首尔特别市和京畿道占比最高。两者合计约占 53.5%，说明全国旅游消费的一半以上集中在首都圈。

### 10.4 K-Means 군집분석 / K-Means 聚类分析

K-Means 군집분석 결과, K=2가 가장 적절한 군집 수로 나타났다.

K-Means 聚类结果显示，K=2 是较合适的聚类数量。

| 군집 / 聚类   | 설명 / 说明                            |
| --------- | ---------------------------------- |
| Cluster 1 | 수도권 고활성·고소비 관광거점형 / 首都圈高活跃高消费旅游据点型 |
| Cluster 0 | 일반 지역 관광형 / 一般地区旅游型                |

Cluster 1은 서울특별시와 경기도로 구성되며, 나머지 15개 지역은 Cluster 0으로 분류되었다.

Cluster 1 由首尔特别市和京畿道组成，其余 15 个地区属于 Cluster 0。

### 10.5 Random Forest 변수 중요도 / Random Forest 变量重要度

Random Forest 회귀분석 결과, 관광지출액에 중요한 영향을 미치는 변수는 다음과 같이 나타났다.

Random Forest 回归分析结果显示，影响旅游支出的主要变量如下：

| 순위 / 排名 | 변수 / 变量                                |
| ------- | -------------------------------------- |
| 1       | 방문자 수 / visitor_count                  |
| 2       | 전년도 관광지출액 / tourism_spending_prev_year |
| 3       | 목적지 검색건수 / destination_search          |

다만 전년도 관광지출액은 목표 변수와 높은 관련성을 가지므로, 본 프로젝트에서는 예측 성능보다 변수 중요도 해석에 중점을 두었다.

由于前一年旅游支出额与目标变量具有较高相关性，因此本项目更侧重于变量重要度解释，而不是过度强调预测准确率。

---

## 11. 한계점 / 局限性

1. 분석 단위가 광역시도 수준이므로 시군구 내부 차이는 충분히 반영하지 못하였다.
   分析单位为广域市道，未能充分反映市郡区内部差异。

2. 2026년 자료는 일부 월만 존재하므로 최종 분석에서 제외하였다.
   2026 年数据只有部分月份，因此未纳入最终分析。

3. Random Forest 모형은 관광지출액 영향요인 해석을 위한 보조적 분석으로 활용하였다.
   Random Forest 模型主要作为影响因素解释的辅助分析。

4. 향후 교통 접근성, 숙박시설 수, 지역축제, GRDP 등 외부 변수를 추가하면 더 풍부한 분석이 가능하다.
   后续可以加入交通可达性、住宿设施数量、地区节庆、GRDP 等外部变量，使分析更加丰富。

---

## 12. 참고 문헌 및 코드 / 参考文献与代码

### 참고 문헌 / 参考文献

1. 전광상(2026), *내국인 관광 수요 분포의 복잡계적 구조 분석: 코로나19 이전･확산기･회복기 비교*
   https://doi.org/10.22776/kgs.2026.61.1.99

2. Yoo, Lee & Hong(2025), *Proximity, Resilience, and Blue Urbanism: Spatial Dynamics of Post-Pandemic Recovery in South Korea’s Coastal Fishing Communities*
   https://www.mdpi.com/2073-445X/14/6/1303

### Code

https://github.com/ziqiaowang2-web/korea_tourism_recovery_project
