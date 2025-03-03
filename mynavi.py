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
driver.get('https://tenshoku.mynavi.jp/')

# 全てのクラス名を含むCSSセレクタを使ってボタンを見つける
button = driver.find_element(By.CSS_SELECTOR, ".topSearchPanel.renew.js__slideTrigger--jobtop")
button.click()  # ボタンをクリック

# # ページが完全に読み込まれるのを待つ
# WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, 'navItemList__item'))
# )

time.sleep(1)  # 1秒間プログラムを停止

# アコーディオンのトリガー要素をすべて見つける
triggers = driver.find_elements(By.CSS_SELECTOR, ".js__accordion--trigger")

print(len(triggers))

# それぞれのトリガーをクリックしてアコーディオンを展開
for trigger in triggers:
    # 親要素（.toggle）を取得し、`data-large-nm` 属性があるか確認
    parent_div = trigger.find_element(By.XPATH, "./ancestor::div[contains(@class, 'toggle')]")
    if parent_div.get_attribute("data-large-nm"):
        trigger.click()
        time.sleep(1)  # 各クリックの間に少し待つ

# データの抽出
data = []
categories = driver.find_elements(By.CSS_SELECTOR, ".js__sliedeSearch--large")
for category in categories:
    category_name = category.find_element(By.CSS_SELECTOR, ".text").text
    items = category.find_elements(By.CSS_SELECTOR, ".checkBoxList__item")
    for item in items:
        job_title = item.find_element(By.CSS_SELECTOR, ".checkBoxList__text").text
        job_count = item.find_element(By.CSS_SELECTOR, ".textCaution").text.replace('件', '').replace(',', '')
        data.append([category_name, job_title, int(job_count)])

# DataFrameの作成
df = pd.DataFrame(data, columns=['Category', 'Job Title', 'Job Count'])

df_transposed = df.T

df_transposed.to_csv('mynavi.csv', header=False, index=False)

# # DataFrameを整理
# final_data = {}
# for _, row in df.iterrows():
#     category = row['Category']
#     if category not in final_data:
#         final_data[category] = {'Titles': [], 'Counts': []}
#     final_data[category]['Titles'].append(row['Job Title'])
#     final_data[category]['Counts'].append(row['Job Count'])

# # 新しいDataFrameの作成
# categories = list(final_data.keys())
# titles = [title for category in categories for title in final_data[category]['Titles']]
# counts = [count for category in categories for count in final_data[category]['Counts']]
# new_df = pd.DataFrame({
#     'Category': categories * len(final_data[categories[0]]['Titles']),
#     'Job Title': titles,
#     'Job Count': counts
# })

# # 正しく整形されたDataFrameをCSVに出力
# new_df.to_csv('formatted_mynavi.csv', index=False)

# print(new_df)

# ドライバーを閉じる
driver.quit()