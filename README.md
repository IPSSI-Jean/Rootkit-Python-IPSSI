# Ransomware-Python-IPSSI

![CAPTURE](https://zupimages.net/up/22/48/d9jr.png)

**Ce Rootkit a été réalisé dans le cadre pédagogique de l'IPSSI sur un projet d'1,5 jours.**

# Prérequis
- Visual studio code

- Python3

- Connaissances basique / intermédiaire en Python

# Fonctionnement du projet

Le projet répartis sur 2 fichiers : ```Client-Victime.py``` et ```Serveur-Attaquant.py```, il utilise un fichier ```test.txt``` contenant du texte pour tester l'exfiltration de données.

- Exécution du code sur le serveur PUIS
- Exécution du code sur l'ordinateur de la victime, ce qui initialise la connexion avec le serveur
- Plusieurs commandes possibles depuis le serveur attaquant : 
  - Shell : Pour avoir accès au shell de la victime
  - Exit : Arrête le malware coté victime
  - Recv archive : Télécharge des fichiers depuis la victime.
  - Help : Liste les commandes possibles

# Axes d'améliorations du code
Après la phase de réalisation du projet, le professeur nous a demandé une personnalisation du code afin d'améliorer ce dernier.

Pour ce projet, les améliorations suivantes ont été mises en place :

- ...

# Environnement de travail

Il est recommandé d'exécuter ce programme dans un environnement virtuel, il est possible d'en mettre un en place à l'aide des logiciels suivants : 
- Virtualbox
- VMWare workstation pro
- ...

# Auteur

Auteur du projet : Jean O.

Version stable : ```1.0```

# Licence

Ce projet est à but éducatif, il n'est soumis à aucune licences.
