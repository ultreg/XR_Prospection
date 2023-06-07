
# Project Title

A brief description of what this project does and who it's for

- Objective:

XR_ProspectDataScraper aims to scrape data from a website into a csv file.

Here, employers who are committed to road safety can be contacted to be offered an innovative offer in terms of prevention.

The graphical interface allows the end user to launch scrapping on an occasional basis and then compare the employers who have joined or left the process.

(in French below)

- Objectif:

XR_ProspectDataScraper vise à récupérer les données d'un site Web afin d'obtenir un fichier csv.

Ici, les employeurs qui se sont engagés pour la sécurité routière peuvent être contactés pour se voir proposer une offre innovante en matière de prévention.

L'interface graphique permet à l'utilisateur final de lancer un scrapping de façon épisodique puis de comparer les fichiers, afin de voir les employeurs qui ont rejoint ou ont quitté la démarche.
## Acknowledgements

 - Special thanks to Alexandre Nabyt for his help [@Sestere-IA](https://github.com/Sestere-IA)

## Authors



- [@Sestere-IA](https://github.com/Sestere-IA)
- [@ultreg](https://github.com/ultreg)
## Current Functionality

- lancement d'un nouveau scrapping
- comparaison de fichiers csv
- enregistrement dans un dossier de l'ordinateur
## Installation

Install Google Chrome on your computer and create a shortcut of main.exe on your desktop.

Installer Google Chrome sur votre ordinateur et créer un racourci de main.exe sur votre bureau.
## Color Reference

| Color             | Hex                                                                |
| ----------------- | -------------------------------------------------------------------------------------- |
| Orange | ![#ED8B00](https://via.placeholder.com/10/ED8B00?text=+) #ED8B00 |
| Gris | ![#5B6770](https://via.placeholder.com/10/5B6770?text=+)  #5B6770 |



## About me

I'm a Data analyst and I am interested in development in Python and SQL request. https://www.linkedin.com/in/gr%C3%A9goire-ultr%C3%A9/
## Skills

All my skills in https://www.linkedin.com/in/gr%C3%A9goire-ultr%C3%A9/ 
## Feedback

If you have any feedback, please reach out to us at gregoire.ultre@gmail.com.


## Création d'un .exe

- Copier en local les scripts Python et les adapter à votre projet de scrapping.

- Dans ProspectDataScrapper : supprimer les dossiers build et dist et le fichier main. spec s'ils existent.

- Ouvrir l'invite de commande en mode administrateur.

- Installer pyinstaller : pip install pyinstaller

- Installer auto-py-to-exe : pip install auto-py-to-exe

- Exécuter auto-py-to-exe depuis le dossier du projet concerné.

- Emplacement des scripts : emplacement de main.py

- Console windows : maintenir la présence de la console tant que la fenêtre de débug est nécessaire.

- Fichiers additionnels : ajout des dossiers CSV, dataset, Différence, Final CSV et ajout des logos utilisés.

- Paramètres : spécifier un output dans répertoire de sortie, bien que l'output puisse se retrouver dans un dossier dist.

- Copier-coller la commande dans votre console PyCharm et exécuter.

- Ajouter les settings dans les "datas" de main.spec et relancer main.spec depuis la console : pyinstaller main.spec

- Source :
stackoverflow.com/questions/75308876/error-after-running-exe-file-originating-from-scrapy-project/75313625#75313625
- Vérifier la compatibilité sur votre ordinateur et sur un autre ordinateur avant de supprimer la fenêtre de débug.
