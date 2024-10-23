import mysql.connector as mysql
import csv
print("Enter your mySQL server details")
host = input('Hostname: ')
user = input('User: ')
passw = input('Password: ')

mycon = mysql.connect(host=host,user=user,passwd=passw)
mycon.autocommit= True
Cursor = mycon.cursor()
#Login Menu
def login_menu():
    global uid, password
    print("Welcome to employee management terminal!")
    print('1:Log in to access further features')
    print('2:Exit')
    ch = int(input('Enter choice: '))
    if ch ==  1:
        uid = int(input('Enter your user id: '))
        password = input('Enter your password: ')
        query = f"Select * From EMPLOYEES "\
        f'where Id ={uid};'
        Cursor.execute(query)
        rec = Cursor.fetchone()
        if rec[1]==password:
            print("Succesfully logged in! ")
            print(f"Welcome back {rec[2]}")
            if rec[5].lower()=='admin':
                print('Welcome back admin!')
                admin_menu()
            else:
                main_menu()
        else:
            print('User ID or password incorrect')
            login_menu()
  
    
#Main menu 
def main_menu():
    print('What would you like to do today?\n'
          '1. View Salary \n'
          '2: View other details\n'
          '3: Update your password\n'
          '4: View leave details\n '
          '5: Log Out') 
    ch = int(input('Enter your choice: '))
    if ch ==1:
        salary_menu()
    elif ch==2:
        query=f"Select * From EMPLOYEES "\
        f'where Id ={uid};'
        Cursor.execute(query)
        rec= Cursor.fetchone()
        print('Your hire date is: ',rec[3])
        print('Your department is: ',rec[4])
        print('Your position is: ',rec[5])
        print('Your phone no is: ',rec[-1])
    elif ch ==3:
        entered=input(('Enter your current password: '))
        if entered == password:
            new = input('Enter your new password: ')
            q = f'''UPDATE EMPLOYEES
            SET pass = {entered}
            WHERE Id={uid};'''
            Cursor.execute(q)
            print("Password successfully updated")
        else:
            print('Wrong password entered! ')
            main_menu()
    elif ch==4:
        leave_menu()



    elif ch == 5:
        print('Succesfully logged out')
        login_menu()
    else:
        print('Invalid choice')
        main_menu()

#Salary menu
def salary_menu():
    print('''Salary information:
    1: View net salary
    2: View salary details
    3: Go back to main menu
    ''')
    ch1 = int(input('Enter choice: '))
    if ch1 ==1 or 2:
        q= 'SELECT Id,Base_amount,Bonus,Deductions,(Base_amount + Bonus - Deductions) FROM PAYSLIPS \n'
        f'WHERE Id={uid} '
        Cursor.execute(q)
        rec = Cursor.fetchone()
        if ch1 ==1:
            print('Your net salary is: ',rec[4])
            main_menu()
        elif ch1==2:
            print('Your base salary is: ',rec[1])
            print('Your have the bonuses: ',rec[2])
            print('The amount ',rec[3],' is being deducted from your salary')
            print('Your net salary is : ',rec[4])
            main_menu()
    elif ch1==3:
        main_menu()
    else:
        print('Invalid choice')
        salary_menu()

#Leave menu
def leave_menu():
    print('Leave menu')
    print('1: View leave details')
    print('2: Apply for leave')
    ch2 = int(input('Enter choice: '))
    if ch2 == 1:
        query = f'''SELECT * FROM E_LEAVE
        WHERE Id={uid};'''
        Cursor.execute(query)
        rec = Cursor.fetchone()
        print('Your leave type is: ',rec[1])
        print('Your leave duration is: ',rec[2])
        print('The reason you applied for leave is: ',rec[-1])
        print('Your leave status: ',rec[3])
        main_menu()
    elif ch2==2:
        typ = input('Enter your type of leave: ')
        Dur = int(input('Enter your leave duration: '))
        reason = input('Enter your reason: ')
        tup = ()
        uid,typ,Dur,reason = tup
        query = f'''INSERT INTO E_LEAVE (Id,LeaveType,Duration,Reason)
        Values {tup};'''
        print('Leave applied, wait for further notice if approved.')
        main_menu()

