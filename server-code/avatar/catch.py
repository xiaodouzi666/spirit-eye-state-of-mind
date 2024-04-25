from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By  # 确保已经导入By类
import time

# 设置无头Chrome选项
options = Options()
options.add_argument("--headless")  # 启用无头模式
options.add_argument("--no-sandbox")  # 绕过OS安全模型
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_argument('start-maximized')  # 最大化启动，避免未最大化导致的元素定位问题
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

# 设置ChromeDriver路径
driver_path = '/usr/local/bin/chromedriver'  # 更新为正确的chromedriver路径
service = Service(executable_path=driver_path)


# 启动浏览器（这里以Chrome为例）
driver = webdriver.Chrome(service=service, options=options)

# 打开目标网页
driver.get('https://vip.aminer.cn/sign/')  # 请替换成实际的网页URL

try:
    # 定位输入框并输入文本
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "validate_other_text"))
    )
    input_box.clear()
    input_box.send_keys('你好，我是元宇宙虚拟人')

    # 点击生成按钮
    generate_button = driver.find_element(By.CLASS_NAME, 'btnWhiteBlueContainer')
    generate_button.click()

    # 等待视频生成
    time.sleep(10)  # 根据视频生成的实际速度调整等待时间

    # 获取视频链接
    video_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "example_video"))
    )
    video_url = video_element.get_attribute('src')
    print("视频链接:", video_url)

finally:
    # 关闭浏览器
    driver.quit()
