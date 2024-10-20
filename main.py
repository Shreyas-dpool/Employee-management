import mysql.connector as mysql

mycon = mysql.connect(host='localhost',user='root',passwd='root')
# Creating database
Cursor = mycon.cursor()
Cursor.execute('CREATE DATABASE if not exists Employee;')
Cursor.execute('USE Employee;')


