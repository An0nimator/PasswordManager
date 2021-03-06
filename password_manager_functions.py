from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
import time
from tkinter import *
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os

def CreatePassword(f, application_name, application_url, application_username, password_lenght):

    password_file = open('data.txt', "a")
    dictionnaire = "abcdefghijklmnopqrstuvwxyz01234567890123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!§:/;.,?*%^¨$"
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
    encrypted_password = f.encrypt(temporar_password)
    
    #Ecriture des données dans le fichier data.txt
    password_file.write("\n{}, {}, {}, {},".format(application_name, application_url, encrypted_password.decode(), application_username)) #''.join(password) au cas ou
    password_file.close()

def AutoLogin(f, website_choice):
    driver=webdriver.Firefox()
    #Ouverture du fichier data.txt
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
    k = 1
    while e < len(password_Flist):
        if e == k:
            k+=4
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

    #Liste des id possibles, en rajouter selon le site web utilisé 
    list_id = ["email", "username", "Username", "user", "id_login", "input_username", "login_mail", "g_cn_cod", "login-username", "login_field"]
    list_pass = ["password", "Password", "id_password", "input_password", "login_password", "g_cn_mot_pas", "login-password"]
    your_url = url_list[website_choice]
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
    driver.get(your_url)

    #Test des id elements pour les identifiants
    error = True
    i = 0
    while error:
        if i > len(list_id):
            print("List Id Error")
            return
        try:
            identifiant_id = driver.find_element_by_id(list_id[i])
            pass
        except :
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
            if i > len(list_pass):
                print("List Pass Error")
                return
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
    your_password = f.decrypt(password) #Decryptage du mot de passe

    #Envoie les données au site
    identifiant_id.send_keys(your_login)
    password_id.send_keys(your_password.decode())

def Password_Viewer(f, website_choice):
    #Ouverture du fichier data.txt
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
        
    password = password_list[website_choice].replace(" ", "")
    password = password.encode()             #Transforme str en byte
    try:
        your_password = f.decrypt(password) #Decryptage du mot de passe
    except:
        print("Vous n'avez pas le mot de passe maitre permettant le decodage...")
        return

    return your_password.decode()

def Web_Selector():
    #Ouverture du fichier data.txt
    password_file = open('data.txt', "r")
    password_Flist = [password_file.read()]
    password_Flist = ",".join(password_Flist)
    password_Flist = password_Flist.split(",")
    password_list = []

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
            website_list.append(password_Flist[b].replace("\n",""))
            pass
        b+=1
    if website_list[len(website_list)-1] == '':
        del website_list[len(website_list)-1]
        pass

    return website_list


def Change_Password(f):
    
    #Ouverture du fichier data.txt
    password_file = open('data.txt', "rt")
    password_Flist = [password_file.read()]
    password_Flist = ",".join(password_Flist)
    password_Flist = password_Flist.split(",")
    password_list = []

    # Crée une liste avec tout les mots de passe decryptés
    i=0
    a=2
    while i < len(password_Flist):
        if i==a:
            a+=4
            password = password_Flist[i].encode()
            password_list.append(f.decrypt(password))
            pass
        i+=1

    # Réecrit les mots de passes dans le fichier data
    new_password = input("Entrez votre nouveau mot de passe : ").encode()
    salt = b'156'
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=1000,
    backend=default_backend()
)
    key = base64.urlsafe_b64encode(kdf.derive(new_password))
    f = Fernet(key)
    password_file.close()
    i=2
    a=0
    with open("data.txt") as file:
        while a < len(password_list):
            new_encrypted_password = f.encrypt(password_list[a])
            new_encrypted_password = new_encrypted_password.decode()
            newText = file.read().replace(password_Flist[i], new_encrypted_password)
            a+=1

    with open("data.txt", "w") as file:
        file.write(newText)

    print("Le mot de passe maitre a bien été changé.")

def Remove_Password(f):
    #Ouverture du fichier data.txt
    password_file = open('data.txt', "r")
    password_Flist = [password_file.read()]
    password_Flist = ",".join(password_Flist)
    password_Flist = password_Flist.split(",")
    password_list = []

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
            website_list.append(password_Flist[b].replace("\n",""))
            pass
        b+=1
    if website_list[len(website_list)-1] == '':
        del website_list[len(website_list)-1]
        pass
    
    password_file.close()

    # Affichage de selection des applications
    d = 0
    while d < len(website_list):
        print("{} : {}".format(d,website_list[d]))
        d+=1
        
    website_choice = int(input("Choix : "))

    # Crée une liste avec tout les mots de passe 
    i=0
    a=2
    while i < len(password_Flist):
        if i==a:
            a+=4
            password_list.append(password_Flist[i].replace(" ", ""))
            pass
        i+=1

    #Essaye d'ouvrir un mot de passe pour voir si la clé est la bonne
    try:
        f.decrypt(password_list[1].encode())
    except:
        print("Vous ne possedez pas le mot de passe permettant de réaliser cette action !") 
        return None
    with open("data.txt", "r") as password_file:
        lines = password_file.readlines()
        password_file.close()
    with open("data.txt", "w") as password_file:          
        for line in lines:
            if line != lines[website_choice]:
                password_file.write(line)
    print("Le mot de passe a bien été supprimé.")

def Rewrite_Password(f):
    encoded_password_to_change = Password_Viewer(f)
    changed_password = f.encrypt(input("Entrez le mot de passe de rechange : ").encode())
    fichier = open("data.txt", "rt")
    data = fichier.read()
    data = data.replace(encoded_password_to_change, changed_password.decode())
    fichier.close()

    fichier = open("data.txt", "wt")
    fichier.write(data)
    fichier.close()

#def Forgot_Password(f):

def fernetKeyCreation(master_password):
    salt = b'156'
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=1000,
    backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    f = Fernet(key)
    return f

