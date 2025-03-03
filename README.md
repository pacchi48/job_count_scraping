# job_count_scraping
求人サイトからカテゴリ別に求人数を取得し、csvに出力する


# 手順

1. pythonをインストール

    公式サイトから最新版をダウンロード
    https://www.python.org/downloads/

    インストール後にターミナルを開いて
    
    ```
    python -v
    ```

    でインストールされているかを確認

    参考サイト：https://qiita.com/yoshi-kin/items/e0a7336a288188913097

2. seleniumをインストール

    ターミナルを開いて

    ```
    pip install selenium
    ```

3. chromeのドライバーをインストール

    chromeのバージョンを確認。

    確認方法
    https://mhtdesign.net/guide/version-confirmation.html

    ```
    # 94のところをchromeのバージョンにする
    pip install chromedriver-binary==94.*
    ```
4. 各pythonファイルを実行する。

5. data配下にcsvが出力されるので、それをスプレッドシートにインポート
