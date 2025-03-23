import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re  # 正規表現ライブラリをインポート
from selenium.webdriver.chrome.options import Options

# Chrome WebDriverのセットアップ
cService = webdriver.ChromeService()
driver = webdriver.Chrome(service=cService)

# 指定したURLにアクセス
driver.get('https://employment.en-japan.com/search/search_list/?occupation=101000&aroute=1')

# 全てのクラス名を含むCSSセレクタを使ってボタンを見つける
open_modal = driver.find_element(By.CSS_SELECTOR, ".addLink.reSelect")
open_modal.click()  # ボタンをクリック

time.sleep(3)

# もしくは、src属性で特定する場合
wait = WebDriverWait(driver, 10)
iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, '/search/modal_form_job/?dispsmall=1')]")))
driver.switch_to.frame(iframe)

time.sleep(1)

# アコーディオンのトリガー要素をすべて見つける
table = driver.find_element(By.ID, "modalFormBase")
categories = table.find_elements(By.CSS_SELECTOR, ".category")

data = []

for category in categories:
    # 大カテゴリ
    l_cate = category.find_element(By.TAG_NAME, 'span')
    l_cate_name = l_cate.text.replace("\n", "")
    class_name = l_cate.get_attribute('class')

    # 要素がビューポート中央に来るようにスクロール
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", category)
    category.click()
    time.sleep(1)

    # 法人営業のテキストを取得
    selectList = driver.find_element(By.CSS_SELECTOR, f".formList.{class_name}")
    sub_categories = selectList.find_elements(By.CSS_SELECTOR, ".subCategorySet")

    for sub in sub_categories:
        m_cate_el = sub.find_element(By.CSS_SELECTOR, ".subCategoryCheck")
        m_cate = m_cate_el.find_element(By.TAG_NAME, 'label').text.replace("\n", "")
        m_cate = re.sub(r'\(\d+件\)', '', m_cate)

        lists = sub.find_elements(By.CSS_SELECTOR, '.list:not(.emptyList)')

        for li in lists:
            s_cate = li.find_element(By.TAG_NAME, 'label').text.replace("\n", "")
            s_cate = re.sub(r'\(\d+件\)', '', s_cate)
            count_str = li.find_element(By.TAG_NAME, 'span').text

            count = int(re.sub(r'[()件,]', '', count_str))  # 件数から不要な文字を削除して整数に変換

            # カテゴリ名、サブカテゴリ名、件数をリストに追加
            data.append([l_cate_name, m_cate, s_cate, count])

# DataFrameの作成
df = pd.DataFrame(data, columns=['L', 'M', 'S', 'Job Count'])

df_transposed = df.T

df_transposed.to_csv('./data/en.csv', header=False, index=False)

# ドライバーを閉じる
driver.quit()

print('正常終了')