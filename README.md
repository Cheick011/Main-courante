# Main-courante
Application graphique de saisie de la Main courante sauvetage spéléo 

# Tutoriel d’installation Main-Courante 

Installation et configuration de Git 

## 1. Installation de Git 

Pour installer Git, exécutez la commande suivante dans le terminal : 

> sudo apt update && sudo apt install git 
 

## 2. Configuration de Git avec votre compte GitHub 

Une fois l’installation terminée, ouvrez un terminal et renseignez votre nom d’utilisateur ainsi que votre adresse e-mail : 

> git config --global user.name "VotreNom" 
> git config --global user.email "VotreEmail" 
 

 

## Création et ajout d’une clé SSH à GitHub 

#### 1. Génération d’une clé SSH 

Lancez la commande suivante afin de générer une clé SSH : 

> ssh-keygen -t rsa -b 4096 -C "VotreEmail" 
 

Appuyez sur la touche Entrée jusqu’à la fin de la génération de la clé. 

#### 2. Affichage de la clé publique 

Pour afficher la clé publique, utilisez la commande suivante : 

> cat ~/.ssh/id_rsa.pub 
 

Copiez ensuite le contenu affiché. 

#### 3. Ajout de la clé SSH sur GitHub 

Ajoutez la clé copiée dans les paramètres SSH de votre compte GitHub. 

Connectez-vous à GitHub 

Allez dans Paramètres > Clés SSH et GPG > Nouvelle clé SSH, collez la clé et sauvegardez. 

 

#### 4. Cloner le dépôt GitHub : 

Une fois configuré, clonez le projet avec la commande suivante : 

> git clone git@github.com:Cheick011/Main-courante.git
> cd Main-courante 
 

 

## Installer les dépendances 

Les dépendances nécessaires sont listées dans le fichier requirements.txt : 

> pip install -r requirements.txt 
 

 

## Description des répertoires et fichiers 

Voici une brève explication de l'organisation du projet : 

##### Répertoire data/ 

Contient les données telles que la structure de la base de donnée, les maquettes, les icones, etc . 

##### Répertoire html/ 

Stocke les fichiers web générés. 

##### Répertoire Main-courante/ 

Contient le code source du programme, organisé en modules. 

Chaque module réalise une tâche spécifique, comme Authentifier un utilisateur, envoie les données, etc. 

#### Lien entre les fichiers et répertoires 

Le fichier principal Maincourante.py exécute le module login.py une fois exécutée ce qui permet à l’utilisateur de s’authentifier et commencer à utiliser l’application. 

 

## Exécution du programme 

Lancez le programme en spécifiant les fichiers d'entrée et le répertoire de sortie : 

> cd Maincourante 
> python3 Maincourante.py 

Cela va lancer la page d’authentification. 

#### NB : Ce projet est documenté avec Sphinx. 

 

 
