import mysql.connector as mysql

mycon = mysql.connect(host='localhost',user='root',passwd='root')
# Creating database
Cursor = mycon.cursor()
Cursor.execute('CREATE DATABASE if not exists Company;')
Cursor.execute('USE Company;')

#Creating tables
#Mouna insert queries here
Cursor.execute('CREATE TABLE EMPLOYEES' \                    #Creating Employees table
               '(Id int not null primary key,' \ 
               'Pass varchar(16),' \
               'Name varchar(20) not null,' \
               'Hire_Date date,' \
               'Department varchar(20),' \
               'Position varchar(20) not null,' \
               'Phone_No int not null unique);')

Cursor.execute('CREATE TABLE PAYSLIPS' \ 
               '(Id int FOREIGN KEY REFRENCES EMPLOYEES(Id),' \      #Creating Payslips table
               'Base_Amount decimal(10,2),' \
               'Bonus decimal(10,2),' \
               'Deductions decimal (10,2),' \
               'Net_Salary decimal(10,2));' )

Cursor.execute('CREATE TABLE LEAVE' \
               'Id int FOREIGN KEY REFRENCES EMPLOYEES(Id),' \        #Creating Leave table
               'Leave varchar(30),' \
               'Start_Date date,' \
               'End_Date date,' \
               'Status date,' \
               'Reason varchar(300));') 



      
               

