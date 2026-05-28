# 韩国地区旅游复苏能力与旅游消费不均衡分析

中文题目：韩国地区旅游复苏能力与旅游消费不均衡分析：基于旅游大数据的区域活性化策略研究  
韩文题目：한국 지역별 관광 회복력 및 관광소비 불균형 분석: 관광 빅데이터 기반 지역 활성화 전략 제안

## 1. 项目说明

本项目用于“大数据分析”期末项目。代码支持两种运行方式：

1. **真实数据模式**：把韩国旅游数据实验室、data.go.kr、KOSIS 下载的数据放入 `data/raw/`，脚本会自动清洗、合并、分析。
2. **演示数据模式**：如果暂时没有真实数据，运行 `src/00_generate_sample_data.py` 会生成一份结构相似的模拟数据，用于测试完整流程。

建议最终提交时使用真实数据，并在报告中说明数据来源。

## 2. 推荐数据来源

### Korea Tourism Data Lab
建议手动下载 CSV/Excel 后放入：

```text
data/raw/datalab/
```

可用字段方向：
- 방문자 수 / visitor_count
- 관광소비 / tourism_spending
- 평균 체류시간 / avg_stay_time
- 평균 숙박일 / avg_lodging_days
- 목적지 검색량 / destination_search
- 숙박방문자 비율 / lodging_visitor_ratio

### data.go.kr OpenAPI / KOSIS OpenAPI
如已申请 API key，可以把 `.env.template` 复制为 `.env` 后填写 key。

## 3. PyCharm 运行步骤

1. 在 PyCharm 新建 Pure Python 项目。
2. 建议路径，例如：`E:\pythonProject\korea_tourism_recovery_project`
3. 解释器建议选择：项目 venv → virtualenv → Python 3.10、3.11、3.12 或 3.13。
4. 创建项目后，把本压缩包解压到项目目录。
5. 打开 PyCharm 终端，执行：
   ```bash
   pip install -r requirements.txt
   ```
6. 没有真实数据时，先执行：
   ```bash
   python src/00_generate_sample_data.py
   ```
7. 然后按顺序执行：
   ```bash
   python src/02_load_datalab_files.py
   python src/03_clean_merge_data.py
   python src/04_eda_visualization.py
   python src/05_clustering_model.py
   python src/06_regression_model.py
   python src/07_make_final_outputs.py
   ```

也可以双击或在终端运行：
```bash
run_all.bat
```

## 4. 输出结果

运行完成后，结果会保存在：

```text
outputs/figures/
outputs/tables/
outputs/maps/
data/processed/
```
