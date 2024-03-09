
# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

#=====importing libraries===========

import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass

with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


# Creating a dictionary with tasks components and appends to a list called 'task_list'
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = "Yes" if task_components[5] == "Yes" else "No"

    task_list.append(curr_t)


#====Login Section====
# The code is a Python script that reads usernames and passwords from a file named
# user.txt to allow a user to login.
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r', encoding="utf-8") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password
    


#User login and checking password
def log_in():
    """
    The function 'log_in' allows a user to log in with a username and password,
    checking against a dictionary of username-password pairs.
    """
    LOGGED_IN = False
    while not LOGGED_IN:

        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("\nLogin Successful!\n")
            LOGGED_IN = True
    if(LOGGED_IN):
        return curr_user
    else:
        log_in()



def main():
    """
    The main function presents a menu to the user for registering a user, adding a
    task, viewing tasks, generating reports, displaying statistics, or exiting the
    program.
    """
    curr_user = log_in()
    
    while True:
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()
        if menu == 'r':
            reg_user()
        elif menu == 'a':
            add_task()
        elif menu == 'va':
            view_all()
        elif menu == 'vm':
            view_mine(curr_user)
        elif menu == 'gr':
            generate_reports()
        elif menu == 'ds':
            display_stat(curr_user)
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("\nYou have made a wrong choice, Please Try again\n")



def reg_user():
    """
    The 'reg_user' function adds a new user to the user.txt file after taking 
    input for username, password, and confirming the password.
    """
    # - Request input of a new username
    new_username = input("New Username: ")
    # - Checking if the input username already exists 
    if new_username in username_password.keys():
        print("\nUsername Already exist! Please enter a different username!\n")
        reg_user()
    else:
        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("\nNew user added\n")
            username_password[new_username] = new_password
            
            with open("user.txt", "w",encoding="utf-8") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            print("\nUser registered successfully!\n")

        # - Otherwise you present a relevant message.
        else:
            print("\nPasswords do no match\n")



def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("\nUser does not exist. Please enter a valid username\n")
            continue
        else:
            break
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("\nInvalid datetime format. Please use the format specified\n")


    # Then get the current date.
    curr_date = date.today()
    #creating the new task dictionary with all the componets input got from user
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # Append the dictionary to the task_list list and write the task_list
    # To the tasks file
    task_list.append(new_task)

    # Finally, task information is written to the tasks file with each task on a new line.
    with open("tasks.txt", "w",encoding="utf-8") as file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed']=="Yes" else "No"
            ]
            task_list_to_write.append(";".join(str_attrs)) 
        file.write("\n".join(task_list_to_write))
    print("\nTask successfully added.\n")



def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
    print("-"*50)
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Complete: \t {t['completed']}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print("\n",disp_str)
        print("-"*50)



