import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re  # 正規表現ライブラリをインポート
from selenium.webdriver.chrome.options import Options

# モバイルエミュレーションの設定
mobile_emulation = {
    "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}

chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

# Chrome WebDriverのセットアップ
cService = webdriver.ChromeService(executable_path="venv/lib/python3.13/site-packages/chromedriver_binary/chromedriver")
driver = webdriver.Chrome(service=cService, options=chrome_options)

# 指定したURLにアクセス
driver.get('https://employment.en-japan.com/')

# 全てのクラス名を含むCSSセレクタを使ってボタンを見つける
button = driver.find_element(By.CSS_SELECTOR, ".md_btn.md_btn--white.md_btn--job.job.js_uiViewSegue")
button.click()  # ボタンをクリック

time.sleep(3)  # 1秒間プログラムを停止

# アコーディオンのトリガー要素をすべて見つける
triggers = driver.find_elements(By.CSS_SELECTOR, ".js_area_div")

# それぞれのトリガーをクリックしてアコーディオンを展開
for trigger in triggers:
    # 要素がビューポート中央に来るようにスクロール
    driver.execute_script("arguments[0].scrollIntoView(true);", trigger)
    time.sleep(1)
    # 要素が表示されているか確認し、クリック可能であればクリック
    if trigger.is_displayed() and trigger.is_enabled():
        # 要素を探し、削除する
        element_to_remove = driver.find_element(By.ID, "stickyUnit2")
        driver.execute_script("arguments[0].remove();", element_to_remove)
        trigger.click()
    else:
        print("Element not interactable:", trigger.text)

time.sleep(3)

# データの抽出
data = []

# 大カテゴリの要素を取得
main_categories = driver.find_elements(By.CSS_SELECTOR, ".js_area_div")

for main_category in main_categories:
    # '営業系' のテキストを持つ直接の span 要素を探すための XPath を調整
    category_name = main_category.find_element(By.CSS_SELECTOR, ".md_accordionTrigger.js_title.be_open").text
    # 括弧より前のテキストを抽出
    category_name = category_name.split('(')[0].strip()

    # 同じ親要素の中からサブカテゴリを持つdivを取得
    sub_categories_class = main_category.find_element(By.CSS_SELECTOR, ".jsSubCategoryDiv.js_checkboxes")
    sub_categories = sub_categories_class.find_elements(By.CSS_SELECTOR, ".md_checkUnit.jsSubCategoryCheck.js_accordion.js_checkboxUnit.js_pref_div")

    for sub_category in sub_categories:
        # サブカテゴリのタイトルと件数を取得
        job_title = sub_category.find_element(By.CSS_SELECTOR, ".jsList.js_pref_title").text
        job_count_text = sub_category.find_element(By.CSS_SELECTOR, "span.num").text  # 件数を含むテキスト
        job_count = int(re.sub(r'[()件,]', '', job_count_text))  # 件数から不要な文字を削除して整数に変換

        # カテゴリ名、サブカテゴリ名、件数をリストに追加
        data.append([category_name, job_title, job_count])

# DataFrameの作成
df = pd.DataFrame(data, columns=['Category', 'Job Title', 'Job Count'])

df_transposed = df.T

df_transposed.to_csv('./data/en.csv', header=False, index=False)

# ドライバーを閉じる
driver.quit()