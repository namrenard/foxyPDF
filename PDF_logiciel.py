import os.path

from PyPDF2 import PdfFileWriter, PdfFileReader
import datetime

"""
Version 1 : combiner 2 fichiers par selections.
------------------
1/ le path pour les deux fichiers d'entrées -> récupérer les noms des deux fichiers
1.2/ le path pour le fichier de sortie -> donner un nom
1.3/ la récupération des fichiers et la génération du fichier combiner
1.4/ on couple tous les fichiers sans chercher les pages.
2/ Extraire image : https://pypdf2.readthedocs.io/en/3.0.0/user/extract-images.html
3/ Extraire texte : https://pypdf2.readthedocs.io/en/3.0.0/user/extract-text.html

"""


class PDF:

    def __init__(self):
        self.files = []

    # Fonctions pour lire les paths de chaque fichier
    @staticmethod
    def get_file() -> str:
        prompt = input("Veuillez entrer un nom de fichier :")
        prompt = prompt + ".pdf"

        try:
            if os.path.join(prompt):
                ## debug
                print(f"DEBUG : {os.path.join(prompt)}")
                ########
                return prompt
        except FileNotFoundError:
            print("Erreur, le fichier pdf n'existe pas.")
        except IsADirectoryError:
            print(" Erreur, c'est un dossier et non un fichier pdf.")
        return ""

    def fusion_files(self):
        print("Veuillez indiquer le nombre de fichiers PDF à combiner.")
        scanner = input(" ? >>> ")
        # on vérifie que c'est bien un nombre et qu'il y a 2 fichiers à minima.
        while not scanner.isdigit() or int(scanner) < 2:
            print("Erreur, merci d'entrer un nombre supérieur ou égale à 2.")
            scanner = input(" ? >>> ")

        for i in range(int(scanner)):
            file = PDF.get_file()
            if file != "":
                self.files.append(os.path.realpath(file))
        if len(self.files) < 2:
            print("Erreur, il n'y a pas à minima 2 fichiers pdf valide.")
            exit(2)
        return self.make_pdf()

    def make_pdf(self):
        if not self.files:
            print("Aucun fichier PDF à fusionner.")
            return

        datas = PdfFileWriter()
        for file_path in self.files:
            try:
                file_open = open(file_path, "rb")
                file_read = PdfFileReader(file_open)
                for i in range(file_read.getNumPages()):
                    datas.addPage(file_read.getPage(i))

            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {file_path}: {str(e)}")
                exit(-1)

        date = datetime.date.today().strftime("%d-%m-%Y")
        prompt = input("Veuillez donner un nom de fichier pour le fichier combiné :")
        if not prompt:
            filename = f"fichier_combine_{date}.pdf"
            print(f"Vous n'avez pas donné de nom, {filename} sera le nom du fichier combiné.")
        else:
            filename = f"{prompt}.pdf"
            print(f"{filename} sera le nom du fichier combiné.")

        try:
            file_out = open(filename, "wb")
            datas.write(file_out)
            print()
            print(f"Fusion réussie. Le fichier combiné est enregistré sous {filename}")
            file_out.close()
            self.files.clear()
            return 1
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier combiné : {str(e)}")
            self.files.clear()
            return 0

    def extract_text(self):
        print("Not implemented yet")
        exit(3)

    def extract_image(self):
        print("Not implemented yet")
        exit(4)


# Main--------------------------------------------------------
if __name__ == "__main__":
    print("-----FoxyPDF v1-----")
    print("Veuillez choisir une action en indiquant un numéro entre 1 et 4.")
    print("--------------------")
    foxypdf = PDF()
    while True:
        print(" 1-Combiner des fichiers PDF.\n 2-Extraire du texte.\n 3-Extraire des images.\n 4-Quitter.")
        print()
        choix = input("Votre choix ? >>> ")
        if choix == "1":
            foxypdf.fusion_files()
        elif choix == "2":
            foxypdf.extract_text()
        elif choix == "3":
            foxypdf.extract_image()
        elif choix == "4":
            print("Au revoir.")
            exit()
        else:
            print("Erreur, vous n'avez pas choisis une action valide.\n Recommencez s'il vous plait.")
            print()
