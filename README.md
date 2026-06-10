# 한국 지역별 관광 회복력 및 관광소비 불균형 분석  
# 韩国地区旅游复苏能力与旅游消费不均衡分析

## 1. 프로젝트 개요 / 项目概要

본 프로젝트는 Korea Tourism Data Lab의 관광 빅데이터를 활용하여 한국 지역별 관광 회복력과 관광소비 불균형을 분석한다. 방문자 수, 관광지출액, 목적지 검색건수, 평균 체류시간 등의 지표를 통합하여 지역별 관광 회복/활성 지수를 산출하고, K-Means 군집분석과 Random Forest 회귀모형을 통해 지역 관광 구조와 주요 영향요인을 확인하였다.

本项目使用 Korea Tourism Data Lab 的旅游大数据，分析韩国各地区的旅游复苏能力和旅游消费不均衡。通过整合访问人数、旅游支出额、目的地搜索量、平均停留时间等指标，构建地区旅游复苏/活跃度指数，并使用 K-Means 聚类和 Random Forest 回归模型分析地区旅游结构及主要影响因素。

---

## 2. 연구 주제 / 研究题目

**한국어**  
한국 지역별 관광 회복력 및 관광소비 불균형 분석: 관광 빅데이터 기반 지역 활성화 전략 제안

**中文**  
韩国地区旅游复苏能力与旅游消费不均衡分析：基于旅游大数据的区域活性化策略研究

---

## 3. 데이터 / 数据

주요 데이터는 Korea Tourism Data Lab에서 다운로드한 CSV 파일을 사용하였다. 원본 데이터는 `data/raw/datalab/` 폴더에 저장한다.

主要数据来自 Korea Tourism Data Lab 下载的 CSV 文件。原始数据放置在 `data/raw/datalab/` 文件夹中。

**사용한 주요 변수 / 使用的主要变量**

| 구분 / 类别 | 변수 / 变量 |
|---|---|
| 방문 / 访问 | 방문자 수 / visitor_count |
| 소비 / 消费 | 관광지출액 / tourism_spending |
| 검색 / 搜索 | 목적지 검색건수 / destination_search |
| 체류 / 停留 | 평균 체류시간 / avg_stay_time |
| 숙박 / 住宿 | 평균 숙박일수 / avg_lodging_days |

**데이터셋 URL / 数据集链接**  
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

**한국어**  
Python 3.10 이상 환경에서 실행하였다. Windows와 PyCharm 환경을 기준으로 구성하였다.

**中文**  
本项目在 Python 3.10 以上环境运行，主要面向 Windows 和 PyCharm 环境。

**필수 패키지 설치 / 安装依赖**

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

**한국어**  
실제 Korea Tourism Data Lab 데이터를 사용하는 경우 아래 순서대로 실행한다.

**中文**  
使用真实 Korea Tourism Data Lab 数据时，按以下顺序运行：

```bash
python src/02_load_datalab_real_files.py
python src/03_clean_merge_data_v2.py
python src/04_eda_visualization.py
python src/05_clustering_model.py
python src/06_regression_model.py
python src/07_make_final_outputs.py
```

또는 Windows에서 다음 파일을 실행할 수 있다.  
也可以在 Windows 中直接运行：

```bash
run_real_data.bat
```

**주의 / 注意**

- 실제 분석 시 `data/raw/datalab/` 폴더에 다운로드한 CSV 파일을 넣는다.  
  真实分析时，将下载的 CSV 文件放入 `data/raw/datalab/`。
- `sample_korea_tourism_datalab.csv`는 테스트용 파일이므로 최종 분석에서는 제거한다.  
  `sample_korea_tourism_datalab.csv` 是测试文件，正式分析时删除。

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

| 파일 / 文件 | 내용 / 内容 |
|---|---|
| `data/processed/tourism_recovery_dataset.csv` | 최종 분석 데이터 / 最终分析数据 |
| `outputs/tables/final_summary_table.csv` | 지역별 최종 요약표 / 地区最终汇总表 |
| `outputs/tables/cluster_profile.csv` | 군집별 평균 특성 / 聚类画像 |
| `outputs/tables/regression_metrics.csv` | 회귀모형 평가 결과 / 回归模型评价结果 |
| `outputs/tables/feature_importance.csv` | 변수 중요도 / 特征重要度 |
| `outputs/maps/tourism_recovery_map.html` | 관광 회복/활성 지도 / 旅游复苏活跃度地图 |
| `outputs/figures/` | 분석 시각화 이미지 / 分析图表 |

---

## 9. 분석 방법 / 分析方法


1. 관광데이터랩 CSV 파일을 불러와 지역명과 컬럼명을 정리하였다.  
2. 방문자 수, 관광지출액, 검색건수, 체류시간 등을 통합하였다.  
3. Min-Max 정규화를 통해 관광 회복/활성 지수를 계산하였다.  
4. K-Means 군집분석으로 지역 관광 유형을 구분하였다.  
5. Random Forest 회귀모형으로 관광지출액에 영향을 미치는 변수를 확인하였다.  
6. Folium과 Streamlit을 활용하여 지도와 대시보드를 구성하였다.


1. 读取旅游数据实验室 CSV 文件，并统一地区名称和列名。  
2. 整合访问人数、旅游支出额、搜索量和停留时间等指标。  
3. 使用 Min-Max 标准化计算旅游复苏/活跃度指数。  
4. 使用 K-Means 聚类划分地区旅游类型。  
5. 使用 Random Forest 回归模型分析影响旅游支出的主要因素。  
6. 使用 Folium 和 Streamlit 展示地图与前端页面。

---

## 10. 참고 문헌 및 코드 / 参考文献与代码

**참고 문헌 / 参考文献**

1. 전광상(2026), *내국인 관광 수요 분포의 복잡계적 구조 분석: 코로나19 이전･확산기･회복기 비교*  
   https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003315569

2. Yoo, Lee & Hong(2025), *Proximity, Resilience, and Blue Urbanism: Spatial Dynamics of Post-Pandemic Recovery in South Korea’s Coastal Fishing Communities*  
   https://www.mdpi.com/2073-445X/14/6/1303

**Code**  
https://github.com/ziqiaowang2-web/korea_tourism_recovery_project
