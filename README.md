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
4. run_all.pyを実行する。

    ```
    pythonのpath run_all.pyのpath

    例
    /Users/yu-suzuki/Project/job_count_csv/venv/bin/python /Users/yu-suzuki/Project/j
ob_count_csv/run_all.py
    ```

5. data配下にcsvが出力されるので、それをスプレッドシートにインポート


## 備考

### 注意点
run_all.pyが実行時間30分~1時間ほどかかる。
ディスプレイがスリープになったら中断されるので、要設定。かつCPUも食うかもしれないので、他作業がない時にでも実行推奨。

失敗の際は正常終了が出力されないので、そこでエラーを確認。

chromeをアップデートするとdriverと差異が出て動かなくなる可能性あり、その場合は更新したバージョンのdriverを再度インストールする必要。