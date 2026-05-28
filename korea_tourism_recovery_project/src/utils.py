"""
공통 유틸리티 함수 / 通用工具函数

이 파일은 전체 프로젝트에서 반복적으로 사용하는 경로, 파일 읽기, 컬럼명 정규화,
지역명 통일, 저장 함수를 제공합니다.

本文件提供整个项目中反复使用的路径、文件读取、列名标准化、
地区名称统一和保存函数。
"""

from pathlib import Path
import pandas as pd
import numpy as np

# 프로젝트 루트 경로 / 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# 데이터 및 결과 폴더 경로 / 数据和输出文件夹路径
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS = PROJECT_ROOT / "outputs"
FIGURES = OUTPUTS / "figures"
TABLES = OUTPUTS / "tables"
MAPS = OUTPUTS / "maps"

# 필요한 폴더가 없으면 자동 생성 / 如果必要文件夹不存在则自动创建
for path in [DATA_RAW, DATA_PROCESSED, OUTPUTS, FIGURES, TABLES, MAPS]:
    path.mkdir(parents=True, exist_ok=True)


def read_table(path: Path) -> pd.DataFrame:
    """
    CSV 또는 Excel 파일을 읽습니다.
    读取 CSV 或 Excel 文件。

    한국어 CSV는 보통 utf-8-sig, cp949, euc-kr 인코딩이 섞여 있기 때문에
    여러 인코딩을 순서대로 시도합니다.

    韩文 CSV 经常混用 utf-8-sig、cp949、euc-kr 编码，
    因此这里会按顺序尝试多种编码。
    """
    path = Path(path)
    suffix = path.suffix.lower()

    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)

    encodings = ["utf-8-sig", "utf-8", "cp949", "euc-kr"]
    last_error = None

    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception as exc:
            last_error = exc

    raise RuntimeError(f"Cannot read file: {path}. Last error: {last_error}")


def normalize_column_name(col: str) -> str:
    """
    관광데이터랩/KOSIS에서 내려받은 컬럼명을 프로젝트 표준 컬럼명으로 변환합니다.
    将旅游数据实验室/KOSIS 下载数据的列名转换为项目标准列名。
    """
    col = str(col).strip().replace("\n", " ").replace("\r", " ")
    compact = col.replace(" ", "")

    mapping = {
        # 지역 / 地区
        "지역": "region",
        "시도": "region",
        "시도명": "region",
        "광역지자체": "region",
        "광역시도": "region",

        # 날짜 / 日期
        "기준년월": "date",
        "기준연월": "date",
        "년월": "date",
        "연월": "date",
        "날짜": "date",

        # 방문자 / 游客
        "방문자수": "visitor_count",
        "방문자 수": "visitor_count",
        "전년동기방문자수": "visitor_count_prev",
        "전년동기 방문자수": "visitor_count_prev",
        "방문자수증감률": "visitor_growth_rate",
        "방문자수 증감률": "visitor_growth_rate",
        "순방문자수": "unique_visitors",
        "순 방문자 수": "unique_visitors",

        # 관광 소비 / 旅游消费
        "관광지출액": "tourism_spending",
        "관광 지출액": "tourism_spending",
        "관광소비": "tourism_spending",
        "관광소비액": "tourism_spending",
        "관광 소비액": "tourism_spending",
        "전년도관광지출액": "tourism_spending_prev_year",
        "전년도 관광지출액": "tourism_spending_prev_year",
        "전년동기관광지출액": "tourism_spending_prev",
        "전년동기 관광지출액": "tourism_spending_prev",
        "관광지출액증감률": "spending_growth_rate",
        "관광지출액 증감률": "spending_growth_rate",

        # 검색 / 搜索
        "검색건수": "destination_search",
        "목적지검색건수": "destination_search",
        "목적지 검색건수": "destination_search",
        "목적지검색량": "destination_search",
        "목적지 검색량": "destination_search",

        # 체류 / 停留
        "평균체류시간": "avg_stay_time",
        "평균 체류시간": "avg_stay_time",
        "평균숙박일수": "avg_lodging_days",
        "평균 숙박일수": "avg_lodging_days",
        "평균숙박일": "avg_lodging_days",
        "평균 숙박일": "avg_lodging_days",
        "숙박방문자비율": "lodging_visitor_ratio",
        "숙박 방문자 비율": "lodging_visitor_ratio",

        # 기타 / 其他
        "증가율(%)": "visitor_increase_rate_top",
        "순위": "rank",
        "관광지명": "attraction_name",
        "중분류": "category_mid",
        "소분류": "category_small",
        "주소": "address",
        "인구": "population",
        "총인구": "population",
        "GRDP": "grdp",
        "grdp": "grdp",
    }

    return mapping.get(col, mapping.get(compact, col))