def view_mine(curr_user):
    """
    The 'view_mine' function displays tasks assigned to the current user, allows the
    user to select a task to mark as complete or edit, and writes the modified task
    list to a file.
    """
    # Display tasks assigned to the current user
    task_counter=0
    print("-"*50)
    for t in task_list:
        if t['username'] == curr_user:
            task_counter+=1
            disp_str = f"Task number: \t{task_counter}\n"
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Complete: \t {t['completed']}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print("\n",disp_str)
            print("-"*50)
            
    # If the user has no tasks in the task_list
    if task_counter == 0:
        print("-"*50)
        print("\nYou have no tasks assigned.\n")
        print("-"*50)
        return
    
    # When the user has tasks in the task_list,
    #Prompt the user to select a task
    try:
        task_select = int(input("Enter a task number or enter any other number to return to the main menu: "))
        
        # Process the selected task to do either Mark the task as complete or edit 
        # The task's usename or due_date
        curr_task_counter = 0
        for t in task_list:
            if t['username'] == curr_user:
                curr_task_counter+=1
                if task_select == curr_task_counter:
                    select = input("Do you want to mark as complete or edit the task? (enter 'mark' or 'edit'): ").lower()
                    if select == "mark":
                        t['completed'] = "Yes"
                        print("-"*50)
                        print("\nTask marked as complete.\n")
                        print("-"*50)
                    elif select == "edit":
                        edit_select = input("What do you want to edit? (enter 'username' or 'due_date'): ").lower()
                        if edit_select == "username":
                            # Checking whether new username is in the user list or
                            while True:
                                update_username = input("Enter a new username: ")
                                if update_username in username_password.keys():
                                    t['username'] = update_username                                
                                    print("-"*50)
                                    print("\nUsername updated.\n")
                                    print("-"*50)
                                    break
                                else:
                                    print("\nAlert! Username Invalid!\n")
                                    continue
                        elif edit_select == "due_date":
                            new_due_date_str = input("Enter a new due_date (YYYY-MM-DD): ")
                            new_due_date = datetime.strptime(new_due_date_str, DATETIME_STRING_FORMAT)
                            t['due_date'] = new_due_date
                            print("-"*50)
                            print("\nDue date updated.\n")
                            print("-"*50)
                        else:
                            print("\nPlease check your option spelling!\n")
                    else:
                        print("\nPlease check your choice spelling!\n")

        # Write the modified task list to the "tasks.txt" file
        with open("tasks.txt", "w",encoding="utf-8") as t_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] == "Yes" else "No"  # Ensure to write "Yes" or "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            t_file.write("\n".join(task_list_to_write))
    except ValueError:
        print("\nInvalid choice!\n")



