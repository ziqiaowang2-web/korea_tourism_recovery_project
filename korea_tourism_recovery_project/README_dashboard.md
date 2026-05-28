# Streamlit Dashboard 使用说明 / 실행 안내

把本压缩包中的文件复制到你的项目根目录：

```text
E:\PythonProject\korea_tourism_recovery_project\
```

复制后项目结构应类似：

```text
korea_tourism_recovery_project/
├─ app.py
├─ run_dashboard.bat
├─ src/
├─ data/
├─ outputs/
└─ requirements.txt
```

## 1. 安装 Streamlit / Streamlit 설치

在 PyCharm 终端运行：

```bash
pip install streamlit
```

或者把下面这一行追加到 `requirements.txt`：

```text
streamlit>=1.30.0
```

## 2. 启动页面 / 대시보드 실행

方法一：

```bash
streamlit run app.py
```

方法二：双击运行：

```text
run_dashboard.bat
```

## 3. 注意 / 주의

页面会读取以下文件夹中的结果：

```text
outputs/figures/
outputs/tables/
outputs/maps/
data/processed/
```

如果页面提示缺少文件，请先运行 `src` 里的分析脚本生成结果。
