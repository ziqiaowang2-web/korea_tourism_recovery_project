"""
Streamlit Dashboard for Korea Tourism Recovery Project
한국 지역별 관광 회복력 및 관광소비 불균형 분석 대시보드
韩国地区旅游复苏能力与旅游消费不均衡分析展示页面

使用方法 / 실행 방법:
1. pip install streamlit
2. streamlit run app.py

说明 / 설명:
本页面读取项目 outputs 和 data/processed 中已经生成的结果文件。
이 대시보드는 프로젝트의 outputs 및 data/processed 폴더에 생성된 결과 파일을 읽어 시각화합니다.
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components


# =========================
# 路径设置 / 경로 설정
# =========================
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUTS = PROJECT_ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
TABLES = OUTPUTS / "tables"
MAPS = OUTPUTS / "maps"
PROCESSED = PROJECT_ROOT / "data" / "processed"


# =========================
# 页面基础设置 / 페이지 기본 설정
# =========================
st.set_page_config(
    page_title="한국 지역별 관광 회복력 분석",
    page_icon="🇰🇷",
    layout="wide",
)


# =========================
# 工具函数 / 유틸리티 함수
# =========================
@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    """读取 CSV / CSV 파일 읽기"""
    return pd.read_csv(path, encoding="utf-8-sig")


def show_file_warning(path: Path, label: str):
    """文件不存在时显示提示 / 파일이 없을 때 안내 문구 표시"""
    if not path.exists():
        st.warning(f"缺少文件 / 파일 없음: {label}\n\n路径 / 경로: `{path}`")
        return True
    return False


def show_image(path: Path, caption: str = ""):
    """显示图片 / 이미지 표시"""
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.warning(f"图表文件不存在 / 그림 파일이 없습니다: `{path}`")


def format_large_number(value):
    """数字格式化 / 큰 숫자 포맷"""
    try:
        value = float(value)
    except Exception:
        return value

    if abs(value) >= 1_0000_0000_0000:
        return f"{value / 1_0000_0000_0000:.2f}조"
    if abs(value) >= 1_0000_0000:
        return f"{value / 1_0000_0000:.2f}억"
    if abs(value) >= 1_0000:
        return f"{value / 1_0000:.2f}만"
    return f"{value:,.0f}"


# =========================
# 侧边栏 / 사이드바
# =========================
st.sidebar.title("📌 Navigation / 메뉴")
page = st.sidebar.radio(
    "页面选择 / 페이지 선택",
    [
        "프로젝트 개요 / 项目概要",
        "전국 관광 추세 / 全国趋势",
        "지역별 불균형 / 地区不均衡",
        "군집분석 / 聚类分析",
        "모델 해석 / 模型解释",
        "관광 지도 / 旅游地图",
        "결론 / 结论",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Project**  
    한국 지역별 관광 회복력 및 관광소비 불균형 분석

    **Data Source**  
    Korea Tourism Data Lab
    """
)


# =========================
# 标题 / 제목
# =========================
st.title("한국 지역별 관광 회복력 및 관광소비 불균형 분석")
st.caption("관광 빅데이터 기반 지역 활성화 전략 제안 / 基于旅游大数据的区域活性化策略研究")


