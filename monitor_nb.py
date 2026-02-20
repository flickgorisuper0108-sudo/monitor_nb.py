import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# --- 設定 ---
TARGET_URL = "https://outlet.newbalance.jp/pd/M1906AV1-48796.html?sm=Top+Results&pdq=1906A"
WEBHOOK_URL = os.environ['https://discord.com/api/webhooks/782606611280953399/E6AJIIIkJC7ScmPw4iGC_-C1Ri62DXOLurhyHVfTr6ZR-zg98bynaTND7PFImnGTcFIV']

def notify_discord(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

def check_stock():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # サイトにロボットだと判定されにくくするための設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    
    available_sizes = []
    
    try:
        driver.get(TARGET_URL)
        time.sleep(5) # 読み込み待ち
        
        # サイズボタン（swatch-item size クラスの中の button）をすべて取得
        size_buttons = driver.find_elements(By.CSS_SELECTOR, ".swatch-item.size button")
        
        for button in size_buttons:
            size_label = button.text.strip() # "27.0" などのテキストを取得
            classes = button.get_attribute("class")
            
            # 'disabled' がクラスに含まれていなければ、選択可能（在庫あり）
            if "disabled" not in classes:
                available_sizes.append(size_label)
        
        if available_sizes:
            # 見つかったサイズを並べてメッセージ作成
            size_str = "、".join(available_sizes)
            message = f"👟 **NBアウトレット 在庫復活！** 👟\n以下のサイズが購入可能になっています：\n**{size_str}**\n{TARGET_URL}"
            notify_discord(message)
        else:
            print("全サイズ完売中...")
            
    except Exception as e:
        print(f"エラー発生: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_stock()
