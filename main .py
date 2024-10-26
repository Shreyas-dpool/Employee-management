import mysql.connector as mysql

# Get MySQL server details from the user
print("Enter your mySQL server details")
hostname = input('Hostname: ')
username = input('User: ')
password_input = input('Password: ')

# Establish connection to MySQL database
connection = mysql.connect(host=hostname, user=username, passwd=password_input)
connection.autocommit = True
cursor = connection.cursor()

# Use the specified database
cursor.execute("USE COMPANY;")

# Login Menu: Allows the user to log in and access different features based on their role
def login_menu():
    global user_id, user_password
    print("Welcome to employee management terminal!")
    print('1: Log in to access further features')
    print('2: Exit')
    choice = int(input('Enter choice: '))
    
    if choice == 1:
        # Input user credentials
        user_id = int(input('Enter your user id: '))
        user_password = input('Enter your password: ')
        query = f"SELECT * FROM EMPLOYEES WHERE Id = {user_id};"
        cursor.execute(query)
        record = cursor.fetchone()
        
        # Validate user password
        if record[1] == user_password:
            print("Successfully logged in!")
            print(f"Welcome back {record[2]}")
            
            # Check if the user is an admin
            if record[5].lower() == 'admin':
                print('Welcome back admin!')
                admin_menu()
            else:
                main_menu()
        else:
            print('User ID or password incorrect')
            login_menu()

# Main Menu: Provides different options for regular users
def main_menu():
    print('What would you like to do today?\n'
          '1. View Salary \n'
          '2: View other details\n'
          '3: Update your password\n'
          '4: View leave details\n'
          '5: Log Out') 
    user_choice = int(input('Enter your choice: '))
    
    if user_choice == 1:
        salary_menu()
    elif user_choice == 2:
        # Fetch and display user details
        query = f"SELECT * FROM EMPLOYEES WHERE Id = {user_id};"
        cursor.execute(query)
        record = cursor.fetchone()
        print('Your hire date is:', record[3])
        print('Your department is:', record[4])
        print('Your position is:', record[5])
        print('Your phone number is:', record[-1])
        main_menu()
    elif user_choice == 3:
        # Change user password
        entered_password = input('Enter your current password: ')
        if entered_password == user_password:
            new_password = input('Enter your new password: ')
            update_record("EMPLOYEES", 'Pass', new_password, user_id)
            print("Password successfully updated")
            main_menu()
        else:
            print('Wrong password entered!')
            main_menu()
    elif user_choice == 4:
        leave_menu()
    elif user_choice == 5:
        print('Successfully logged out')
        login_menu()
    else:
        print('Invalid choice')
        main_menu()

# Salary Menu: Allows users to view salary details
def salary_menu():
    print('''Salary information:
    1: View net salary
    2: View salary details
    3: Go back to main menu
    ''')
    salary_choice = int(input('Enter choice: '))
    
    if salary_choice == 1 or salary_choice == 2:
        # Fetch salary details
        query = f'SELECT Id, Base_amount, Bonus, Deductions, (Base_amount + Bonus - Deductions) FROM PAYSLIPS WHERE Id={user_id};'
        cursor.execute(query)
        salary_record = cursor.fetchone()
        
        if salary_choice == 1:
            print('Your net salary is:', salary_record[4])
        elif salary_choice == 2:
            print('Your base salary is:', salary_record[1])
            print('Your bonuses:', salary_record[2])
            print('Deductions from salary:', salary_record[3])
            print('Your net salary is:', salary_record[4])
        main_menu()
    elif salary_choice == 3:
        main_menu()
    else:
        print('Invalid choice')
        salary_menu()

# Leave Menu: Allows users to view or apply for leave
def leave_menu():
    global user_id
    print('Leave menu')
    print('1: View leave details')
    print('2: Apply for leave')
    leave_choice = int(input('Enter choice: '))
    query = f"SELECT * FROM E_LEAVE WHERE Id = {user_id};"
    cursor.execute(query)
    leave_record = cursor.fetchone()
    
    if leave_choice == 1:
        # Fetch and display leave details
        print('Your leave type is:', leave_record[1])
        print('Your leave duration is:', leave_record[2])
        print('Reason for leave:', leave_record[-1])
        print('Leave status:', leave_record[3])
        main_menu()
    elif leave_choice == 2 and user_id!='':
        #Checking if there is already an exisiting leave application
        if leave_record !=[] :
            print('Leave record already exists')
            main_menu()
        # Apply for leave
        else:
            leave_type = input('Enter your type of leave: ')
            leave_duration = int(input('Enter your leave duration: '))
            leave_reason = input('Enter your reason: ')
            leave_data = (user_id, leave_type, leave_duration, leave_reason)
            query = f"INSERT INTO E_LEAVE (Id, LeaveType, Duration, Reason) VALUES {leave_data};"
            print('Leave applied, wait for further notice if approved.')
            main_menu()
    else:
        print("Invalid choice")

