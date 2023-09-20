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
    def getFile() -> str:
        prompt = input("Veuillez entrer un nom de fichier pdf valide en terminant par .pdf :")
        # gestion erreur de fichier non pdf.
        while not prompt.endswith(".pdf"):
            print("ERREUR, vous n'avez pas chargé un fichier PDF.")
            prompt = input("Veuillez entrer un nom de fichier pdf valide en terminant par .pdf :")

        try:
            if os.path.join(prompt):
                return prompt
        except FileNotFoundError:
            print("Erreur, le fichier pdf n'existe pas.")
        except IsADirectoryError:
            print(" Erreur, c'est un dossier et non un fichier pdf.")
        return ""

    def fusionFiles(self):
        print("Veuillez indiquer le nombre de fichiers PDF à combiner.")
        print("Note : les fichiers seront fusionnés à la suite.")
        scanner = input(" ? : ")
        # on vérifie que c'est bien un nombre
        while not scanner.isdigit() or int(scanner) < 2:
            print("Erreur, merci d'entrer un nombre supérieur ou égale à 2.")
            scanner = input(" ? : ")

        for i in range(int(scanner)):
            file = PDF.getFile()
            if file != "":
                self.files.append(file)
            if len(self.files) < 2:
                print("Erreur, il n'y a pas à minima 2 fichiers pdf valide.")
                exit(2)
        return self.openAndReadFile(file)

    def openAndReadFile(self):
        if not self.files:
            print("Aucun fichier PDF à fusionner.")
            return

        datas = PdfFileWriter()

        for file_path in self.files:
            try:
                with open(file_path, "rb") as file_open:
                    file_read = PdfFileReader(file_open)
                    for page_number in range(file_read.getNumPages()):
                        datas.addPage(file_read.getPage(page_number))

            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {file_path}: {str(e)}")

        return self.writeFile(datas)

    def writeFile(self, datas):
        date = datetime.date.today().strftime("%d-%m-%Y")
        prompt = input("Veuillez donner un nom de fichier pour le fichier combiné : ")
        if not prompt:
            filename = f"fichier_combine_{date}.pdf"
            print(f"Vous n'avez pas donné de nom, {filename} sera le nom du fichier combiné.")
        else:
            filename = f"{prompt}.pdf"
            print(f"{filename} sera le nom du fichier combiné.")

        try:
            with open(filename, "wb") as file_out:
                datas.write(file_out)
            print(f"Fusion réussie. Le fichier combiné est enregistré sous {filename}")
            return 1
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier combiné : {str(e)}")
            return 0

    def extractText(self):
        print("Not implemented yet")
        exit(3)

    def extractImage(self):
        print("Not implemented yet")
        exit(4)


# Main--------------------------------------------------------
if __name__ == "__main__":
    print("-----FoxyPDF v1-----")
    print("Veuillez choisir une action en indiquant un numéro 1,2 ou 3.")
    print()
    foxypdf = PDF()
    while True:
        print(" 1-Combiner des fichiers PDF.\n 2-Extraire du texte.\n 3-Extraire des images.")
        print()
        choix = input("Votre choix ? : ")
        if choix == "1":
            foxypdf.fusionFiles()
        elif choix == "2":
            foxypdf.extractText()
        elif choix == "3":
            foxypdf.extractImage()
        else:
            print("Erreur, vous n'avez pas choisis une action valide.\n Recommencez s'il vous plait.")
            print()