def generate_reports():
    '''Generate 'task_overview.txt' and 'user_overview.txt' with the 
    task and user reports with spacing and labelling
    '''
    # Defining all the variables needed for this function
    overdue_count = 0
    complete_count = 0
    incomplete_count =0
    incomplete_percent=0
    overdue_percent=0
    tasks_percent =0
    user_complete_percent = 0
    user_incomplete_percent =0

    num_tasks = len(task_list)
    num_users = len(username_password.keys())
    print("\nReports generated successfully!\n")



    def count_calculate(t_list):
        ''' This function calculates the number of completed and incomplete tasks 
        by iterating through a list of tasks and counting the number of tasks 
        that are marked as completed ("yes") and the number
        of tasks that are marked as incomplete ("no")'''

        complete_count = 0
        incomplete_count = 0
        for task in t_list:
            if task["completed"] == "Yes":
                complete_count += 1
            elif task["completed"] == "No":
                incomplete_count += 1

        return complete_count, incomplete_count
    


    def overdue_check(task):
        """
        The `overdue_check` function determines if a task is overdue based on its
        due date and completion status.
        """
        # Get the current date
        current_date = datetime.now().date()
        task_due_date = task["due_date"].date()

        # Check if the due date of the task is before the current date
        if task_due_date < current_date and task["completed"] == "No":
            return True  # Task is overdue
        else:
            return False  # Task is not overdue


   # This code is creating a task overview report and writing it to a
   # file named "task_overview.txt".
    with open("task_overview.txt", 'w',encoding="utf-8") as fp:
        if num_tasks>0:
            complete_count, incomplete_count = count_calculate(task_list)
            overdue_count = 0
            for t in task_list:
                if overdue_check(t) :
                    overdue_count += 1

            incomplete_percent = round((incomplete_count/num_tasks)*100)
            overdue_percent = round((overdue_count/num_tasks)*100)
        else:
            print("You have zero tasks!")

        # Writing all the task overview report 
        fp.write(f"{'='*22} TASK OVERVIEW {'='*22}\n\n")
        fp.write(f"Number of tasks: \t\t\t {num_tasks}\n")
        fp.write(f"Number of completed tasks: \t\t {complete_count}\n")
        fp.write(f"Number of incomplete tasks: \t\t {incomplete_count}\n")
        fp.write(f"Number of overdue tasks: \t\t {overdue_count}\n")
        fp.write(f"Percentage of incomplete tasks:\t\t {incomplete_percent}%\n")
        fp.write(f"Percentage of overdue tasks: \t\t {overdue_percent}%\n")

    # Generating user overview report and writing it to user_overview text file
    # By iterating through username from user text file and comparing 
    # To task_list to generate report for each user
    with open("user_overview.txt", 'w',encoding="utf-8") as fp:
        fp.write(f"{'='*22} USER OVERVIEW {'='*22}\n\n")
        fp.write(f"Number of users: \t\t {num_users}\n")
        fp.write(f"Number of tasks: \t\t {num_tasks}\n")
        fp.write(f"Number of completed tasks: \t {complete_count}\n")
        fp.write(f"Number of incomplete tasks: \t {incomplete_count}\n\n")

        for t_user in username_password.keys():
            t_count=0
            complete_count=0
            incomplete_count=0
            overdue_count=0
            for t in task_list:
                if t["username"]== t_user:
                    t_count+=1
                    if t["completed"].lower() == "yes":  
                        complete_count += 1
                    elif t["completed"].lower() == "no":
                        incomplete_count += 1    
                    if overdue_check(t):
                        overdue_count += 1

            # The above code is calculating and writing an overview of task
            # statistics for a specific user to a file. It first checks if the
            # number of tasks assigned to the user is greater than 0. If so, it
            # calculates the percentage of total tasks, completed tasks,
            # incomplete tasks, and overdue tasks for that user. It then writes
            # this information to a file. If the user has zero tasks, it simply
            #  writes zero tasks to the file
            if t_count > 0:
                fp.write(f"{'-'*22} OVERVIEW for user {t_user} {'-'*22}\n\n")
                fp.write(f"The assigned number of tasks: \t\t\t {t_count}\n")

                tasks_percent = round((t_count/num_tasks)*100)
                fp.write(f"The percentage of total number of tasks : \t {tasks_percent}%\n")

                user_complete_percent = round((complete_count/t_count)*100)
                fp.write(f"The percentage of tasks that are completed : \t {user_complete_percent}%\n")

                user_incomplete_percent = round((incomplete_count/t_count)*100)
                fp.write(f"The percentage of tasks that are incomplete : \t {user_incomplete_percent}%\n")

                user_overdue_percent = round((overdue_count/t_count)*100)
                fp.write(f"The Percentage of overdue tasks: \t\t {user_overdue_percent}%\n\n")
            else:
                fp.write(f"{'-'*22} OVERVIEW for user {t_user} {'-'*22}\n\n")
                fp.write(f"The assigned number of tasks: \t\t\t {0}\n")
                fp.write(f"The percentage of total number of tasks : \t {0}%\n")
                fp.write(f"he percentage of tasks that are completed : \t {0}%\n")
                fp.write(f"The percentage of tasks that are incomplete : \t {0}%\n")
                fp.write(f"The Percentage of overdue tasks: \t\t {0}%\n\n")



def  display_stat(curr_user):
    """
    The function 'display_stat' reads and prints the contents of two text files if
    the current user is "admin", otherwise it prompts the user to switch to admin
    user. If the text files not found, it asks the user if they would want to
    generate the files and if they say yes,it calls the generate_reports file and
    display the statistics to the screen.
    """

    while True:
        try:
            if curr_user == "admin":
                with open ("task_overview.txt","r",encoding="utf-8") as file:
                    file = file.read()
                    print(file)
                with open ("user_overview.txt","r",encoding="utf-8") as file:
                    file =file.read()
                    print(file)
                    break
            else:
                print("Only Admin can display statistics. Please change into admin user!")
                break
        except FileNotFoundError:
            print("You have not generated reports yet!!!")
            choice = input("Do you want to generate it now? Y/N :")
            if choice == "yes":
                generate_reports()
                continue
            elif choice == "no":
                main()
        
    

if __name__ == "__main__" :
    main()
