import os.path
import re
from PyPDF2 import PdfWriter, PdfReader
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
        """
        Méthode statique pour recupérer un nom de fichier pdf.
        :return: le nom du fichier sous forme de string
        """
        prompt = input("Veuillez entrer un nom de fichier (sans l'extension):")
        prompt = prompt + ".pdf"

        try:
            if os.path.join(prompt):
                return prompt
        except FileNotFoundError:
            print("Erreur, le fichier pdf n'existe pas.")
            exit(0)
        except IsADirectoryError:
            print(" Erreur, c'est un dossier et non un fichier pdf.")
            exit(0)
        return ""

    def fusion_files(self):
        """
        Méthode pour gérer le fusion de plusieurs fichiers PDF complet ensemble.

        :return: la méthode pour fusionner la liste de fichiers PDF
        """
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
            exit(0)
        return self.make_pdf()

    def make_pdf(self):
        """
        Méthode de création d'un fichier pdf combiné à partir d'une liste de fichiers pdf.

        :return: code 1 ou 0, si la fusion a réussi ou pas.
        """
        if not self.files:
            print("Aucun fichier PDF à fusionner.")
            return exit(0)

        datas = PdfWriter()
        for file_path in self.files:
            try:
                file_open = open(file_path, "rb")
                file_read = PdfReader(file_open)
                for i in range(len(file_read.pages)):
                    datas.add_page(file_read.pages[i])

            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {file_path}: {str(e)}")
                exit(-1)

        date = datetime.date.today().strftime("%d-%m-%Y")
        prompt = input("Veuillez donner un nom de fichier de sortie sinon faites 'ENTRER' :")
        if not prompt:
            filename = f"fichier_combine_{date}.pdf"
            print(f"Vous n'avez pas donné de nom, {filename} sera le nom du fichier combiné.")
        else:
            filename = f"{prompt}.pdf"
            print(f"{filename} sera le nom du fichier combiné.")

        try:
            file_out = open(filename, "wb")
            datas.write(file_out)
            print(f"Fusion réussie. Le fichier combiné est enregistré sous {filename}")
            print()
            file_out.close()
            self.files.clear()
            return 1
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier combiné : {str(e)}")
            self.files.clear()
            return 0

    def extract_text(self):
        """
        Méthode d'extraction de texte dans un fichier .txt depuis un fichier PDF.
        L'extraction peut se faire sur le fichier en entier ou des pages définies.

        :return: -1 ou 0 si l'extraction a pu se faire.
        """
        file = PDF.get_file()
        if file != "":
            try:
                pdf_open = open(file, "rb")
                pdf_read = PdfReader(pdf_open)
                print(
                    "\nConsignes pour l'extraction:"
                    "\n+ Donnez les numéros de chaque page du fichier à extraire,"
                    "\n+ Séparez les par une virgule,"
                    "\n+ Mettre '-1' pour extraire toutes les pages du fichier,"
                    "\n+ Faites 'ENTRER' pour valider.")
                print("++ Note : L'extraction est dépendante de la fabrication du PDF."
                      "\nExemple : Un scan d'un texte ou image avec texte ne marchera pas")
                pages_choice = input("numéro(s) de(s) page(s) ? >>>")

                # vérifie si l'utilisateur a bien mis un numéro
                while pages_choice == "" or "0" in pages_choice:
                    print("Erreur : Aucun numéro n'a été donné.")
                    pages_choice = input("numéro(s) de(s) page(s) ? >>>")

                # le code -1 c'est pour tout extraire le fichier.
                if pages_choice == "-1":
                    pages = []
                    for i in range(len(pdf_read.pages)):
                        pages.append(i)
                else:
                    clean_pages_choice = re.split(':|;|,|\*|\n| |\t', pages_choice)
                    pages = list(map(int, clean_pages_choice))
                    for i in range(len(pages)):
                        pages[i] = pages[i]-1
                # Gestion erreur trop de pages
                if len(pages) > len(pdf_read.pages):
                    print("\nErreur : Vous avez indiqué trop de pages.\nExtraction interrompue.\n")
                    return 0

                file_output = f"texte_extrait_de_{file.replace('.pdf', '')}.txt"
                txt_output = open(file_output, "a", encoding="utf-8")
                for p in pages:
                    try:
                        page = pdf_read.pages[p]
                        txt_extract = page.extract_text()
                        # Try different encodings if UTF-8 fails
                        try:
                            txt_output.write(f"\n-----PAGE {p}---------\n")
                            txt_output.write(txt_extract)

                        except UnicodeEncodeError:
                            print(f"Problème d'encodage 'utf-8' avec {p}. Changement d'encodage avec 'latin1'.")
                            txt_output.write(txt_extract.encode("latin1", "replace").decode("latin1"))
                    except Exception as e:
                        print(f"Erreur dans l'extraction du texte : {str(e)}")
                        return 0

                print("\n Succès : L'extraction de texte(s) est terminée.\n")
                return 1

            except FileNotFoundError:
                print("Erreur: aucun fichier pdf n'a été trouvé.")
                return 0
        else:
            print("Erreur: le fichier est vide.")
        return 0

    def extract_image(self):
        """
        Methode d'extraction des images en passant par le parametre 'image' du fichier.
        Cette méthode prend en compte un fichier dont les images ont été compressée

        :return: 1 ou 0 suivant que l'extraction est réussi
        """
        file = PDF.get_file()
        pdf_read = PdfReader(file)
        print("Veuillez indiquer une page pour en extraire les images ou '0' pour tout le fichier.")
        print("Note : Si cela ne marche pas ou une erreur, essayer l'extraction forcé. ")
        page_number = input("page ? >>>")
        while not page_number.isnumeric() or page_number == "":
            print("Erreur : Veuillez indiquer un nombre valide.")
            page_number = input("page ? >>>")
        else:
            compteur = 0
            if page_number != "0":
                page_number_int = int(page_number) - 1
                page = pdf_read.pages[page_number_int]
                for image in page.images:
                    try:
                        file_output = open(str(compteur) + "_" + image.name, "wb")
                        file_output.write(image.data)
                        compteur += 1
                        file_output.close()
                    except Exception as e:
                        print(f"Erreur : l'extraction a rencontré un problème : {str(e)}.\n ")
                        return 0
            else:
                pages_total = pdf_read.pages
                for i in range(len(pages_total)):
                    for image in pages_total[i].images:
                        try:
                            file_output = open(f"{str(compteur)}_page_{i}_{image.name}", "wb")
                            file_output.write(image.data)
                            compteur +=1
                            file_output.close()
                        except Exception as e:
                            print(f"Erreur : l'extraction a rencontré un problème : {str(e)}.\n ")
                            return 0
            print("\nSuccès : l'extraction des images est terminées.\n")
            return 1

    def extract_image2(self):
        """
        Méthode d'extraction "forcé" d'images en se basant sur le les données contenu dans le parametre xObject.
        Elle fonctionne si l'attribut "Filtre" est rensignée dans les metadonnées du Xobject et applique l'extension
        JPEG ou PNG en fonction du filtre.
        Elle peut renvoyer des objets "corrompu" si pas de filtre en appliquant JPG par défault.

        :return: 1 ou 0 si l'extraction a pu être faite.
        """
        file = PDF.get_file()
        pdf_read = PdfReader(file)
        print("Veuillez indiquer une page pour en extraire les images ou '0' pour tout le fichier.")
        print("Note : Si l'image n'a pas été compressé, l'extraction échouera.")
        page_number = input("page ? >>>")
        while not page_number.isnumeric() or page_number == "":
            print("Erreur : Veuillez indiquer un nombre valide.")
            page_number = input("page ? >>>")
        else:
            if page_number != "0":
                page_number_int = int(page_number) - 1
                page = pdf_read.pages[page_number_int]
                #ref : https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python/37055040#37055040
                xObject = page['/Resources']['/XObject'].get_object()
                try:
                    for obj in xObject:
                        if xObject[obj]['/Subtype'] == '/Image':
                            image = xObject[obj]
                            image_data = image.get_data()
                            if '/Filter' in image:
                                filters = image['/Filter']
                                if '/DCTDecode' in filters:
                                    file_extension = 'jpg'
                                elif '/FlateDecode' in filters:
                                    file_extension = 'png'
                                else:
                                    file_extension = 'inconnu'
                            else:
                                # Par défaut, supposez que c'est du JPEG si le filtre n'est pas spécifié
                                file_extension = 'jpg'
                            file_output = open(f"image_{page_number_int}_{obj[1:]}.{file_extension}", "wb")
                            file_output.write(image_data)
                            file_output.close()
                except Exception as e:
                    print(f"Erreur : l'extraction a rencontré un problème : {str(e)}.\n ")
                    return 0
            else:
                pages_total = pdf_read.pages
                for i in range(len(pages_total)):
                    page = pdf_read.pages[i]
                    xObject = page['/Resources']['/XObject'].get_object()
                    try:
                        for obj in xObject:
                            if xObject[obj]['/Subtype'] == '/Image':
                                image = xObject[obj]
                                image_data = image.get_data()
                                if '/Filter' in image:
                                    filters = image['/Filter']
                                    if '/DCTDecode' in filters:
                                        file_extension = 'jpg'
                                    elif '/FlateDecode' in filters:
                                        file_extension = 'png'
                                    else:
                                        file_extension = 'inconnu'
                                else:
                                    # Par défaut
                                    file_extension = 'jpg'
                                file_output = open(f"page_{i}_{obj[1:]}.{file_extension}", "wb")
                                file_output.write(image_data)
                                file_output.close()
                    except Exception as e:
                        print(f"Erreur : l'extraction a rencontré un problème : {str(e)}.\n ")
                        return 0
            print("\nSuccès : l'extraction des images est terminées.\n")
            return 1


# Main--------------------------------------------------------
if __name__ == "__main__":
    print("-----------FoxyPDF v1-----------------")
    print("Veuillez choisir une action en indiquant un numéro entre 1 et 5.")
    print("--------------------")
    foxypdf = PDF()
    while True:
        print(
            " 1-Combiner des fichiers PDF."
            "\n 2-Extraire du texte vers un fichier texte."
            "\n 3-Extraire des images."
            "\n 4-Extraction forcée des images (si l'extraction '3' n'a pas marchée)."
            "\n 5-Quitter.")
        print()
        choix = input("Votre choix ? >>> ")
        if choix == "1":
            foxypdf.fusion_files()
        elif choix == "2":
            foxypdf.extract_text()
        elif choix == "3":
            foxypdf.extract_image()
        elif choix == "4":
            foxypdf.extract_image2()
        elif choix == "5":
            print("Au revoir.")
            exit()
        else:
            print("Erreur, vous n'avez pas choisis une action valide.\n Recommencez s'il vous plait.")
            print()
