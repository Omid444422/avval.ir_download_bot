import mysql.connector
from json import loads,dumps
import datetime
from time import time

database = mysql.connector.connect(host='localhost',user='root',password='',database='avval.ir')
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
        url = job['web_url']
        name = job['company_name']

        setting = dumps({"is_share_button_visible":0,"is_download_button_visible":0,"background_type":"gradient","background_color":"#ffffff","background_preset":"two","background_gradient_one":"#1e3fc4","background_gradient_two":"#ffffff","background":"7c548c06e9f39e71ce58df979e8823f4.png","font_family":"default","font_size":16,"favicon":"09bd7faf402cf63acff18a53fa29824d.png","logo":"43b49973aa7439e1e9582067f49ead95.png","opengraph":"","logo_size":125660,"favicon_size":99010,"opengraph_size":None,"background_size":98715,"first_name":"","last_name":"","company":"","job_title":"","birthday":""})

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
            values = (None,'2','1','address',str(job['company_name']),str(job['address']),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

            cursor.execute(sql,values)

            order += 1

        # telephons
        if job['telephons']:
            for single_telephon in job['telephons']:
                values = (None,'2','1','phone',str(job['company_name']),str(single_telephon),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)

                order += 1

        
        #phone numbers
        if job['phone_numbers']:
            for single_phone in job['phone_numbers']:
                values = (None,'2','1','phone',str(job['company_name']),str(single_phone),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)
            
                order += 1

        # web
        if job['web_url']:
            values = (None,'2','1','link',str(job['company_name']),str(job['web_url']),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

            cursor.execute(sql,values)

            order += 1

        # email
        if job['email']:
            values = (None,'2','1','email',str(job['company_name']),str(job['email']),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

            cursor.execute(sql,values)
            order += 1

        # social media
        if job['social_media']:
            for single_media in job['social_media']:
                vcard_type = None

                if single_media.find('instagram'):
                    vcard_type = 'instagram'

                elif single_media.find('t.me'):
                    vcard_type = 'telegram'
            
                elif single_media.find('twitter'):
                    vcard_type = 'twitter'

                elif single_media.find('facebook'):
                    vcard_type = 'facebook'
            
                elif single_media.find('linkedin'):
                    vcard_type = 'linkedin'

                elif single_media.find('youtube'):
                    vcard_type = 'youtube'

                elif single_media.find('whatsapp') or single_media.find('w.me'):
                    vcard_type = 'whatsapp'
            
                else:
                    vcard_type = 'media'

                values = (None,'2','1',vcard_type,str(job['company_name']),str(single_media),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)
                order += 1

        # chats
        
        if job['chats']:

            for single_chat in job['chats']:
                vcard_type = None

                if single_media.find('instagram'):
                    vcard_type = 'instagram'

                elif single_media.find('t.me'):
                    vcard_type = 'telegram'
            
                elif single_media.find('twitter'):
                    vcard_type = 'twitter'

                elif single_media.find('facebook'):
                    vcard_type = 'facebook'
            
                elif single_media.find('linkedin'):
                    vcard_type = 'linkedin'

                elif single_media.find('youtube'):
                    vcard_type = 'youtube'

                elif single_media.find('whatsapp') or single_media.find('w.me'):
                    vcard_type = 'whatsapp'
            
                else:
                    vcard_type = 'chat'

                values = (None,'2','1',vcard_type,str(job['company_name']),str(single_chat),"{'\open_in_new_tab\':1}",'0','0','1',current_time,current_time)

                cursor.execute(sql,values)
                order += 1


database.commit()
