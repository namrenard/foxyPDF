import os.path
import re
from PyPDF2 import PdfWriter, PdfReader
import datetime


class PDF:
    """
    Classe implémentant la librairie PyPDF2 pour combiner des pdf,extraire du texte ou des images de fichiers pdf
    """

    def __init__(self):
        self.files = []
        self.files_extract = []

    @staticmethod
    def get_file() -> str:
        """
        Méthode statique pour récupérer un nom de fichier pdf.
        :return: le nom du fichier sous forme de string
        """
        prompt = input("Veuillez entrer un nom de fichier (sans l'extension):")
        if not prompt.endswith(".pdf"):
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

    def combine_menu(self):
        """
        Méthode pour gérer la fusion de plusieurs fichiers PDF complet ou des pages de plusieurs
        fichiers différents.

        :return: la méthode pour fusionner la liste de fichiers PDF
        """
        print("Que voulez-vous combiner ?"
              "\n-1 des fichiers complets."
              "\n-2 des pages issus de fichiers différents.")
        scanner = input("Votre choix ? >>>")
        while int(scanner) != 1 and int(scanner) != 2:
            scanner = input("Votre choix ? >>>")

        # fichier complet
        if int(scanner) == 1:
            print("Combien de fichiers sont à fusionner ?")
            scanner2 = input(" ? >>> ")
            # on vérifie que c'est bien un nombre et qu'il y a 2 fichiers à minima sinon 2 fichiers par défaut.
            if not scanner2.isnumeric() or int(scanner) >= 2:
                scanner2 = "2"
            for i in range(int(scanner2)):
                file = PDF.get_file()
                if file != "":
                    self.files.append(os.path.realpath(file))
            # Verification que le nombre de fichiers minimal est bien de 2 pour une fusion.
            if len(self.files) < 2:
                print("Erreur, il n'y a qu'un fichier PDF valide.")
                return 0
            return self.combine_files()
        else:
            # fusion de pages de fichiers pdf différents.
            choix_fichier = False
            while not choix_fichier:
                f = PDF.get_file()
                file = os.path.realpath(f)
                pages_input = input("Indiquez numériquement les pages (séparées par des virgules): >>>")
                clean_pages = re.split(':|;|,|\*|\n| |\t', pages_input)
                new_element = {"file": file, "pages": clean_pages}
                self.files_extract.append(new_element)
                next_file = input("Ajouter un autre fichier pdf ? >>>  o/n")
                if next_file.lower() != "o":
                    choix_fichier = True
            return self.combine_pages()

    def combine_pages(self):
        """
        Methode de création d'un fichier pdf avec des pages de plusieurs fichiers pdf

        :return: code 1 ou 0 si la fusion a réussi ou pas.
        """
        if not self.files_extract:
            print("Aucune page à fusionner.")
            return 0
        datas = PdfWriter()
        for element in self.files_extract:
            file = element["file"]
            pages = list(map(int, element["pages"]))
            for i in range(len(pages)):
                pages[i] = pages[i] - 1
            try:
                file_open = open(file, "rb")
                file_read = PdfReader(file_open)
                for p in pages:
                    if int(p) < len(file_read.pages):
                        datas.add_page(file_read.pages[p])
            except Exception as e:
                print(f"Erreur dans la fusion des pages : {str(e)}")
                return 0
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
            self.files_extract.clear()
            return 1
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier combiné : {str(e)}")
            self.files_extract.clear()
            return 0

    def combine_files(self):
        """
        Méthode de création d'un fichier pdf combiné à partir d'une liste de fichiers pdf.

        :return: code 1 ou 0, si la fusion a réussi ou pas.
        """
        if not self.files:
            print("Aucun fichier PDF à fusionner.")
            return 0

        datas = PdfWriter()
        for file_path in self.files:
            try:
                file_open = open(file_path, "rb")
                file_read = PdfReader(file_open)
                for i in range(len(file_read.pages)):
                    datas.add_page(file_read.pages[i])
            except Exception as e:
                print(f"Erreur lors de la lecture du fichier {file_path}: {str(e)}")
                return 0

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
            print(f"Fusion réussie.\nLe fichier combiné est enregistré sous le nom : {filename}")
            print()
            file_out.close()
            self.files.clear()
            return 1
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier combiné : {str(e)}")
            self.files.clear()
            return 0

    @staticmethod
    def extract_text():
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

    @staticmethod
    def extract_image():
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
                            compteur += 1
                            file_output.close()
                        except Exception as e:
                            print(f"Erreur : l'extraction a rencontré un problème : {str(e)}.\n ")
                            return 0
            print("\nSuccès : l'extraction des images est terminées.\n")
            return 1

    @staticmethod
    def forced_extraction():
        """
        Méthode d'extraction "forcée" d'images en se basant sur le les données contenu dans le parametre x_object.
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
                # ref : https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in
                # -python/37055040#37055040
                x_object = page['/Resources']['/XObject'].get_object()
                try:
                    for obj in x_object:
                        if x_object[obj]['/Subtype'] == '/Image':
                            image = x_object[obj]
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
                    x_object = page['/Resources']['/XObject'].get_object()
                    try:
                        for obj in x_object:
                            if x_object[obj]['/Subtype'] == '/Image':
                                image = x_object[obj]
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
    print("-----------FoxyPDF v1.3-----------------")
    print("Veuillez choisir une action en indiquant un numéro entre 1 et 5.")
    print("--------------------")
    run = PDF()
    while True:
        print(
            " 1-Combiner des fichiers ou des pages PDF."
            "\n 2-Extraire du texte d'un fichier pdf."
            "\n 3-Extraire des images d'un fichier pdf."
            "\n 4-Extraction forcée des images (si l'extraction '3' n'a pas marchée)."
            "\n 5-Quitter.")
        print()
        choix = input("Votre choix ? >>> ")
        if choix == "1":
            run.combine_menu()
        elif choix == "2":
            run.extract_text()
        elif choix == "3":
            run.extract_image()
        elif choix == "4":
            run.forced_extraction()
        elif choix == "5":
            print("Au revoir.")
            exit()
        else:
            print("Erreur, vous n'avez pas choisis une action valide.\n Recommencez s'il vous plait.")
            print()