# Update function to update database records
def update_record(table, attribute, value, Id):
    try: 
        if isinstance(value, int):
            query = f"UPDATE {table} SET {attribute}={value} WHERE Id={Id};"
        else:
            query = f"UPDATE {table} SET {attribute}='{value}' WHERE Id={Id};"
        cursor.execute(query)    
    except:
        print('Id or attribute not found')

# Admin Menu: Provides options for admins to manage employee details
def admin_menu():
    print('Welcome to admin menu')
    print('1: Update employee details')
    print('2: Change employee salaries')
    print('3: View employee leave details')
    print("4: Add a new employee's details")
    print('5: Delete an employee')
    print('6: Access other features')
    print('7: Log out')
    admin_choice = int(input('Enter your choice: '))
    
    if admin_choice == 1:
        # Update employee details
        update_id = int(input('Enter the id of the user you want to update: '))
        attribute_to_update = input('Enter the attribute to update (Id, Department, Position, Phone_no): ')
        new_value = input('Enter the new value: ')
        update_record('EMPLOYEES', attribute_to_update, new_value, update_id)
        admin_menu()
    elif admin_choice == 2:
        # Change employee salary details
        update_id = int(input('Enter the id of the user you want to update: '))
        salary_attribute_to_update = input('Enter the salary attribute to update (Base_amount, Deductions, Bonus): ')
        new_value = input('Enter the new value: ')
        update_record('PAYSLIPS', salary_attribute_to_update, new_value, update_id)
        print('Successfully updated')
        admin_menu()
    elif admin_choice == 3:
        # View employee leave details
        update_id = int(input('Enter the id of the user: '))
        query = f"SELECT * FROM E_LEAVE WHERE Id={update_id};"
        cursor.execute(query)
        leave_record = cursor.fetchone()
        print('Leave type:', leave_record[1])
        print('Leave duration:', leave_record[2])
        print('Reason for leave:', leave_record[-1])
        print('Leave status:', leave_record[3])
        
        # Option to update leave status
        if leave_record[3].lower() == 'pending':
            print('This leave application is pending, you can approve, deny or leave it pending')
            new_status = input('Enter current status: ')
            update_record('E_LEAVE', 'Status', new_status, update_id)
            print("Successfully updated")
        admin_menu()
    elif admin_choice == 4:
        # Add new employee details
        new_id = int(input('Enter new employee id: '))
        new_password = input('Enter password: ')
        new_name = input('Enter name: ')
        hire_date = input('Enter hire date: ')
        department = input('Enter department: ')
        position = input('Enter position: ')
        phone_number = input('Enter phone number: ')
        base_salary = int(input('Enter base salary: '))
        bonus_amount = int(input('Enter bonus: '))
        salary_deductions = int(input('Enter deductions: '))
        employee_record = (new_id, new_password, new_name, hire_date, department, position, phone_number)
        query = f"INSERT INTO employees VALUES {employee_record};"
        cursor.execute(query)
        payslip_record = (new_id, base_salary, bonus_amount, salary_deductions)
        query = f"INSERT INTO PAYSLIPS VALUES {payslip_record};"
        cursor.execute(query)
        print('Record successfully inserted!')
        admin_menu()
    elif admin_choice == 5:
        # Delete employee details
        delete_id = int(input('Enter employee id to delete: '))
        try:
            query = f"DELETE FROM employees WHERE Id={delete_id};"
            cursor.execute(query)
            print('Record successfully deleted')
        except:
            print('Details not found')
        finally:
            admin_menu()
    elif admin_choice == 6:
        main_menu()
    elif admin_choice == 7:
        login_menu()
    else:
        print('Invalid choice')
        admin_menu()

# Initial welcome message and login
print('Welcome to Employee Management System')
print('Developed by Shreyas H Suvarna, Shahil Kumar, T Mouna Prasad, and Alok Yadav')
print('To access admin features, use one of the following ids and passwords:')
print('id: 34634 password: &zZ)K9')
print('id: 24232 password: eEc5>>')
print('id: 54745 password: Rb9Y{')
login_menu()
input('Press Enter to exit')

# Close MySQL connection
connection.close()
