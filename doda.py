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
driver.get('https://doda.jp/')


# ページが完全にロードされるのを待つ
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
)

try:
    # '職種'テキストを含むリンクを検索しクリック
    job_type_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'searchType__item')]//a[.//span[contains(text(), '職種')]]"))
    )
    job_type_link.click()
    time.sleep(5)
except TimeoutException:
    print("指定された要素が見つからないか、クリック可能な状態になりません。")

try:
    # modal__searchContent--active クラス内のすべての accordion__item 要素を見つける
    triggers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".modal__searchContent--active .accordion__item")
        )
    )

    print(len(triggers))
    
    # 各要素に対する操作
    for trigger in triggers:
        # 要素がビューポート中央に来るようにスクロール
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", trigger)
        
        time.sleep(3)

        # 要素が表示されているか確認し、クリック可能であればクリック
        if trigger.is_displayed() and trigger.is_enabled():
            trigger.click()
        else:
            print("Element not interactable:", trigger.text)

except Exception as e:
    print("An error occurred:", e)

data = []
try:
    elements = driver.find_elements(By.CSS_SELECTOR, ".accordion__content--open")
    print(len(elements))

    for element in elements:
        # 各accordion__content--openの中の項目を取得
        listItems = element.find_elements(By.CSS_SELECTOR, ".accordion__item")
        if listItems:
            # 最初の要素（大カテゴリ）を取得
            main_category = listItems[0].find_element(By.CSS_SELECTOR, "span:nth-of-type(2)").text

            for listItem in listItems[1:]:  # 最初の要素をスキップ
                sub_category_text = listItem.find_element(By.CSS_SELECTOR, "span:nth-of-type(2)").text
                count_text = listItem.find_element(By.CSS_SELECTOR, ".accordion__textOpenCount").text
                count = re.sub(r'[（）件,]', '', count_text) # 括弧、'件'、カンマを削除し整数に変換

                # print(main_category)
                # print(sub_category_text)
                # print(count)
                data.append((main_category, sub_category_text, count))

except Exception as e:
    print("An error occurred:", e)

print(data)

# DataFrameの作成
df = pd.DataFrame(data, columns=['Category', 'Job Title', 'Job Count'])

df_transposed = df.T

df_transposed.to_csv('./data/doda.csv', header=False, index=False)

driver.quit()