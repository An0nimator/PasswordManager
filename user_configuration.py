from cryptography.fernet import Fernet
import base64
from os import urandom
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json
import os

def Create_A_New_User():
    # Nom du compte
    name = input("Entrez votre nom : ")
    # Mail du compte
    email = input("Entrez votre email : ")
    # Mot de passe du compte
    master_password = input("Entrez votre mot de passe maitre : ")
    # Passe le mdp de str a bytes
    master_password = master_password.encode()
    # Création de la clé 
    salt = urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1000,
        backend=default_backend()
    )
    no_tab = True
    key = base64.urlsafe_b64encode(kdf.derive(master_password))
    f = Fernet(key)
    # Encryption du mot de passe compte à l'aide de la clé
    master_password_encrypted = f.encrypt(master_password)

    # Ecriture des données comptes dans fichier JSON
    # Si le fichier n'existe pas
    if not os.path.exists("user_config.json"):
        user = {
            "user":{
            'name':[name], 
            "email":[email], 
            "key":[key.decode()], 
            "mp_encrypted":[master_password_encrypted.decode()]}
        }
        with open('user_config.json', 'a') as fichier:
            json.dump(user, fichier)

    # Si celui-ci existe
    else:
        with open('user_config.json') as fichier:
            data = json.load(fichier)
            print(data)
                             
        data['user']['name'].append(name)
        data['user']['email'].append(email)
        data['user']['key'].append(key.decode())
        data['user']['mp_encrypted'].append(master_password_encrypted.decode())

        os.remove('user_config.json')
        
        with open('user_config.json', 'a')as fichier:
            json.dump(data, fichier)
            
def User_Verification():
    name = input("Entrez votre nom : ")
    master_password = input("Entrez votre mot de passe maitre : ")

    # Ouvre et récupere les données du JSON
    with open('user_config.json') as fichier:
        data = json.load(fichier)
    
    # Retorune des listes extraite de ces données
    keys = data['user']['key']
    usernames = data['user']['name']
    mps_encrypted = data['user']['mp_encrypted']

    # Retourne l'indice de l'utilisateur
    for username in usernames:
        if username == name:
            user_index = usernames.index(username)
            username = name
            break
            
    # Utilise la clé de de l'utilisateur
    key = keys[user_index].encode()
    f = Fernet(key)
    mp_encrypted = f.encrypt(master_password.encode())
    user_mp_encrypted = data['user']['mp_encrypted'][user_index].encode()

    # Compare les mot de passes
    if f.decrypt(mp_encrypted) == f.decrypt(user_mp_encrypted) and username == name:
        print("Acces autorisé")
        return True, f, username
        
    else:
        print("Vos identifiants sont incorrects")
        return False