# =========================
# 页面 1：项目概要 / 프로젝트 개요
# =========================
if page == "프로젝트 개요 / 项目概要":
    st.header("1. 프로젝트 개요 / 项目概要")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(
            """
            본 프로젝트는 **Korea Tourism Data Lab**의 관광 빅데이터를 활용하여  
            2020년 이후 한국 관광 수요의 회복 추세와 2025년 지역별 관광소비 불균형을 분석합니다.

            本项目使用 **韩国旅游数据实验室 Korea Tourism Data Lab** 的旅游大数据，  
            分析 2020 年以后韩国旅游需求恢复趋势，以及 2025 年各地区旅游消费不均衡现象。
            """
        )

        st.subheader("연구 질문 / 研究问题")
        st.markdown(
            """
            1. 코로나19 이후 한국 관광 방문자 수와 관광지출액은 어떻게 변화했는가?  
               COVID-19 后韩国游客数量和旅游支出如何变化？
            2. 2025년 지역별 관광 회복/활성 수준은 어떻게 다른가?  
               2025 年各地区旅游复苏/活跃度有何差异？
            3. 관광소비는 특정 지역에 집중되어 있는가?  
               旅游消费是否集中在少数地区？
            4. 관광지출액에 영향을 미치는 주요 변수는 무엇인가?  
               影响旅游支出的主要因素是什么？
            """
        )

    with col2:
        st.subheader("분석 흐름 / 分析流程")
        st.markdown(
            """
            **데이터 수집 / 数据收集**  
            Korea Tourism Data Lab CSV

            **전처리 / 数据预处理**  
            컬럼 정리, 결측치 처리, 지표 통합

            **EDA / 探索性分析**  
            방문자 수, 관광지출액 추세 분석

            **모델링 / 建模**  
            K-Means 군집분석, Random Forest 회귀

            **결과 해석 / 结果解释**  
            지역 불균형과 활성화 전략 제안
            """
        )

    st.info(
        "이 대시보드는 이미 생성된 outputs 및 data/processed 결과 파일을 기반으로 표시됩니다. "
        "如果页面提示缺少文件，请先运行 src 中的数据处理脚本。"
    )


# =========================
# 页面 2：全国趋势 / 전국 관광 추세
# =========================
elif page == "전국 관광 추세 / 全国趋势":
    st.header("2. 전국 관광 추세 / 全国旅游趋势")

    trend_path = TABLES / "national_monthly_trend.csv"
    if not trend_path.exists():
        trend_path = PROCESSED / "national_monthly_real_trend.csv"

    if not show_file_warning(trend_path, "national_monthly_trend.csv 或 national_monthly_real_trend.csv"):
        trend = load_csv(trend_path)

        st.subheader("월별 방문자 수 추세 / Monthly Visitor Count Trend")
        show_image(FIGURES / "01_visitor_trend.png", "방문자 수 추세 / 访问人数趋势")

        st.subheader("월별 관광지출액 추세 / Monthly Tourism Spending Trend")
        show_image(FIGURES / "02_spending_trend.png", "관광지출액 추세 / 旅游支出趋势")

        st.subheader("전국 월별 데이터 / 全国月度数据")
        st.dataframe(trend, use_container_width=True)

        if "visitor_count" in trend.columns and "tourism_spending" in trend.columns:
            col1, col2, col3 = st.columns(3)

            first_visitor = trend["visitor_count"].iloc[0]
            last_visitor = trend["visitor_count"].iloc[-1]
            visitor_growth = (last_visitor - first_visitor) / first_visitor * 100

            first_spending = trend["tourism_spending"].iloc[0]
            last_spending = trend["tourism_spending"].iloc[-1]
            spending_growth = (last_spending - first_spending) / first_spending * 100

            col1.metric(
                "방문자 수 증가율 / 访问人数增长率",
                f"{visitor_growth:.1f}%",
                help="첫 월 대비 마지막 월 기준 / 首月到最后一月"
            )
            col2.metric(
                "관광지출액 증가율 / 旅游支出增长率",
                f"{spending_growth:.1f}%",
                help="첫 월 대비 마지막 월 기준 / 首月到最后一月"
            )
            col3.metric(
                "분석 월 수 / 分析月份数",
                f"{len(trend)}"
            )


