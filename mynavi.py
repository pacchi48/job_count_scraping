import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Chrome WebDriverのセットアップ
cService = webdriver.ChromeService(executable_path="venv/lib/python3.13/site-packages/chromedriver_binary/chromedriver")
driver = webdriver.Chrome(service=cService)

# 指定したURLにアクセス
driver.get('https://tenshoku.mynavi.jp/list/')

# 全てのクラス名を含むCSSセレクタを使ってボタンを見つける
button = driver.find_element(By.CSS_SELECTOR, ".btnAddS.js__jobCheckbox")
button.click()  # ボタンをクリック

time.sleep(2)  # 1秒間プログラムを停止

# アコーディオンのトリガー要素をすべて見つける
modal = driver.find_element(By.CSS_SELECTOR, ".modalChoice__content")
categories = modal.find_elements(By.CSS_SELECTOR, ".modalChoice__item")

data  =[]

for category in categories:
    # 大カテゴリ名
    l_cate = category.text

    # 大カテゴリをクリック
    category.click()

    # 画面遷移待機
    time.sleep(2)

    # 中カテゴリ群
    # element = modal.find_element(By.CSS_SELECTOR, '.js__selectCondition--large[style="display: block;"]')

    element = modal.find_element(By.XPATH, "//*[contains(@class, 'js__selectCondition--large') and not(contains(@style, 'display: none'))]")    
    sections = element.find_elements(By.TAG_NAME, 'section')

    for section in sections:
        m_el = section.find_element(By.CSS_SELECTOR, ".choiceContent__sectionTitle")
        # 中カテゴリ名
        m_cate = m_el.find_element(By.CLASS_NAME, 'checkbox__text').text

        # 小カテゴリ群
        s_elements = section.find_elements(By.CSS_SELECTOR, ".choiceContent__item")

        for s_el in s_elements:
           # 小カテゴリ名
           s_cate = s_el.find_element(By.CSS_SELECTOR, ".checkbox__text").text

           # チェックボックスをクリック
           s_el = s_el.find_element(By.TAG_NAME, "label")
           # 要素がビューポート中央に来るようにスクロール
           driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", s_el)
           s_el.click()

           # 内容を反映するボタンを押下
           ref_button = driver.find_element(By.CSS_SELECTOR, ".modalChoice__submit").find_element(By.CSS_SELECTOR, ".btnSecondaryL.js__modal--apply")
           ref_button.click()

           # 画面遷移待機
           time.sleep(1)

           # 件数取得
           count = driver.find_element(By.CSS_SELECTOR, ".btnSearch").find_element(By.CSS_SELECTOR, ".js__searchRecruit--count").text
           data.append([l_cate, m_cate, s_cate, count])

           # 職種ボタンを押下し、モーダルを開く
           button.click()

           time.sleep(2)  # 1秒間プログラムを停止

           # チェックボックスをクリック
           driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", s_el)
           s_el.click()

# DataFrameの作成
df = pd.DataFrame(data, columns=['L', 'M', 'S', 'Count'])

df_transposed = df.T

df_transposed.to_csv('./data/mynavi.csv', header=False, index=False)

# ドライバーを閉じる
driver.quit()