#Update function
def update(table,attribute,value,Id):
    if type(value) is int:
        query = f'''UPDATE {table}
        set {attribute}={value}
        where Id={uid}'''
        Cursor.execute(query)    
    else:
        query = f'''UPDATE {table}
        set {attribute}='{value}'
        where Id={uid}'''
        Cursor.execute(query)    

# Admin menu
def admin_menu():
    print('Welcome to admin menu')
    print('1: Update employee details')
    print('2: Change employee salaries')
    print('3: Look at employee leave details')
    print("4: Add a new employee's details")
    print('5: Delete an employee details')
    print('6: Access other features')
    print('7: Log out')
    ch1 = int(input('Enter your choice: '))
    if ch1 == 1:
        upid = int(input('Enter the id of the user you want to update: '))
        atr = input('Enter which attribute you want to update(Id,Department,Position,Phone_no): ')
        val = input('Enter new value of attribute: ')
        if atr.lower() == 'id'or 'phone_no':
            val = int(val)
            update('EMPLOYEES',atr,val,upid)

        else:
            update('EMPLOYEES',atr,val,upid)
            
    elif ch1 ==2:
        upid = int(input('Enter the id of the user you want to update: '))
        atr = input('Enter which attribute you want to update(Base_amount,Deductions,Bonus): ')
        val = int(input('Enter new value of attribute: '))
        update('PAYSLIPS',atr,val,upid)
    elif ch1 ==3:
        upid = int(input('Enter the id of whos leave details you want to see: '))
        query = f'''SELECT * FROM E_LEAVE
        WHERE Id={upid};'''
        Cursor.execute(query)
        rec = Cursor.fetchone()
        print('Their leave type is: ',rec[1])
        print('Their leave duration is: ',rec[2])
        print('Their reason you applied for leave is: ',rec[-1])
        print('Their leave status: ',rec[3])
        print('their leave reason is: ',rec[-1])
        if rec[3].lower()=='Pending':
            print('This leave application is pending, you can approve, deny or leave it pending')
            nstat = input('Enter current status: ')
            update('E_LEAVE','Status',nstat,upid)
            print("Successfully updated")
        admin_menu()
        
    elif ch1 ==4:
        Id = int(input('Enter new employee id: '))
        passw = input('Enter password: ')
        name = input('Enter name')
        hiredate = input('Enter hire date: ')
        dep = input('Enter department')
        pos = input('Enter position: ')
        ph = input('Enter phone number: ')
        base = int(input('Enter base salary: '))
        bonus = int(input('Enter bonus(optional): '))
        deductions = int(input('Enter deductions: '))
        erec = ()
        Id,passw,name,hiredate,dep,pos,ph = erec
        query = f'''insert into employees
        Values {erec};'''
        Cursor.execute(query)
        prec = ()
        Id,base,bonus,deductions = prec
        query='INSERT INTO PAYSLIPS'\
        f'VALUES {prec};'
        Cursor.execute(query)
        print('Record successfully inserted! ')
        admin_menu()
    elif ch1==5:
        uid = int(input('Enter employee id which is to be deleted: '))
        try:
            query = 'Delete from employees'\
            f'where Id={uid}'
            print('Record successfully deleted')
        except:
            print('Details not found')
    elif ch1==6:
        main_menu()
    elif ch1==7:
        login_menu()
    else:
        print('Invalid choice')
        admin_menu()
print('Welcome to Employee management project')
print('Made by Shreyas H Suvarna, Shahil Kumar,T Mouna Prasad and Alok Yadav')
print('To access admin features use one of the following ids or password: ')
print('id: 34634 password: &zZ)K9')
print('id: 24232 password:eEc5>>')
print('id: 54745 password=Rb9Y{')
login_menu()