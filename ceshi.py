from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

service = Service(r"C:\Users\liulanqi\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)
# 可替换指定领导的URL链接
driver.get("https://liuyan.people.com.cn/threads/list?fid=573")
# 给3秒等待第一页数据加载时间，避免浏览器直接关闭
time.sleep(3)
def safe_find_text(element, xpath, default="N/A"):
    try:
        return element.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        return default
# 记录已爬取数据的ID（唯一标识）
crawled_ids = set()
with open("领导留言板.txt", "w", encoding="utf-8") as f:
    while True:
        # 等待新数据加载（关键：等待新增的li元素）
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//ul[@class='replyList']/li[not(@data-crawled)]"))
            )
        except:
            print("数据加载超时或已无新数据")
            break
        # 获取当前所有li元素
        li_list = driver.find_elements(By.XPATH, "//ul[@class='replyList']/li")
        new_data_count = 0
        for item in li_list:
            # 检查是否已爬取过（通过留言ID）
            pll_03 = safe_find_text(item, ".//div[@class='headMainS fl']/h2/span[2]")
            if pll_03 in crawled_ids:
                continue  # 跳过已爬取的数据
            # 标记为已爬取
            crawled_ids.add(pll_03)
            # 提取其他字段
            pll_01 = safe_find_text(item, "./div[@class='tabList fl']/h1")
            pll_02 = safe_find_text(item, "./div[@class='tabList fl']/p")
            pll_04 = safe_find_text(item, "./div[2]/div[@class='headMainS fl']/p")
            pll_05 = safe_find_text(item, "./p[@class='replyContent']/span[1]")
            pll_06 = safe_find_text(item, ".//p[@class='domainName']")
            # 写入文件
            data = f"""
                    问题标题：{pll_01}
                    回复状态：{pll_02}
                    留言ID：{pll_03}
                    留言时间：{pll_04}
                    留言内容：{pll_05}
                    留言类型：{pll_06}
                    {'=' * 30}"""
            f.write(data + "\n")
            new_data_count += 1
        print(f"本次爬取到 {new_data_count} 条新数据")
        # 如果没有新数据，停止翻页
        if new_data_count == 0:
            print("没有新数据，翻页结束")
            break
        # 尝试翻页
        try:
            driver.find_element(By.XPATH, "//div[@class='mordList']").click()
            # 动态标记已爬取元素（通过注入属性）
            driver.execute_script("""
                document.querySelectorAll('ul.replyList li').forEach(li => {
                    li.setAttribute('data-crawled', 'true');
                });
            """)
            time.sleep(2)
        except NoSuchElementException:
            print("翻页结束")
            break
time.sleep(5)
driver.quit()
