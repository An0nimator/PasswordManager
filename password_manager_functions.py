from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from random import randint
import time
from tkinter import *
from cryptography.fernet import Fernet
import base64
import os

def CreatePassword(f, username):
    password_file = open(username, "a")
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
    encrypted_password = f.encrypt(temporar_password)
    
    #Ecriture des données dans le fichier data.txt
    password_file.write("\n{}, {}, {}, {},".format(website, website_url, encrypted_password.decode(), website_login)) #''.join(password) au cas ou
    password_file.close()

def AutoLogin(f, driver, username):
    #Ouverture du fichier data.txt
    password_file = open(username, "r")
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

    # Affichage de selection des applications
    d = 0
    while d < len(website_list):
        print("{} : {}".format(d,website_list[d]))
        d+=1
        
    website_choice = int(input("Choix : "))

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

def Password_Viewer(f, username):
    #Ouverture du fichier data.txt
    password_file = open(username, "r")
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
            website_list.append(password_Flist[b].replace("\n",""))
            pass
        b+=1
    if website_list[len(website_list)-1] == '':
        del website_list[len(website_list)-1]
        pass
    
    # Affichage de selection des applications
    d = 0
    while d < len(website_list):
        print("{} : {}".format(d,website_list[d]))
        d+=1
        
    website_choice = int(input("Choix : "))
    
    password = password_list[website_choice].replace(" ", "")
    password = password.encode()             #Transforme str en byte
    try:
        your_password = f.decrypt(password) #Decryptage du mot de passe
    except:
        print("Vous n'avez pas le mot de passe maitre permettant le decodage...")
        return
        

    print("Votre mot de passe : ", your_password.decode())
    return password_list[website_choice]

def Remove_Password(f, username):
    #Ouverture du fichier data.txt
    password_file = open(username, "r")
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
    with open(username, "r") as password_file:
        lines = password_file.readlines()
        password_file.close()
    with open(username, "w") as password_file:          
        for line in lines:
            if line != lines[website_choice]:
                password_file.write(line)
    print("Le mot de passe a bien été supprimé.")

def Rewrite_Password(f, username):
    encoded_password_to_change = Password_Viewer(f)
    changed_password = f.encrypt(input("Entrez le mot de passe de rechange : ").encode())
    fichier = open(username, "rt")
    data = fichier.read()
    data = data.replace(encoded_password_to_change, changed_password.decode())
    fichier.close()

    fichier = open(username, "wt")
    fichier.write(data)
    fichier.close()
    

