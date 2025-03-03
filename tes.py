import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1) Chrome を初期化
# DRIVER_PATH は環境に依存します。

cService = webdriver.ChromeService(executable_path="venv/lib/python3.13/site-packages/chromedriver_binary/chromedriver")
driver = webdriver.Chrome(service=cService)

# 2) Google のページを開く
driver.get('https://www.google.com')

#### Fig.1

# 3) ページが完全に読み込まれるまで待つ
time.sleep(3)

# 4) 検索ボックスのオブジェクトを取得
q = driver.find_element(By.NAME, 'q')

# 5) 検索ボックスにキーを送信
q.send_keys('ゼロからはじめるPython')

#### Fig.2

# 6) フォームを送信
q.submit()

# 7) 10秒待つ
time.sleep(10)

#### Fig.3

# 8) ドライバを終了
driver.quit()
