import mysql.connector as mysql
import csv
print("Enter your mySQL server details")
host = input('Hostname: ')
user = input('User: ')
passw = input('Password: ')
hos = input('En')
mycon = mysql.connect(host=host,user=user,passwd=passw)
mycon.autocommit= True
# Creating database
Cursor = mycon.cursor()
Cursor.execute('CREATE DATABASE if not exists Company;')
Cursor.execute('USE Company;')

#Creating tables
#Creating Employees table
q = 'CREATE TABLE if not exists EMPLOYEES' \
'(Id int not null primary key,' \
'Pass varchar(16) unique not null,' \
'Name varchar(20) not null,' \
'Hire_Date date,' \
'Department varchar(20),' \
'Position varchar(20) not null,' \
'Phone_No varchar(10) not null unique);'
Cursor.execute(q)

#Creating Payslips table

q = 'CREATE TABLE if not exists PAYSLIPS' \
'(Id int ,' \
'Base_Amount decimal(10,2),' \
'Bonus decimal(10,2) default 1000,' \
'Deductions decimal (10,2) default 0,' \
'FOREIGN KEY (Id) REFERENCES EMPLOYEES(Id) ON UPDATE CASCADE ON DELETE CASCADE);' 
Cursor.execute(q)

#Creating Employee leave table

q = 'CREATE TABLE if not exists E_LEAVE ' \
'(Id int,  ' \
'LeaveType varchar(30),' \
'Duration int ,' \
'Status varchar(8) default "pending",' \
'Reason varchar(200) not null,'\
'FOREIGN KEY (Id) REFERENCES EMPLOYEES(Id) ON UPDATE CASCADE ON DELETE CASCADE);'
Cursor.execute(q)

#Inserting data into the tables
#Employee
with open('F:\\Project\\Data\\Employees.csv',newline='\r\n') as f:
    r = csv.reader(f,quoting=csv.QUOTE_MINIMAL)
    for re in r:
        
        if re ==[]:
            break
        else:
            re[0]=int(re[0])
            rec =  tuple(re)
            query = 'INSERT INTO EMPLOYEES '\
            f'VALUES {rec};'
            Cursor.execute(query)
#Payslips
with open('F:\\Project\\Data\\Payslips.csv',newline='\r\n')as f:
    r = csv.reader(f)
    for re in r:
        if re==[]:
            break
        else:
            re[0]=int(re[0])
            rec = tuple(re)
            query = f'''INSERT INTO PAYSLIPS
            VALUES {rec};'''
            Cursor.execute(query)
#Leave
with open('F:\\Project\\Data\\Leave.csv',newline='\r\n')as f:
    r = csv.reader(f)
    for re in r:
        
        if re ==[]:
            break
        else:
            re[0]=int(re[0])
            rec =  tuple(re)
            query = 'INSERT INTO E_LEAVE '\
            f'VALUES {rec};'
            Cursor.execute(query)
print('Data successfully imported')
input('press enter to exit')