import mysql.connector
from json import loads,dumps
import datetime
from time import time

database = mysql.connector.connect(host='localhost',user='root',password='',database='mihanpop_10')
cursor = database.cursor()

sql = 'INSERT INTO jobs (category,sub_category,opened_url,company_name,company_image,address,telephons,web_url,email,social_media,chats) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

jobs_list = None
values = None

get_file_data = open('all.json','r',encoding='utf-8')
jobs_list = loads(get_file_data.read())

for category in jobs_list:
    for job in category:

        # vcard insert

        domain_id = None
        project_id = None
        user_id = 1
        pixels_ids = dumps([])
        url = None
        if job['web_url']:
            url = job['web_url'].replace('https://','').replace('http://','').replace('/','-').replace('.','-')

        #set phone numbers as url if url not exist
        if job['phone_numbers'] and not job['web_url']:
            for single_phone in job['phone_numbers']:
                url = str(single_phone)

        # telephons
        if job['telephons'] and not job['web_url']:
            for single_telephon in job['telephons']:
                url = str(single_telephon)
            
        name = job['company_name']

        setting = dumps({"is_share_button_visible":0,"is_download_button_visible":0,"background_type":"gradient","background_color":"#ffffff","background_preset":"two","background_gradient_one":"#1e3fc4","background_gradient_two":"#ffffff","background":job['company_image'],"font_family":"default","font_size":16,"favicon":"09bd7faf402cf63acff18a53fa29824d.png","logo":job['company_image'],"opengraph":"","logo_size":125660,"favicon_size":99010,"opengraph_size":None,"background_size":98715,"first_name":"","last_name":"","company":"","job_title":"","birthday":""})

        description = job['desc']
        password = None
        theme = 'new-york'
        custom_js = None
        custom_css = None
        page_views = 0
        is_se_visible = 1
        is_removed_branding = 0
        is_enabled = 1
        last_datetime = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        date_time = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')

        sql = 'INSERT INTO vcards (domain_id,project_id,user_id,pixels_ids,url,name,settings,description,password,theme,custom_js,custom_css,pageviews,is_se_visible,is_removed_branding,is_enabled,last_datetime,datetime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        values = (domain_id,project_id,user_id,pixels_ids,url,name,setting,description,password,theme,custom_js,custom_css,page_views,is_se_visible,is_removed_branding,is_enabled,last_datetime,date_time)

        cursor.execute(sql,values)
        database.commit()

        inserted_id = cursor._last_insert_id

        print(inserted_id)

        # vcards blocks
        
        order = 0
        current_time = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')

        sql = "INSERT INTO `vcards_blocks` (`vcard_block_id`,`vcard_id`,`user_id`,`type`,`name`,`value`,`settings`,`order`,`pageviews`,`is_enabled`,`datetime`,`last_datetime`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        # address
        if job['address']:
            values = (None,inserted_id,'1','address',str(job['company_name']),str(job['address']),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

            cursor.execute(sql,values)

            order += 1

        # web
        if job['web_url']:
            url = job['web_url']
            values = (None,inserted_id,'1','link',str(job['company_name']),str(url),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

            cursor.execute(sql,values)

            order += 1

         #phone numbers
        if job['phone_numbers'] and not job['web_url']:
            for single_phone in job['phone_numbers']:
                values = (None,inserted_id,'1','phone',str(job['company_name']),str(single_phone),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)
            
                order += 1

         # telephons
        if job['telephons'] and not job['web_url']:
            for single_telephon in job['telephons']:
                values = (None,inserted_id,'1','phone',str(job['company_name']),str(single_telephon),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)

                order += 1

         #phone numbers set as link
        if job['phone_numbers'] and not job['web_url']:
            for single_phone in job['phone_numbers']:
                values = (None,inserted_id,'1','link',str(job['company_name']),str(single_phone),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)
            
                order += 1

          # telephons set as link
        if job['telephons'] and not job['web_url']:
            for single_telephon in job['telephons']:
                values = (None,inserted_id,'1','link',str(job['company_name']),str(single_telephon),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)

                order += 1

        # email
        if job['email']:
            email = job['email'].split('://')
            values = (None,inserted_id,'1','email',str(job['company_name']),str(email[1]),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

            cursor.execute(sql,values)
            order += 1

        # social media
        if job['social_media']:
            for single_media in job['social_media']:
                vcard_type = None
                is_type_set = False

                if single_media.find('instagram') != -1 and not is_type_set:
                    vcard_type = 'instagram'
                    is_type_set = True

                elif single_media.find('t.me') != -1 and not is_type_set:
                    vcard_type = 'telegram'
                    is_type_set = True
            
                elif single_media.find('twitter') != -1 and not is_type_set:
                    vcard_type = 'twitter'
                    is_type_set = True

                elif single_media.find('facebook') != -1 and not is_type_set:
                    vcard_type = 'facebook'
                    is_type_set = True
            
                elif single_media.find('linkedin') != -1 and not is_type_set:
                    vcard_type = 'linkedin'
                    is_type_set = True

                elif single_media.find('youtube') != -1 and not is_type_set:
                    vcard_type = 'youtube'
                    is_type_set = True

                elif single_media.find('whatsapp') != -1 and not is_type_set or single_media.find('w.me') and not is_type_set:
                    vcard_type = 'whatsapp'
                    is_type_set = True
            
                else:
                    vcard_type = 'media'
                    is_type_set = True

                media = single_media.split('/')

                values = (None,inserted_id,'1',vcard_type,str(job['company_name']),str(media[-1]),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)
                order += 1

        # chats
        
        if job['chats']:

            for single_chat in job['chats']:
                vcard_type = None
                is_type_set = False

                if single_chat.find('instagram') != -1 and not is_type_set:
                    vcard_type = 'instagram'
                    is_type_set = True

                elif single_chat.find('t.me') != -1 and not is_type_set:
                    vcard_type = 'telegram'
                    is_type_set = True
            
                elif single_chat.find('twitter') != -1 and not is_type_set:
                    vcard_type = 'twitter'
                    is_type_set = True

                elif single_chat.find('facebook') != -1 and not is_type_set:
                    vcard_type = 'facebook'
                    is_type_set = True
            
                elif single_chat.find('linkedin') != -1 and not is_type_set:
                    vcard_type = 'linkedin'
                    is_type_set = True

                elif single_chat.find('youtube') != -1 and not is_type_set:
                    vcard_type = 'youtube'
                    is_type_set = True

                elif single_chat.find('whatsapp') != -1 and not is_type_set or single_media.find('w.me') and not is_type_set:
                    vcard_type = 'whatsapp'
                    is_type_set = True
            
                else:
                    vcard_type = 'chat'
                    is_type_set = True

                chat = single_chat.split('/')

                values = (None,inserted_id,'1',vcard_type,str(job['company_name']),str(chat[-1]),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)
                order += 1


database.commit()
