import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re  # 正規表現ライブラリをインポート
from selenium.webdriver.chrome.options import Options
import sys

#モバイルエミュレーションの設定
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
driver.get('https://woman-type.jp/job-search/?routeway=82')

# data-target が job-selection-content の a 要素を取得する
element = driver.find_element(
        By.CSS_SELECTOR, 
        "a.js-toggle.link-button.-type04.-left[href='#hope-job']"
    )
element.click()

time.sleep(3)  # 1秒間プログラムを停止

data = []

try:
    # --- 1) 最初に、既にチェックの入っているチェックボックスを解除 ---
    # すでに checked が入っている input[type='checkbox'] をすべて取得
    modal = driver.find_elements(By.ID, "hope-job")
    accordion_areas = modal[0].find_elements(By.CSS_SELECTOR, ".accordion-area")

    for area in accordion_areas:
        # 大カテゴリ
        title = area.find_elements(By.CSS_SELECTOR, ".accordion-title")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title[0])
        title[0].click()
        l_cate = title[0].text

        # listを取得
        accordion_div = area.find_element(By.CSS_SELECTOR, "div.accordion-inner")
        li_elements = accordion_div.find_elements(By.TAG_NAME, "li")

        for li_el in li_elements[1:]:
            # チェックボックスがチェック
            label_element = li_el.find_element(By.TAG_NAME, "label")
            # 要素がビューポート中央に来るようにスクロール
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label_element)
            # driver.execute_script("arguments[0].scrollIntoView(true);", label_element)
            label_element.click()

            # 中カテゴリ
            m_cate = label_element.text

            time.sleep(1)  # 1秒間プログラムを停止

            # 追加ボタンをクリック
            add_button = driver.find_element(
                By.CSS_SELECTOR,
                "a.js-toggle-close.link-button.-type02[href='#hope-job']"
            )
            add_button.click()

            time.sleep(1)  # 1秒間プログラムを停止

            # 結果件数
            count_elem = driver.find_element(By.CSS_SELECTOR, "div.result span.count")
            count_value = count_elem.text

            # dataの追加
            data.append((l_cate, m_cate, count_value))

            # 職種を追加を押下
            element = driver.find_element(
                    By.CSS_SELECTOR, 
                    "a.js-toggle.link-button.-type04.-left[href='#hope-job']"
                )
            element.click()

            time.sleep(1)  # 1秒間プログラムを停止

            # チェックを外す
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", label_element)
            label_element.click()

            time.sleep(1)  # 1秒間プログラムを停止
            
except Exception as e:
    print("An error occurred:", e)
    sys.exit(1)  # スクリプト終了(終了コード1)
    

# DataFrameの作成
df = pd.DataFrame(data, columns=['Category', 'Job Title', 'Job Count'])

df_transposed = df.T

df_transposed.to_csv('./data/onnna.csv', header=False, index=False)

# ドライバーを閉じる
driver.quit()