# 双语注释版 src 脚本说明 / 이중언어 주석 버전 src 스크립트 설명

把本压缩包里的 `src` 文件夹复制到你的项目根目录：

```text
E:\PythonProject\korea_tourism_recovery_project\
```

覆盖原来的 `src` 文件夹即可。

실제 Korea Tourism Data Lab CSV 파일을 사용하는 경우 실행 순서는 다음과 같습니다:

```bash
python src/02_load_datalab_real_files.py
python src/03_clean_merge_data_v2.py
python src/04_eda_visualization.py
python src/05_clustering_model.py
python src/06_regression_model.py
python src/07_make_final_outputs.py
```

或者直接运行：

```bash
run_real_data.bat
```

真实数据文件放在：

```text
data/raw/datalab/
```

演示数据文件 `sample_korea_tourism_datalab.csv` 建议删除。