def standardize_region_name(region: str) -> str:
    """
    지역명을 17개 광역시도 표준명으로 통일합니다.
    将地区名称统一为韩国 17 个广域市道标准名称。
    """
    if pd.isna(region):
        return region

    region = str(region).strip()

    mapping = {
        "서울": "서울특별시",
        "서울시": "서울특별시",
        "서울특별시": "서울특별시",
        "부산": "부산광역시",
        "부산시": "부산광역시",
        "대구": "대구광역시",
        "대구시": "대구광역시",
        "인천": "인천광역시",
        "인천시": "인천광역시",
        "광주": "광주광역시",
        "광주시": "광주광역시",
        "대전": "대전광역시",
        "대전시": "대전광역시",
        "울산": "울산광역시",
        "울산시": "울산광역시",
        "세종": "세종특별자치시",
        "세종시": "세종특별자치시",
        "경기": "경기도",
        "강원": "강원특별자치도",
        "강원도": "강원특별자치도",
        "충북": "충청북도",
        "충남": "충청남도",
        "전북": "전북특별자치도",
        "전라북도": "전북특별자치도",
        "전남": "전라남도",
        "경북": "경상북도",
        "경남": "경상남도",
        "제주": "제주특별자치도",
        "제주도": "제주특별자치도",
    }

    return mapping.get(region, region)


def parse_month(value):
    """
    다양한 날짜 표현을 pandas 월 단위 날짜로 변환합니다.
    将多种日期格式转换为 pandas 月度日期。
    """
    if pd.isna(value):
        return pd.NaT

    text = str(value).strip().replace(".", "-").replace("/", "-")

    # 예: 202501 -> 2025-01-01 / 例如：202501 -> 2025-01-01
    if len(text) == 6 and text.isdigit():
        text = f"{text[:4]}-{text[4:6]}-01"
    elif len(text) == 7:
        text = f"{text}-01"

    try:
        return pd.to_datetime(text).to_period("M").to_timestamp()
    except Exception:
        return pd.NaT


def clean_numeric(series: pd.Series) -> pd.Series:
    """
    쉼표, 퍼센트, 공백이 포함된 숫자형 문자열을 숫자로 변환합니다.
    将包含逗号、百分号和空格的数字字符串转换为数值。
    """
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip(),
        errors="coerce"
    )


def minmax(series: pd.Series) -> pd.Series:
    """
    0~1 Min-Max 정규화를 수행합니다.
    执行 0~1 Min-Max 标准化。
    """
    series = pd.to_numeric(series, errors="coerce")
    min_v = series.min()
    max_v = series.max()

    if pd.isna(min_v) or pd.isna(max_v) or max_v == min_v:
        return pd.Series(0.0, index=series.index)

    return (series - min_v) / (max_v - min_v)


def save_csv(df: pd.DataFrame, path: Path):
    """
    CSV 파일을 utf-8-sig 인코딩으로 저장합니다.
    使用 utf-8-sig 编码保存 CSV，方便 Excel 正常显示中文/韩文。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"[SAVE] {path}")
