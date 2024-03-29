import mysql.connector
from json import loads,dumps

database = mysql.connector.connect(host='localhost',user='root',password='',database='avval.ir')
cursor = database.cursor()

sql = 'INSERT INTO jobs (category,sub_category,opened_url,company_name,company_image,address,telephons,web_url,email,social_media,chats) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

jobs_list = None
values = None

get_file_data = open('all.json','r',encoding='utf-8')
jobs_list = loads(get_file_data.read())

for category in jobs_list:
    for job in category:

        is_record_exist = False

        cursor.execute('SELECT * FROM jobs WHERE company_name=%s AND sub_category=%s',(job['company_name'],job['sub_category']))
        result = cursor.fetchall()

        for record in result:
            is_record_exist = True
            break

        if is_record_exist:
            print('skip: ' + job['company_name'])
            continue

        values = (job['category'],job['sub_category'],job['opened_url'],job['company_name'],job['company_image'],job['address'],dumps(job['telephons']),job['web_url'],job['email'],dumps(job['social_media']),dumps(job['chats']))

        cursor.execute(sql,values)
        print('insert: ' + job['company_name'])


database.commit()
