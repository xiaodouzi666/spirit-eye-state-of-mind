from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)
CORS(app)  # 允许所有域名跨域

@app.route('/generate_video', methods=['POST'])
def generate_video():
    user_message = request.json.get('message', '')  # 安全地获取消息
    group_id = "1768536805574983825"
    api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiLliJjkv4rlkJsiLCJVc2VyTmFtZSI6IuWImOS_iuWQmyIsIkFjY291bnQiOiIiLCJTdWJqZWN0SUQiOiIxNzY4NTM2ODA1NjIxMTIxMTY5IiwiUGhvbmUiOiIxMzczOTA4MjgwMyIsIkdyb3VwSUQiOiIxNzY4NTM2ODA1NTc0OTgzODI1IiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjQtMDMtMjIgMDQ6Mzk6NTUiLCJpc3MiOiJtaW5pbWF4In0.xjtaEkbdtPCGBYP3wuYtAGeiTgLASxEk_TZqfjFlXkz-b7Nfs-3SqppYTu6V7_13zBDQL_16GtFRBBlN8thHjpfzmAH4kDsa7nrS30-DxIbIyIoBwHt_kdrYsNt-5CCKXh8bFdGwtgzh7QJ3XIXPqilD1j5hKGdSzfRuJIizUtkF_etQr78fzqVE9UUgH5SuCjlbJrpzXhB_gjMZifjyXk56srjE2dSw_k2voOegLmqxswkFUa92KoU6G-cPcyaG0MFiNWA_qjG-Dn-NbKcgNusTnBG7zyaZaaz72zGRS7baukwkadvSQX7pGpWhR1dZKfNfk4Gl-HIUfbqozFSj9g"

    # 构造请求大模型的请求体
    url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={group_id}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    request_body = {
        "model": "abab5.5-chat",
        "tokens_to_generate": 1024,
        "reply_constraints": {"sender_type": "BOT", "sender_name": "MM智能助理"},
        "messages": [{"sender_type": "USER", "sender_name": "小明", "text": user_message}],
        "bot_setting": [
            {
                "bot_name": "MM智能助理",
                "content": "这是您的介绍信息",
            }
        ],
    }

    response = requests.post(url, headers=headers, json=request_body)
    reply = response.json().get("reply", "未获取到回复")

    # 使用Selenium和ChromeDriver打开浏览器并输入大模型的回复
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get('https://vip.aminer.cn/sign/')
        input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "validate_other_text")))
        input_box.clear()
        input_box.send_keys(reply)  # 将大模型的回复输入到网页中

        generate_button = driver.find_element(By.CLASS_NAME, 'btnWhiteBlueContainer')
        generate_button.click()
        time.sleep(10)  # 根据实际需要调整等待时间

        video_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "example_video")))
        video_url = video_element.get_attribute('src')
    finally:
        driver.quit()

    return jsonify({'video_url': video_url})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