# =========================
# 页面 3：地区不均衡 / 지역별 불균형
# =========================
elif page == "지역별 불균형 / 地区不均衡":
    st.header("3. 지역별 관광 회복/활성도 및 소비 불균형")

    summary_path = TABLES / "final_summary_table.csv"
    if not show_file_warning(summary_path, "final_summary_table.csv"):
        summary = load_csv(summary_path)

        st.subheader("지역별 관광 회복/활성 지수 / 地区旅游复苏/活跃度指数")
        show_image(FIGURES / "03_recovery_index_by_region.png", "지역별 관광 회복/활성 지수")

        st.subheader("지역별 관광지출액 / 地区旅游支出额")
        show_image(FIGURES / "04_spending_by_region.png", "지역별 관광지출액")

        st.subheader("최종 지역별 요약표 / 最终地区汇总表")

        display_df = summary.copy()
        for col in ["visitor_count", "tourism_spending", "destination_search"]:
            if col in display_df.columns:
                display_df[col + "_formatted"] = display_df[col].apply(format_large_number)

        st.dataframe(display_df, use_container_width=True)

        st.subheader("핵심 결과 / 核心结果")
        top5 = summary.sort_values("tourism_recovery_index", ascending=False).head(5)
        bottom5 = summary.sort_values("tourism_recovery_index", ascending=True).head(5)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Top 5 지역 / 前五地区**")
            st.dataframe(top5[["region", "tourism_recovery_index"]], use_container_width=True)

        with col2:
            st.markdown("**Bottom 5 지역 / 后五地区**")
            st.dataframe(bottom5[["region", "tourism_recovery_index"]], use_container_width=True)

        if "tourism_consumption_share" in summary.columns:
            seoul_gyeonggi = summary[summary["region"].isin(["서울특별시", "경기도"])]
            share = seoul_gyeonggi["tourism_consumption_share"].sum() * 100
            st.metric(
                "서울 + 경기 관광소비 비중 / 首尔+京畿旅游消费占比",
                f"{share:.1f}%"
            )


# =========================
# 页面 4：聚类分析 / 군집분석
# =========================
elif page == "군집분석 / 聚类分析":
    st.header("4. K-Means 군집분석 / K-Means 聚类分析")

    cluster_path = PROCESSED / "cluster_result.csv"
    profile_path = TABLES / "cluster_profile.csv"
    k_path = TABLES / "kmeans_k_selection.csv"

    col1, col2 = st.columns(2)

    with col1:
        show_image(FIGURES / "05_kmeans_silhouette.png", "K별 실루엣 점수 / Silhouette Score by K")

    with col2:
        show_image(FIGURES / "06_kmeans_elbow.png", "엘보우 방법 / Elbow Method")

    if not show_file_warning(k_path, "kmeans_k_selection.csv"):
        k_df = load_csv(k_path)
        st.subheader("K 선택 결과 / K 选择结果")
        st.dataframe(k_df, use_container_width=True)

    if profile_path.exists():
        st.subheader("군집별 평균 특성 / Cluster Profile")
        profile = load_csv(profile_path)
        st.dataframe(profile, use_container_width=True)

    if cluster_path.exists():
        st.subheader("지역별 군집 결과 / 地区聚类结果")
        cluster = load_csv(cluster_path)
        st.dataframe(cluster, use_container_width=True)

    st.markdown(
        """
        **해석 / 解释**  
        K-Means 결과에서 K=2의 실루엣 점수가 가장 높게 나타난 경우,  
        지역 관광 구조는 크게 `수도권 고활성·고소비 관광거점형`과 `일반 지역 관광형`으로 구분할 수 있습니다.

        如果 K=2 的轮廓系数最高，可以解释为：韩国地区旅游结构大致分为  
        `首都圈高活跃高消费旅游据点型` 和 `一般地区旅游型`。
        """
    )


