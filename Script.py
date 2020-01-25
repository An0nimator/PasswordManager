#IMPORTANT/COOL FEATURES TO ADD : USE ENCRYPTED PASSWORD
from selenium import webdriver
from random import randint
import time
from tkinter import *
from cryptography.fernet import Fernet

#key = b'ZvaLZr4dSzCXD67SB_oa7V93igIsN_X4iVbPgrZfWSM='

def CreatePassword(fe):

    ferne = Fernet(fe.encode())
    password_file = open('data.txt', "a")
    website = input("A quelle site souhaiteriez vous affiler votre mot de passe : ")
    website_url = input("Saisissez son url : ")
    website_login = input("Entrez votre identifiant : ")
    dictionnaire = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!§:/;.,?*%^¨$"
    password_lenght = input("Veuillez entrer la longueur du mot de passe : ")
    password_lenght = int(password_lenght)
    password = []
    i=0

    #Creation du mot de passe 
    while i < password_lenght:
        selector = randint(0,len(dictionnaire)-1)
        password.append(dictionnaire[selector])
        i+=1

    #Encyption du password
    temporar_password = ''.join(password)
    temporar_password = temporar_password.encode()
    encrypted_password = ferne.encrypt(temporar_password)
    
    #Ecriture des données dans le fichier data.txt
    password_file.write("\n{}, {}, {}, {},".format(website, website_url, str(encrypted_password), website_login)) #''.join(password) au cas ou
    password_file.close()

def AutoLogin(fe):
    #Ouverture du fichier data.txt
    fernet = Fernet(fe.encode())
    password_file = open('data.txt', "r")
    password_Flist = [password_file.read()]
    password_Flist = ",".join(password_Flist)
    password_Flist = password_Flist.split(",")
    password_list = []

    # Crée une liste avec tout les mots de passe 
    i=0
    a=2
    while i < len(password_Flist):
        if i==a:
            a+=4
            password_list.append(password_Flist[i].replace(" ", ""))
            pass
        i+=1

    # Crée une liste avec tout les noms des applications
    b=0
    c=4
    website_list = []
    while b < len(password_Flist):
        if b == c:
            c+=4
            website_list.append(password_Flist[b].replace("\n", ""))
            pass
        elif b==0:
            website_list.append(password_Flist[b])
            pass
        b+=1
    if website_list[len(website_list)-1] == '':
        del website_list[len(website_list)-1]
        pass
    

    # Crée une liste contenant les urls
    url_list = []
    e = 0
    f = 1
    while e < len(password_Flist):
        if e == f:
            f+=4
            url_list.append(password_Flist[e].replace(" ", ""))
            pass
        e+=1

    #Crée une liste avec tout les identifiants
    login_list = []
    g = 0
    h = 3
    while g < len(password_Flist):
        if g == h:
            h+=4
            login_list.append(password_Flist[g].replace(" ", ""))
            pass
        g+=1

    # Affichage de selection des applications
    d = 0
    while d < len(website_list):
        print("{} : {}".format(d,website_list[d]))
        d+=1
        
    website_choice = int(input("Choix : "))

    #Liste des id possibles 
    list_id = ["email", "username", "user", "id_login", "input_username", "login_mail"]
    list_pass = ["password", "id_password", "input_password", "login_password"]

    #Creation de l'objet webdriver
    driver = webdriver.Firefox()
    your_url = url_list[website_choice]
    driver.get(your_url)
    """
    print("Attente du chargement total de la page...")
    time.sleep(15)
    print("Chargement de la page terminée.")
    """
    #Test des id elements pour les identifiants
    error = True
    i = 0
    while error:
        try:
            identifiant_id = driver.find_element_by_id(list_id[i])
            pass
        except :
            print("")
            i+=1
            pass
        else:
            error = False
            pass
        pass

    #Test des id elements pour les passwords
    error = True
    i = 0
    while error:
        try:
            password_id = driver.find_element_by_id(list_pass[i])
            pass
        except :
            print("")
            i+=1
            pass
        else:
            error = False
            pass
        pass


    #Creation des données à envoyer au sites
    your_login = login_list[website_choice]
    password = password_list[website_choice].replace(" ", "")
    password = password.encode()                 #Transforme str en byte
    your_password = fernet.decrypt(password[2:]) #Decryptage du mot de passe

     #Envoie les données au site
    identifiant_id.send_keys(your_login)
    password_id.send_keys(your_password.decode())

#Bloc principale 

print('Gestionnaire de mot de passe\n')
encrypt_key = input("Entrez la clé cryptographique : \n")
#f = Fernet(encrypt_key.encode())
print("Creer un mot de passe : 1\n")
print("Autologin : 2\n")
select = ""
while select != 'q':
    select = input("Commande : ")
    if select == "1":
        CreatePassword(encrypt_key)
        print("Mot de passe cree avec succes...")
        pass
    elif select == "2":
        AutoLogin(encrypt_key)
        pass
    elif select == 'q':
        print('Fermeture application.')
        pass
    else:
        print("{} n'est pas une commande valide...".format(select))
