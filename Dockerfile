# ベースイメージ（python3.11-slim）
FROM python:3.11.9-slim-bookworm

# 作業ディレクトリを設定
WORKDIR /app

# 必要なLinuxパッケージをインストール
# - chromium & chromium-driver (Chrome相当＋ChromeDriver)
# - apt-get clean などでキャッシュを削除し、イメージサイズを抑える
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pythonパッケージのインストール
#  - Selenium
#  - rfcbibtex (もとの要件を維持)
RUN pip install --no-cache-dir selenium rfcbibtex

# Pythonスクリプトをコンテナにコピー（ファイル名は例）
COPY job_count.py /app/

# コンテナ起動時に実行するコマンド
# - "python job_count.py" でSeleniumスクリプトを走らせる想定
CMD ["python", "job_count.py"]
