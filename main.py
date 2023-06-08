"""
A brief description of what this project does and who it's for

Objective:
XR_ProspectDataScraper aims to scrape data from a website into a csv file.

Here, employers who are committed to road safety can be contacted to be offered
an innovative offer in terms of prevention.

The graphical interface allows the end user to launch scrapping on an occasional basis and then compare the employers
who have joined or left the process.

(in French below)

Objectif:
XR_ProspectDataScraper vise à récupérer les données d'un site Web afin d'obtenir un fichier csv.

Ici, les employeurs qui se sont engagés pour la sécurité routière peuvent être contactés pour se voir proposer
une offre innovante en matière de prévention.

L'interface graphique permet à l'utilisateur final de lancer un scrapping de façon épisodique puis de comparer
les fichiers, afin de voir les employeurs qui ont rejoint ou ont quitté la démarche.
"""
import tkinter
import os
import shutil
import threading
import pandas as pd
import subprocess
import winreg
import socket
from tkinter import messagebox
from back_end_scrapp_and_compare import ScrappListEmployeEngage
from datetime import datetime


def start_window(app):
    """fenêtre de démarrage avec deux boutons pour scrapper le site ou comparer deux fichiers de résultats"""
    btn_scrapping = tkinter.Button(app, text="Scanner", bg="#ED8B00", command=lambda: scrapper(app))
    btn_scrapping.place(x=100, y=75, width=200, height=100)
    btn_compare = tkinter.Button(app, text="Comparer", bg="white", command=lambda: file_choice(app))
    btn_compare.place(x=100, y=225, width=200, height=100)


def show_error_window(entry=""):
    """message d'erreur"""
    messagebox.showerror("Atention!", "Ceci n'est pas un chemin correct pour enregistrer le document!")
    try:
        entry.delete(0, tkinter.END)
    except:
        pass


def scrapper(app):
    """lancement du scrapping. La connexion à internet n'est vérifiée que dans ce cas."""
    is_connected()
    loading(app, message="Scrapping en cours...")
    ScrappListEmployeEngage()
    app.update()
    registration("Final CSV", app)


def loading(app, message="Scrapping en cours..."):
    """Les deux boutons de démarrage sont effacés et l'interface nous indique qu'un scrapping est en cours."""
    for widget in app.winfo_children():
        widget.destroy()
    lb = tkinter.Label(app, text=message, font=100)
    lb.place(x=100, y=150, width=200, height=100)
    app.update()


def registration(source_dir, app):
    """Fenêtre d'enregistrement du fichier scrappé ou du fichier de comparaison."""
    for widget in app.winfo_children():
        widget.destroy()
    lb = tkinter.Label(app, text="Indiquez où vous voulez \n mettre votre fichier.", font=100, bg="#5B6770",
                       fg='white')
    lb.place(x=50, y=50, width=300, height=100)
    entry_path_file = tkinter.Entry(app, width=200)
    entry_path_file.place(x=50, y=150, width=300, height=30)
    btn_validation_path = tkinter.Button(app, text="valider", bg="green",
                                         command=lambda: get_path(entry_path_file, source_dir, app))
    btn_validation_path.place(x=150, y=250, width=100, height=70)


def get_path(entry_path_file, source_dir, app):
    """Lorsque nous appuyons sur valider dans la fenêtre d'enregistrement, cette méthode vérifie si le lien
    spécifié existe et s'il s'agit bien d'un dossier.
    S'il existe déjà un document portant le même nom, il est remplacé."""
    list_scrappings = os.listdir(source_dir)
    last_scrapp = list_scrappings[-1]

    if os.path.exists(entry_path_file.get()):
        if os.path.isdir(entry_path_file.get()):
            src_path = source_dir + "/" + last_scrapp
            dst_path = entry_path_file.get()
            try:
                shutil.copy(src_path, dst_path)
                subprocess.Popen(['explorer', dst_path])
            except shutil.SameFileError:
                os.remove(dst_path + "/" + os.path.basename(src_path))
                shutil.copy(src_path, dst_path)
                subprocess.Popen(['explorer', dst_path])
        else:
            show_error_window(entry_path_file)
    else:
        show_error_window(entry_path_file)

    for widget in app.winfo_children():
        widget.destroy()
    start_window(app)


