import tkinter as tk
import password_manager_functions  


def secondWindow(fernet_key):
    command_window = tk.Tk()
    command_window.title("Password Manager")
    fernet_key = fernet_key
    text_output = tk.StringVar()
    text_output.set('')

    #Action of command button
    def command_action():
        command_listbox_selection = command_listbox.curselection()
        application_listbox_selection = application_listbox.curselection()

        if command_listbox_selection[0] == 1:
            command_output = password_manager_functions.Password_Viewer(fernet_key, application_listbox_selection[0])
            text_output.set(command_output)

        elif command_listbox_selection[0] == 0:
            application_name = application_name_entry.get()
            application_url = application_url_entry.get()
            application_username = application_username_entry.get()
            password_lenght = int(password_lenght_entry.get())

            password_manager_functions.CreatePassword(fernet_key, application_name, application_url, application_username, password_lenght)

    def autologin():
        application_listbox_selection = application_listbox.curselection()
        password_manager_functions.AutoLogin(fernet_key, application_listbox_selection[0])


    #Listbox Section
    #For Commands
    command_listbox = tk.Listbox(command_window, exportselection=0)
    command_listbox.insert(1, "Create Password")
    command_listbox.insert(2, "Password Viewer")
    command_listbox_selection = ()

    #For Applications Names
    application_listbox_selection = ()
    application_listbox = tk.Listbox(command_window, exportselection=0)
    application_list = password_manager_functions.Web_Selector()
    for i in range(len(application_list)):
        application_listbox.insert(i, application_list[i])
    
    #Parameter For Password Creation
    # Label Section
    application_name_label = tk.Label(command_window, text="Application Name")
    application_url_label = tk.Label(command_window, text="URL")
    application_username_label = tk.Label(command_window, text="Username")
    password_lenght_label = tk.Label(command_window, text="Size")

    #Entry Section
    application_name = tk.StringVar()
    application_name_entry = tk.Entry(command_window, textvariable=application_name)
    application_url = tk.StringVar()
    application_url_entry = tk.Entry(command_window, textvariable=application_url)
    application_username = tk.StringVar()
    application_username_entry = tk.Entry(command_window, textvariable=application_username)
    password_lenght = 0
    password_lenght_entry = tk.Entry(command_window, textvariable=password_lenght)

    #Output Section
    output_label = tk.Label(command_window, textvariable=text_output)

    #Button Section
    #Login Command Boutton
    login_button = tk.Button(command_window, text="LOGIN", command=autologin)

    #Command Execution Button
    command_button = tk.Button(command_window, text="OK", command=command_action)

    #Pack Section
    command_listbox.pack()
    application_name_label.pack()
    application_name_entry.pack()
    application_url_label.pack()
    application_url_entry.pack()
    application_username_label.pack()
    application_username_entry.pack()
    password_lenght_label.pack()
    password_lenght_entry.pack()
    application_listbox.pack()
    output_label.pack()
    command_button.pack()
    login_button.pack()
    command_window.mainloop()

#First window
master_window = tk.Tk()
master_window.title("Password Manager")

#Action of ok_button
def getEntryValue():
    entry_value = master_password_entry.get()
    fernet_key = password_manager_functions.fernetKeyCreation(entry_value)
    master_window.destroy()
    secondWindow(fernet_key)
        
#Text Section
master_label = tk.Label(master_window, text="Enter password :")

#Entry Section
entry_value = tk.StringVar()
master_password_entry = tk.Entry(master_window, textvariable=entry_value, text = "Enter password")


#Button Section
ok_button = tk.Button(master_window, command=getEntryValue, text="OK")

#Packing Section
master_label.pack()
master_password_entry.pack()
ok_button.pack()
master_window.mainloop()
