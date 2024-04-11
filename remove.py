import mysql.connector

database = mysql.connector.connect(host='localhost',user='root',password='',database='mihanpop_10')
cursor = database.cursor()

sql = "DELETE FROM vcards WHERE url IS NULL"

cursor.execute(sql)
database.commit()