def file_choice(app):
    """Cette fenêtre permet de désigner les deux fichiers à comparer."""
    for widget in app.winfo_children():
        widget.destroy()
    lb = tkinter.Label(app, text="Indiquez le chemin des deux fichiers \n scrappés à comparer", font=50, bg="#5B6770",
                       fg='white')
    lb.place(x=20, y=30, width=350, height=70)
    entry_fichier1 = tkinter.Entry(app, width=200)
    entry_fichier1.place(x=50, y=130, width=300, height=30)
    entry_fichier2 = tkinter.Entry(app, width=200)
    entry_fichier2.place(x=50, y=200, width=300, height=30)
    bouton_valider = tkinter.Button(app, text="valider", bg="green",
                                    command=lambda: check_path(entry_fichier1, entry_fichier2, app))
    bouton_valider.place(x=150, y=250, width=100, height=100)


def check_path(fichier1, fichier2, app):
    """Vérifier si le chemin des fichiers à comparer existe et s'il s'agit d'un fichier CSV."""
    if os.path.exists(fichier1.get()) and os.path.exists(fichier2.get()):
        if ".csv" in os.path.splitext(fichier1.get()) and ".csv" in os.path.splitext(fichier2.get()):
            loading_comparer(fichier1.get(), fichier2.get(), app)
        else:
            tkinter.messagebox.showwarning(title="Attention!",
                                           message="Veuillez renseigner des fichiers CSV!")
    else:
        tkinter.messagebox.showwarning(title="Attention!",
                                       message="Les chemins indiqués n'existent pas!")


def loading_comparer(fichier1, fichier2, app):
    """Lance simultanément la comparaison des fichiers et l'étiquette comparaison en cours."""
    compare_thread = threading.Thread(target=lambda: compare(fichier1, fichier2, app), daemon=True)
    compare_thread.start()
    for widget in app.winfo_children():
        widget.destroy()
    lb = tkinter.Label(app, text="Comparaison en cours...", font=100)
    lb.place(x=100, y=150, width=200, height=100)


def compare(file_1, file_2, app):
    """comparaison de deux fichiers"""
    df_1 = pd.read_csv(file_1, sep=";")
    df_2 = pd.read_csv(file_2, sep=";")
    merged = df_1.merge(df_2, on='Nom societe', how='outer', indicator=True)

    # Sélection des lignes ajoutées dans le DataFrame 2
    added = merged.loc[merged['_merge'] == 'right_only', :].assign(evenement='ajout')
    removed = merged.loc[merged['_merge'] == 'left_only', :].assign(evenement='retrait')

    concatenated = pd.concat([added, removed])

    if concatenated.empty:
        no_difference(app)
        for widget in app.winfo_children():
            widget.destroy()
        start_window(app)

    else:
        concatenated.to_csv(
            "Difference/Prospection_Client_added_VS_removed_scrapped_at_{}.csv".format(datetime.date(datetime.now())),
            index=False, encoding='utf-8-sig', sep=";")
        registration("Difference", app)


def no_difference(app):
    """for widget in app.winfo_children():
        widget.destroy()
    lb = tkinter.Label(app, text="Il n'y a pas de différences entres les 2 fichiers!", font=(100))
    lb.place(x=25, y=150, width=350, height=100)"""
    tkinter.messagebox.showwarning(title="Attention!", message="Il n'y a pas de différences entres les 2 fichiers!")
    for widget in app.winfo_children():
        widget.destroy()
    file_choice(app)


def is_connected():
    """test de connexion"""
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
    except OSError:
        tkinter.messagebox.showwarning(title="Attention!", message="Veuillez vous connecter à internet!")


def chrome_installed():
    # Chemin de la clé de registre pour l'emplacement de l'exécutable de Chrome
    chrome_key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"

    try:
        # Ouvrir la clé de registre correspondante
        chrome_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, chrome_key_path)

        # Obtenir la valeur par défaut de la clé (chemin de l'exécutable de Chrome)
        chrome_exe_path = winreg.QueryValue(chrome_key, None)

        if chrome_exe_path:
            print("Chrome est installé")
        else:
            tkinter.messagebox.showwarning(title="Attention!",
                                           message="Veuillez installer Google Chrome sur votre ordinateur!")

    except FileNotFoundError:
        tkinter.messagebox.showwarning(title="Attention!",
                                       message="Veuillez installer Google Chrome sur votre ordinateur!")


def main():
    """création de l'interface graphique"""
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'settings')
    app = tkinter.Tk()
    app.geometry("400x400")
    app.title("XR_Scrapping")
    app.configure(bg="#5B6770")
    app.iconphoto(False, tkinter.PhotoImage(file='Ressources/Signe_Favicon_XRoad.png'))
    start_window(app)
    chrome_installed()
    app.mainloop()


if __name__ == '__main__':
    main()
