"""
可选 API 下载模板 / 선택적 API 다운로드 템플릿

中文：
data.go.kr 或 KOSIS 的 OpenAPI 通常需要申请 API Key。
本脚本只提供模板，实际 endpoint 和参数需要根据数据页面说明修改。

한국어:
data.go.kr 또는 KOSIS OpenAPI는 보통 API Key 신청이 필요합니다.
본 스크립트는 템플릿이며, 실제 endpoint와 파라미터는 데이터 페이지 설명에 맞게 수정해야 합니다.
"""

import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from utils import DATA_RAW, save_csv

load_dotenv()

# .env 파일에서 API Key 불러오기 / 从 .env 文件读取 API Key
DATA_GO_KR_KEY = os.getenv("DATA_GO_KR_KEY", "")
KOSIS_KEY = os.getenv("KOSIS_KEY", "")


def download_json_api(url: str, params: dict, output_csv: Path) -> pd.DataFrame:
    """
    JSON API를 호출하고 결과를 CSV로 저장합니다.
    调用 JSON API 并将结果保存为 CSV。
    """
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    data = response.json()

    # 일반적인 공공데이터 응답 구조를 순서대로 탐색
    # 按常见公共数据 API 结构依次寻找 records
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        records = None
        key_paths = [
            ["response", "body", "items", "item"],
            ["response", "body", "items"],
            ["body", "items"],
            ["items"],
            ["data"],
        ]

        for key_path in key_paths:
            obj = data
            for key in key_path:
                if isinstance(obj, dict) and key in obj:
                    obj = obj[key]
                else:
                    obj = None
                    break

            if obj is not None:
                records = obj
                break

        if records is None:
            df = pd.json_normalize(data)
        else:
            df = pd.json_normalize(records)

    save_csv(df, output_csv)
    return df


def example_data_go_kr_download():
    """
    data.go.kr 다운로드 예시 / data.go.kr 下载示例
    """
    if not DATA_GO_KR_KEY:
        print("DATA_GO_KR_KEY가 없습니다. .env 파일에 Key를 입력하세요.")
        print("未找到 DATA_GO_KR_KEY。请在 .env 文件中填写 Key。")
        return

    # 실제 API 주소로 교체 필요 / 需要替换成真实 API 地址
    url = "https://apis.data.go.kr/REPLACE_WITH_REAL_ENDPOINT"

    params = {
        "serviceKey": DATA_GO_KR_KEY,
        "pageNo": 1,
        "numOfRows": 1000,
        "type": "json",
    }

    output_csv = DATA_RAW / "api" / "data_go_kr_result.csv"
    download_json_api(url, params, output_csv)


def example_kosis_download():
    """
    KOSIS 다운로드 예시 / KOSIS 下载示例
    """
    if not KOSIS_KEY:
        print("KOSIS_KEY가 없습니다. .env 파일에 Key를 입력하세요.")
        print("未找到 KOSIS_KEY。请在 .env 文件中填写 Key。")
        return

    url = "https://kosis.kr/openapi/Param/statisticsParameterData.do"

    params = {
        "method": "getList",
        "apiKey": KOSIS_KEY,
        "format": "json",
        "jsonVD": "Y",
        "userStatsId": "REPLACE_WITH_USER_STATS_ID",
        "prdSe": "Y",
        "startPrdDe": "2020",
        "endPrdDe": "2025",
    }

    output_csv = DATA_RAW / "kosis" / "kosis_result.csv"
    download_json_api(url, params, output_csv)


if __name__ == "__main__":
    print("이 스크립트는 API 다운로드 템플릿입니다.")
    print("这是 API 下载模板。")
    print("Korea Tourism Data Lab CSV를 수동 다운로드했다면 이 파일은 실행하지 않아도 됩니다.")
    print("如果已经手动下载 Korea Tourism Data Lab CSV，可以跳过本脚本。")
