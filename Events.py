from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import util
import re

def get_info(soup):
    # 初始化一个空字典来存储关键信息
    info = {}   
    
    # 定位到指定的<div>元素
    event_detail_div = soup.find('div', id='event_eventdetails', class_='evocard_box eventdetails')
    # 提取文本信息并存入info字典中
    event_details_text = event_detail_div.text.strip()
    # print(event_details_text)
    info = {'Event Details': event_details_text}
    
    # 定位到时间信息的<div>元素
    time_div = soup.find('div', id='event_time', class_='evocard_box time')

    # 提取时间文本信息
    if time_div:
        time_span = time_div.find('span', class_='evo_eventcard_time_t')
        if time_span:
            time_text = time_span.text.strip()
            info['Time'] = time_text

    # 定位到地址信息的<div>元素
    location_div = soup.find('div', id='event_location', class_='evocard_box location')

    # 提取地址文本信息
    if location_div:
        location_name = location_div.find('p', class_='evo_location_name')
        location_address = location_div.find('p', class_='evo_location_address')
        if location_name and location_address:
            location_name_text = location_name.text.strip()
            location_address_text = location_address.text.strip()
            info['Location'] = f"{location_name_text}, {location_address_text}"

    # 定位到"了解更多"链接的<a>元素
    learn_more_div = soup.find('div', id='event_learnmore', class_='evocard_box learnmore')

    # 提取链接
    if learn_more_div:
        learn_more_link = learn_more_div.find('a')
        if learn_more_link:
            learn_more_href = learn_more_link.get('href')
            info['Learn More'] = learn_more_href

    # 定位到社区信息的<div>元素
    community_div = soup.find('div', id='event_customfield1', class_='evocard_box customfield1')

    # 提取社区信息
    if community_div:
        community_text = community_div.find('p')
        if community_text:
            community_name = community_text.text.strip()
            info['Community'] = community_name
    
    # 定位到组织者信息的<div>元素
    organizer_div = soup.find('div', id='event_organizer', class_='evocard_box organizer')

    # 提取组织者信息和链接
    if organizer_div:
        organizer_name = organizer_div.find('a')
        if organizer_name:
            organizer_name_text = organizer_name.text.strip()
            info['Organizer'] = organizer_name_text

            organizer_href = organizer_name.get('href')
            info['Organizer URL'] = organizer_href


    # 打印info字典
    # print(info)

    data.append(info)
    return data


def get_one_page(driver,data):

    # 等待父元素加载
    parent_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "evcal_list"))
    )

    # 获取所有包含 desc_trig_outter 类的子元素
    desc_trig_outter_elements = parent_element.find_elements(By.CLASS_NAME, "desc_trig_outter")

    # 输出 desc_trig_outter 元素的数量
    print("Number of desc_trig_outter elements:", len(desc_trig_outter_elements))

    # index=1

    # 循环遍历每个 desc_trig_outter 元素
    for element in desc_trig_outter_elements:
        # 获取当前元素的id属性值
        element_id = element.find_element(By.CSS_SELECTOR, 'a.desc_trig').get_attribute('id')
        
        # 构造id选择器
        id_selector = f"#{element_id}"
        
        # 使用id选择器定位元素并点击
        driver.find_element(By.CSS_SELECTOR, id_selector).click()
        
        # 等待一段时间，确保内容加载完成
        time.sleep(3)
        
        # 获取页面源代码
        html_content_with_dynamic_content = driver.page_source
        
        # 解析HTML内容
        soup = BeautifulSoup(html_content_with_dynamic_content, 'html.parser')
        
        # 打印找到的 div 元素
        evopop_body_div = soup.find('div', class_='evopop_body')
        # print("index:", index, "event body div", evopop_body_div)

        data=get_info(evopop_body_div)
        
        # print(data)
        
        driver.find_element(By.CSS_SELECTOR, ".evolb_close_btn").click()
        print("close clicked")
        time.sleep(3)
        
        # index+=1
        
        # if index >= 2:
        #     break
    return data



region_code = 'Events'
parameters_list=util.get_file_path_dict(region_code)

main_page_licensed_url = parameters_list.get('main_page_licensed_url', None)
paging_interval = parameters_list.get('paging_interval', None)
main_page_loading_time = parameters_list.get('main_page_loading_time', None)
main_page_non_licensed_url = parameters_list.get('main_page_non_licensed_url', None)
times_for_retry = parameters_list.get('times_for_retry', None)

driver = util.get_driver()
url = main_page_licensed_url
# print(url)
driver.get(url)

data = []
link_data = []
time.sleep(10)

# 获取页面源代码
html_content_with_dynamic_content = driver.page_source
    
# 解析HTML内容
soup = BeautifulSoup(html_content_with_dynamic_content, 'html.parser')


# 输出 desc_trig_outter 元素的数量
    # 等待父元素加载
parent_element = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "evcal_list"))
)

# 获取所有包含 desc_trig_outter 类的子元素
desc_trig_outter_elements = parent_element.find_elements(By.CLASS_NAME, "desc_trig_outter")
print("Number of desc_trig_outter elements:", len(desc_trig_outter_elements))



while len(desc_trig_outter_elements)!=0:

    parent_element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "evcal_list"))
    )

    # 获取所有包含 desc_trig_outter 类的子元素
    desc_trig_outter_elements = parent_element.find_elements(By.CLASS_NAME, "desc_trig_outter")

    data=get_one_page(driver,data)

    time.sleep(5)
        
    # 等待按钮可见
    next_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "evcal_next"))
    )

    # 点击按钮
    next_button.click()

    time.sleep(5)
    print("click Next page finish")

# 关闭浏览器
driver.close()

df = pd.DataFrame(data)
util.save_final_file(df,region_code, file_type = 'list', job_type = "Events Achive")
util.log_event_list(region_code, 'EV_FINISHED', None, None, None)

