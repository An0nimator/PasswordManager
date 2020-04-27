from password_manager_functions import *
from user_configuration import *

#Bloc principale

# LOGIN
select = ""
print("S'identifier : A\n")
print("Creer un utilisateur : B\n")
while select != 'q':

    select = input("Commande : ") 
    if select == 'A':
        access, f, username = User_Verification()
        if access:
            select = ""
            print('Gestionnaire de mot de passe\n')
            print("Creer un mot de passe : 1\n")
            print("Autologin : 2\n")
            print("Password Viewer : 3\n")
            print("Password Remover : 4\n")
            print("Password Rewriter : 5\n")
            select = ""
            while select != 'q':
                select = input("Commande : ")
                if select == "1":
                    CreatePassword(f, username)
                    print("Mot de passe cree avec succes...")
                    pass
                elif select == "2":
                    if no_tab:
                        driver = webdriver.Firefox()
                        no_tab = False
                    AutoLogin(f, driver, username)
                    pass
                elif select == "3":
                    Password_Viewer(f, username)
                    pass
                elif select == "4":
                    Remove_Password(f, username)
                    pass
                elif select == "5":
                    Rewrite_Password(f, username)
                    pass
                elif select == 'q':
                    print('Fermeture application.')
                    pass
                else:
                    print("{} n'est pas une commande valide...".format(select))

              
    elif select == 'B':
          Create_A_New_User()
    


