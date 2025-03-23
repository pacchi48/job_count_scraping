import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
cService = webdriver.ChromeService()
driver = webdriver.Chrome(service=cService, options=chrome_options)

jobs = {
    '営業系': {
    '営業（法人、個人）': '0101',
    'ルート営業、代理店営業': '0102',
    'カウンターセールス': '0103',
    '技術・システム営業': '0104',
    'メディカル営業（MR、医療機器）': '0105',
    '海外営業': '0106',
    'コンサルタント': '0107',
    '人材コーディネーター': '0108',
    'インサイドセールス': '0110',
    '営業推進・販売促進': '0111',
    '起業家': '0112',
    'その他営業系': '0109'
},
    '企画・事務・管理系': {
    '一般事務、営業事務、貿易事務、秘書': '0201',
    '広告・宣伝・広報・IR': '0202',
    '人事、総務、法務、経理': '0203',
    'マーケティング、リサーチ、分析': '0204',
    'サポートデスク、コールセンター': '0205',
    '通訳、翻訳': '0206',
    '企画・商品開発': '0208',
    '経営企画': '0209',
    'カスタマーサクセス・カスタマーサポ―ト': '0210',
    'ITコンサルタント': '0211',
    'データサイエンティスト': '0212',
    'サイト運用': '0213',
    'その他企画・事務・管理系': '0207'
},
    '販売・サービス系（ファッション、フード、小売）': {
    'バイヤー、スーパーバイザー、店舗開発': '0301',
    'MD（マーチャンダイザー）': '0306',
    '店長・店長候補': '0302',
    '販売スタッフ': '0303',
    'ホール・調理スタッフ': '0304',
    'その他販売・サービス系': '0305',
},
    '専門サービス系（医療、福祉、教育、その他）': {
    '医療事務': '0401',
    '介護スタッフ、ケアマネージャー、栄養士': '0402',
    '教室長・スクール運営': '0403',
    '教員、講師、インストラクター': '0404',
    'ブライダルコーディネーター': '0405',
    'ホテル、宿泊施設スタッフ': '0406',
    'エステティシャン': '0407',
    'ドライバー（交通サービス）': '0409',
    '薬剤師': '0410',
    '理学療法士': '0411',
    '作業療法士': '0412',
    '言語聴覚士': '0413',
    '視能訓練士': '0414',
    '臨床工学技士': '0415',
    '歯科衛生士': '0416',
    '臨床検査技師': '0417',
    '診療放射線技師': '0418',
    '社会福祉士': '0419',
    '精神保健福祉士': '0420',
    '介護福祉士': '0421',
    '医療ソーシャルワーカー': '0422',
    'マッサージ師・はり師': '0423',
    '葬祭ディレクター・プランナー': '0424',
    'トレーダー・ディーラー': '0425',
    '融資・資産運用': '0426',
    '証券アナリスト': '0427',
    'アクチュアリー': '0428',
    '公務員・団体職員': '0429',
    'その他専門サービス系': '0408'
},
    'クリエイティブ系（ディレクター、デザイナー、ライター、その他）': {
    'ディレクター（Web、広告、ゲームほか）': '0501',
    'デザイナー（Web、広告、ゲーム、ファッションほか）': '0502',
    '編集・ライター': '0503',
    '芸能マネージャー・スタッフ': '0504',
    'インテリア・空間コーディネーター': '0505',
    'AD・AP・制作技術・美術': '0506',
    '出版・印刷系オペレーター': '0507',
    'ゲームクリエイター': '0509',
    'その他クリエイティブ系': '0508'
},
    'ITエンジニア系（SE・システム開発・インフラ）': {
    'システム開発（Web・オープン系）': '0601',
    'システム開発（汎用機系）': '0602',
    'システム開発（制御・組み込み系）': '0603',
    'システム開発（アプリ・ゲーム系）': '0604',
    'ネットワーク・サーバエンジニア（設計・構築・運用・保守）': '0605',
    'ネットワークエンジニア': '0614',
    'サーバエンジニア': '0615',
    '社内SE・情報システム': '0606',
    'テクニカルサポート、ヘルプデスク': '0607',
    'プログラマー（PG）・コーダー': '0609',
    'プロジェクトマネージャー（PM）': '0610',
    'セールスエンジニア': '0611',
    'カスタマーエンジニア': '0612',
    'システム運用・保守': '0613',
    'ゲーム系エンジニア': '0616',
    'データベースエンジニア': '0617',
    'その他ITエンジニア系（SE・システム開発・インフラ）': '0608'
},
    '技術系（電気、電子、機械）': {
    '回路・半導体・光学・システム・制御設計': '0701',
    '機械・機構設計、CAD・CAM': '0702',
    '品質保証、品質管理、生産・製造管理': '0703',
    '評価・検査、研究・開発、特許': '0704',
    '製造スタッフ（電気、電子、機械）': '0705',
    'その他技術系（電気、電子、機械）': '0706'
},
    '技術系（建築、土木）': {
    'プランニング、測量、設計、積算': '0801',
    '施工管理、設備保守管理、環境保全': '0802',
    '研究開発、品質管理、特許': '0803',
    'その他技術系（建築、土木）': '0804'
},
    '技術系（医薬、化学、素材、食品）': {
    '化学、素材系': '0901',
    '食品、化粧品、香料系': '0902',
    '医薬品、医療機器、バイオ系': '0903',
    '製造スタッフ（医薬、化学、素材、食品）': '0904',
    'その他技術系（医薬、化学、素材、食品）': '0905'
}
,
    '施設・設備管理、技能工、運輸・物流系': {
    '施設・設備管理、警備、清掃系': '1001',
    '技能工（整備・製造・土木・電気・工事）': '1002',
    '運輸サービス、交通サービス、配送、倉庫系': '1003',
    '商品・在庫・倉庫管理': '1005',
    'ドライバー（運輸サービス）': '1006',
    'その他施設・設備管理、技能工、運輸・物流系': '1004'
},
}

data = []

for key, values in jobs.items():
    for title, val in values.items():
        url = f'https://re-katsu.jp/career/search/sch_result?p5={val}'
        # 指定したURLにアクセス
        driver.get(url)
        time.sleep(1)
        try:
            count = driver.find_element(By.ID, "lblCountAllKinmu")
            data.append((key, title, count.text))
        except Exception as e:
            data.append((key, title, 0))
        

# DataFrameの作成
df = pd.DataFrame(data, columns=['Category', 'Job Title', 'Job Count'])

df_transposed = df.T

df_transposed.to_csv('./data/re_ten.csv', header=False, index=False)

# ドライバーを閉じる
driver.quit()

print('正常終了')