# =========================
# 页面 5：模型解释 / 모델 해석
# =========================
elif page == "모델 해석 / 模型解释":
    st.header("5. 랜덤포레스트 회귀모형 및 변수 중요도")

    metrics_path = TABLES / "regression_metrics.csv"
    importance_path = TABLES / "feature_importance.csv"

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("변수 중요도 / Feature Importance")
        show_image(FIGURES / "07_feature_importance.png", "변수 중요도")

    with col2:
        st.subheader("실제값 vs 예측값 / Actual vs Predicted")
        show_image(FIGURES / "08_actual_vs_predicted.png", "실제값과 예측값 비교")

    if metrics_path.exists():
        st.subheader("모델 평가 지표 / 模型评价指标")
        metrics = load_csv(metrics_path)
        st.dataframe(metrics, use_container_width=True)

    if importance_path.exists():
        st.subheader("변수 중요도 표 / 特征重要度表")
        importance = load_csv(importance_path)
        st.dataframe(importance, use_container_width=True)

    st.warning(
        "분석 대상 지역 수가 17개로 제한되어 있으므로, 회귀모형은 고정밀 예측보다는 "
        "관광지출액 영향요인을 해석하기 위한 보조적 분석으로 활용하는 것이 적절합니다.\n\n"
        "由于地区样本数只有 17 个，回归模型更适合作为影响因素解释，而不是高精度预测模型。"
    )


# =========================
# 页面 6：地图 / 관광 지도
# =========================
elif page == "관광 지도 / 旅游地图":
    st.header("6. 관광 회복/활성 지도 / 旅游复苏活跃度地图")

    map_path = MAPS / "tourism_recovery_map.html"

    if not show_file_warning(map_path, "tourism_recovery_map.html"):
        html = map_path.read_text(encoding="utf-8")
        components.html(html, height=720, scrolling=True)

    st.markdown(
        """
        지도 원의 크기는 관광 회복/활성 지수에 따라 표시됩니다.  
        원을 클릭하면 해당 지역의 방문자 수, 관광지출액, 검색건수, 군집 결과를 확인할 수 있습니다.

        地图中圆点大小代表旅游复苏/活跃度指数。  
        点击圆点可以查看该地区访问人数、旅游支出、搜索量和聚类结果。
        """
    )


# =========================
# 页面 7：结论 / 결론
# =========================
elif page == "결론 / 结论":
    st.header("7. 결론 및 지역 활성화 전략 / 结论与区域活性化策略")

    st.subheader("주요 결론 / 主要结论")
    st.markdown(
        """
        1. **전국 관광 수요는 2020년 이후 지속적으로 회복되는 추세를 보였다.**  
           全国旅游需求自 2020 年后整体持续恢复。

        2. **관광 회복/활성 수준은 수도권과 주요 관광 거점 지역에 집중되었다.**  
           旅游复苏/活跃度集中在首都圈和主要旅游据点地区。

        3. **관광소비는 서울특별시와 경기도에 강하게 집중되었다.**  
           旅游消费高度集中于首尔和京畿道。

        4. **목적지 검색건수와 방문자 수는 관광지출액과 밀접한 관련이 있었다.**  
           目的地搜索量和访问人数与旅游支出密切相关。

        5. **지역 관광 불균형 완화를 위해 지방 관광지의 검색수요 확대와 체류형 관광 전략이 필요하다.**  
           为缓解地区旅游不均衡，需要提升地方旅游地搜索需求，并发展停留型旅游。
        """
    )

    st.subheader("정책 제안 / 政策建议")
    st.markdown(
        """
        - **수도권 집중 완화 / 缓解首都圈集中**  
          지방 관광 콘텐츠와 교통 접근성을 강화해야 한다.

        - **체류형 관광 활성화 / 发展停留型旅游**  
          숙박, 야간 관광, 지역 축제와 연계한 체류형 상품 개발이 필요하다.

        - **디지털 검색수요 확대 / 扩大数字搜索需求**  
          목적지 검색건수가 중요한 변수로 나타났으므로, 지역 관광지의 온라인 노출을 강화해야 한다.

        - **쇼핑 중심 관광에서 지역문화 관광으로 확장 / 从购物型旅游扩展到地方文化旅游**  
          대형 쇼핑시설 중심의 관광 수요를 지역 문화·자연·역사 자원으로 분산할 필요가 있다.
        """
    )

    summary_path = OUTPUTS / "final_output_summary.md"
    if summary_path.exists():
        st.subheader("자동 생성 요약 / 自动生成摘要")
        st.markdown(summary_path.read_text(encoding="utf-8"))
