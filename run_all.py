import subprocess

# 実行するPythonスクリプトのリスト
scripts = {
    'doda' :'doda.py',
    'en転職': "en.py",
    'マイナビ': "mynavi.py",
    '女の転職': "onna.py",
    'Re転職': "re_ten.py",
}

for key, value in scripts.items():
    print(f"▶ 実行中: {key}")
    result = subprocess.run(["python", value], capture_output=True, text=True)
    print(result.stdout)  # スクリプトの標準出力を表示
    if result.returncode != 0:  # エラーが発生した場合
        print(f"⚠️ エラー: {key} の実行に失敗しました！\n{result.stderr}")
        break  # エラーが発生したら中断

print("✅ すべてのスクリプトが完了しました！")
