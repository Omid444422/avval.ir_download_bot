from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from json import dumps

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

driver.get('https://avval.ir/')

sleep(3)

jobs_list = list()
counter = 1
categories_list = list()

main_categories = driver.find_elements(By.XPATH,'//*[@id="directory"]/div[1]/ul/li')

for category in main_categories:
    category_data = {'status':False,'cat_name':None,'jobs_link':list()}
    category.click()

    sleep(2)

    # driver.execute_script("arguments[0].scrollIntoView();", category)

    single_category_name = category.find_element(By.XPATH,'.//button/span').text

    sleep(2)

    sub_categories = driver.find_elements(By.CSS_SELECTOR,'div#tab-wrapper div[style="display: block;"] div:first-child ul.topic li')

    for sub_category in sub_categories:
        single_sub_cat_name = sub_category.find_element(By.XPATH,'.//button').text

        sub_category.click()

        sleep(2)

        sub_category_links = driver.find_elements(By.CSS_SELECTOR,'div#tab-wrapper div[style="display: block;"] div:nth-child(2) div:not([hidden]):not([hidden="hidden"]) ul li')

        for sub_link in sub_category_links:
            single_sub_link_data = {'counter':counter,'sub_cat_name':None,'link_title':None,'url':None,'status':False}

            sub_link_name = sub_link.find_element(By.XPATH,'.//a').text
            sub_link_url = sub_link.find_element(By.XPATH,'.//a').get_attribute('href')

            single_sub_link_data['sub_cat_name'] = single_sub_cat_name
            single_sub_link_data['link_title'] = sub_link_name
            single_sub_link_data['url'] = sub_link_url

            category_data['cat_name'] = single_category_name
            category_data['jobs_link'].append(single_sub_link_data)

            counter+= 1
             
            print('*'*100)
            print(counter)
            print(single_sub_link_data)
            print('*'*100)

    categories_list.append(category_data)



categories_json = dumps(categories_list,ensure_ascii=False)

with open('category_data.json','w',encoding='utf-8') as cat_data_json_file:
    cat_data_json_file.write(categories_json)


print('end')

