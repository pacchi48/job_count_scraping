import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re  # 正規表現ライブラリをインポート
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# Chromeオプションを設定
options = Options()

# ボット検出回避のためのオプション
options.add_argument("--disable-blink-features=AutomationControlled")  # Selenium検出防止
options.add_argument("--start-maximized")  # ウィンドウを最大化
options.add_argument("--disable-popup-blocking")  # ポップアップを無効化
options.add_argument("--disable-infobars")  # "Chromeは自動テスト ソフトウェアによって制御されています" を非表示

# User-Agentの偽装（ランダムな値を入れるとより効果的）
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")

# # Chrome DevTools Protocol (CDP) を利用して自動化フラグを無効化
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#             get: () => undefined
#         })
#     """
# })

# Chrome WebDriverのセットアップ
cService = webdriver.ChromeService()
driver = webdriver.Chrome(service=cService, options=options)

# 指定したURLにアクセス
driver.get('https://doda.jp/DodaFront/View/JobSearchList/')

# JavaScriptを使って navigator.webdriver を偽装
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# ページが完全にロードされるのを待つ
WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
)

data = []

# 職種ボタン
job_buttom = driver.find_element(By.CSS_SELECTOR, ".Button-module_button--sizeXS__FC1is.Button-module_button--grayLine__4qEY4.Button-module_button--width100__W-pdV.select-button")
job_buttom.click()

wait = WebDriverWait(driver, 10)
scroll_areas = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".modalSimpleBar")))

scroll_areas = driver.find_elements(By.CSS_SELECTOR, ".modalSimpleBar")
l_categories = scroll_areas[0].find_elements(By.TAG_NAME, 'li')

for l_cate in l_categories:
    # カテゴリをクリック
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", l_cate)
    l_cate.click()

    l_cate_name = l_cate.find_element(By.CSS_SELECTOR, '.occupationCategoryItem__title.occupationCategoryItem__title--selected').text

    # アクティブな中カテゴリを取得
    scroll_areas = driver.find_elements(By.CSS_SELECTOR, ".modalSimpleBar")[1]
    m_cate_els = driver.find_elements(By.CSS_SELECTOR, ".checkboxItemM")

    for m_cate in m_cate_els:
        # 中カテゴリ名
        m_cate_val = m_cate.find_element(By.CSS_SELECTOR, '.checkboxItemM__title').text
        count_element = m_cate.find_element(By.CSS_SELECTOR, ".checkboxItemM__numberOfJobs").text
        m_cate_name = m_cate_val.replace(count_element, "").strip()

        # 小カテゴリ群
        s_cate_els = m_cate.find_elements(By.CSS_SELECTOR, '.checkboxItemS')
        for s_cate in s_cate_els:
            # 小カテゴリ名
            s_cate_name = s_cate.find_element(By.CSS_SELECTOR, '.checkboxItemS__title').text
            # 小カテゴリ数
            s_cate_count = s_cate.find_element(By.CSS_SELECTOR, '.checkboxItemS__numberOfJobs').text
            s_cate_name = s_cate_name.replace(s_cate_count, "").strip()

            count = int(re.sub(r'[(),]', '', s_cate_count))

            # データを追加
            data.append([l_cate_name, m_cate_name, s_cate_name, count])

# DataFrameの作成
df = pd.DataFrame(data, columns=['L', 'M', 'S', 'count'])

df_transposed = df.T

df_transposed.to_csv('./data/doda.csv', header=False, index=False)

driver.quit()

print('正常終了')