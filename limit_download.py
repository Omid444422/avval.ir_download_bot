from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from os.path import exists
from time import sleep
from json import loads,dumps


categories_links_list = None
downloaded_job_links = list()
counter = 1

with open('./category_data.json','r',encoding='utf-8') as json_category_file:
    categories_links_list = loads(json_category_file.read())

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

for single_category in categories_links_list:
    for job_link in single_category['jobs_link']:

        if exists('./data/'+job_link['link_title']+'.json'):
            print('skip: ' + job_link['link_title'])
            continue
    
        pages = [job_link['url'],job_link['url']+'?page='+str(2)]
        
        for url in pages:

            driver.get(url)

            try:
                error_page = driver.find_element(By.XPATH,'//*[@id="nabak-wizard"]/div[1]/p[1]/b')
                continue
            except:
                pass

            jobs = driver.find_elements(By.CSS_SELECTOR,'#search_form > div.flex.flex-wrap > main > div.c-result > div > div.lg\:flex.justify-center.items-center.min-h-32 > div.content > h2 > a')
            jobs_list = list()

            for job in jobs:
                jobs_list.append(job.get_attribute('href'))

            for single_job in jobs_list:
                driver.get(single_job)

                sleep(5)

                job_company_image_url = None
                try:
                    job_company_image_url = driver.find_element(By.XPATH,'//*[@id="wrapper"]/div/div[2]/div/div/div[1]/div/div[1]/div/img').get_attribute('src')
                except:
                    pass

                job_company_name = driver.find_element(By.CSS_SELECTOR,'h1').text
                job_company_desc = None
                try:
                    job_company_desc  = driver.find_element(By.CSS_SELECTOR,'div.slogan').text
                except:
                    pass

                job_company_address = None
                try:
                    job_company_address = driver.find_element(By.XPATH,'//*[@id="contacts"]/div/div[2]/ul/li[1]/div[2]/p').text
                except:
                    pass
                
                job_telephons = list()
                job_phone_numbers = list()
                job_web_url = None
                job_email = None
                job_social_network = list()
                job_chats = list()

                jobs_data_list = driver.find_elements(By.CSS_SELECTOR,'div.job_cnt.information_contact ul li')

                try:
                    show_phones_button = driver.find_element(By.CSS_SELECTOR,'a.show-phone.button')
                    show_phones_button.click()

                    sleep(1)
                except:
                    pass

                for job_data in jobs_data_list:
                    title = job_data.find_element(By.XPATH,'.//div[1]').text

                    if title.find('تلفن') > -1:

                        value = job_data.find_elements(By.XPATH,'.//div[2]/span')

                        for telephon_number in value:
                            job_telephons.append(telephon_number.text)
                    
                    elif title.find('تلفن همراه') > -1:

                        value = job_data.find_elements(By.XPATH,'.//div[2]/span')

                        for phone_number in value:
                            job_phone_numbers.append(phone_number.text)

                    elif title.find('وب سایت') > -1:
                        job_web_url = job_data.find_element(By.XPATH,'.//div[2]/a').get_attribute('href')

                    elif title.find('تلفکس') > -1:

                        value = job_data.find_elements(By.XPATH,'.//div[2]/span')

                        for phone_number in value:
                            job_phone_numbers.append(phone_number.text)

                    elif title.find('ایمیل') > -1:
                        job_email = job_data.find_element(By.XPATH,'.//div[2]/a').get_attribute('href')

                    elif title.find('صفحات اجتماعی') > -1:
                        value = job_data.find_elements(By.XPATH,'.//div[2]/a')
                    
                        for social_network in value:
                            job_social_network.append(social_network.get_attribute('href'))

                    elif title.find('چت') > -1:
                        value = job_data.find_elements(By.XPATH,'.//div[2]/a')

                        for chat in value:
                            job_chats.append(chat.get_attribute('href'))

                single_job_data = {'counter':counter,'category':single_category['cat_name'],'sub_category':job_link['sub_cat_name'],'opened_url':job_link['url'],'company_image':job_company_image_url,'company_name':job_company_name,'desc':job_company_desc,'address':job_company_address,'telephons':job_telephons,'phone_numbers':job_phone_numbers,'web_url':job_web_url,'email':job_email,'social_media':job_social_network,'chats':job_chats}

                downloaded_job_links.append(single_job_data)

                counter+= 1

                print('*'*100)
                print(single_job_data)
                print('*'*100)

        downloaded_job_links_json = dumps(downloaded_job_links,ensure_ascii=False)
        with open('./data/'+job_link['link_title']+'.json','w',encoding='utf-8') as file_json:
            file_json.write(downloaded_job_links_json)

        downloaded_job_links = list()


print('ended')