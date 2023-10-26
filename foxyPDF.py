import re
import click
from PyPDF2 import PdfWriter, PdfReader
import datetime


@click.command(name="cp", help="Combinaison de différentes pages de fichiers PDF différents.")
# https://stackoverflow.com/questions/47631914/how-to-pass-several-list-of-arguments-to-click-option
@click.argument('filename_and_pages', nargs=-1, type=str, required=True, metavar="filename:pages")
@click.argument('file_out', type=click.Path(), default=None)
def combine_pages(filename_and_pages: list, file_out: str) -> int:
    """
    Methode de création d'un fichier pdf avec des pages de plusieurs fichiers pdf.
    La commande prend en argument un liste de str sous forme "nom_fichier:liste_de_page"
    La liste de page doit être séparé par une virgule ou un point-virgule ou une étoile.

    :return: code 1 ou 0 si la fusion a réussi ou pas.
    """
    files_extract = []
    # on brasse la liste de str et on la découpe via le ":" puis on récupère les sub-str en
    # prenant garde au séparateur.On ajoute ensuite au dictionnaire.
    for obj in filename_and_pages:
        filename, pages = obj.split(":")
        filename = click.Path(exists=True)(None, None, filename)
        p = []
        for page in re.split('[;,*]', pages):
            p.append(int(page))
        new_element = {"file": filename, "pages": p}
        files_extract.append(new_element)

    if not files_extract:
        click.echo("Aucune page à fusionner.")
        return 0

    datas = PdfWriter()
    for element in files_extract:
        file = element["file"]
        pages = element["pages"]
        for i in range(len(pages)):
            pages[i] = pages[i] - 1
        try:
            file_open = open(file, "rb")
            file_read = PdfReader(file_open)
            for p in pages:
                if int(p) < len(file_read.pages):
                    datas.add_page(file_read.pages[p])
        except Exception as e:
            click.echo(f"Erreur dans la fusion des pages : {str(e)}")
            return 0
    if not file_out:
        date = datetime.date.today().strftime("%d-%m-%Y")
        file_out = f"fichier_combine_{date}.pdf"
        click.echo(f"Vous n'avez pas donné de nom, {file_out} sera le nom du fichier combiné.")

    try:
        output = open(file_out, "wb")
        datas.write(output)
        click.echo(f"Fusion réussie. Le fichier combiné est enregistré sous {file_out}.\n")
        output.close()
        return 1
    except Exception as e:
        click.echo(f"Erreur lors de l'écriture du fichier combiné : {str(e)}")
        return 0


@click.command(name="cf", help="Combinaison de fichiers PDF complet entre eux.")
@click.argument('filename', nargs=-1, type=click.Path(exists=True))
@click.argument('file_out', type=click.Path(), default=None)
def combine_files(filename: list, file_out: str) -> int:
    """
    Méthode de création d'un fichier pdf combiné à partir d'une liste de fichiers pdf.

    :return: code 1 ou 0, si la fusion a réussi ou pas.
    """
    files = []
    if len(filename) < 2:
        raise click.UsageError("Erreur : Il faut indiquer au moins deux fichiers.")

    for file in filename:
        if ".pdf" in file:
            files.append(file)
        else:
            raise click.BadParameter(f"Le fichier {file} doit être un fichier PDF.")
    if not files:
        click.echo("Erreur : Aucun fichier PDF à fusionner.")
        return 0
    datas = PdfWriter()
    for file_path in files:
        try:
            file_open = open(file_path, "rb")
            file_read = PdfReader(file_open)
            for i in range(len(file_read.pages)):
                datas.add_page(file_read.pages[i])
        except Exception as e:
            click.echo(f"Erreur lors de la lecture du fichier {file_path}: {str(e)}")
            return 0
    if file_out is None:
        date = datetime.date.today().strftime("%d-%m-%Y")
        file_out = f"fichier_combine_{date}.pdf"
        click.echo(f"Vous n'avez pas donné de nom de sortie, {file_out} sera le nom du fichier combiné.")
    elif not file_out.endswith(".pdf"):
        file_out = f"{file_out}.pdf"
    try:
        fileout = open(file_out, "wb")
        datas.write(fileout)
        click.echo(f"Succès ! Fusion réussie.")
        fileout.close()
        files.clear()
        return 1
    except Exception as e:
        click.echo(f"Erreur lors de l'écriture du fichier combiné : {str(e)}")
        files.clear()
        return 0


@click.command(name="et", help="Extraction de texte d'un fichier complet ou d'une sélection de pages.")
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.argument('file_out', type=click.Path(), default=None)
@click.option('--page', '-p', type=str,
              help='Les pages où extraire du texte, séparé par des virgules, par défaut tout le fichier PDF est extrait')
def extract_text(filename: str, page: str, file_out: str) -> int:
    """
    Méthode d'extraction de texte dans un fichier .txt depuis un fichier PDF.
    L'extraction peut se faire sur le fichier en entier ou des pages définies.
    Les pages ou le texte est a extraire doivent etre séparés par ":" ou ";" ou "," ou "*".

    :return: -1 ou 0 si l'extraction a pu se faire.
    """
    try:
        pdf_open = open(filename, "rb")
        pdf_read = PdfReader(pdf_open)
        # le code 0 c'est pour tout extraire le fichier.
        if not page:
            pages = []
            for i in range(len(pdf_read.pages)):
                pages.append(i)
        else:
            clean_pages = re.split('[:;,*]', page)
            pages = list(map(int, clean_pages))
            for i in range(len(pages)):
                pages[i] = pages[i] - 1
            # Gestion erreur trop de pages
            if len(pages) > len(pdf_read.pages):
                raise click.BadParameter("Erreur : Vous avez indiqué trop de pages.\nExtraction interrompue.\n")

        if file_out is None:
            file_output = f"texte_extrait_de_{filename.replace('.pdf', '')}.txt"
            txt_output = open(file_output, "a", encoding="utf-8")
        elif not file_out.endswith(".txt"):
            file_output = f"{file_out}" + ".txt"
            txt_output = open(file_output, "a", encoding="utf-8")
        else:
            txt_output = open(file_out, "a", encoding="utf-8")
        for p in pages:
            try:
                page = pdf_read.pages[p]
                txt_extract = page.extract_text()
                # Autre encodages si UTF-8 ne marche pas
                try:
                    txt_output.write(f"\n-----PAGE {p}---------\n")
                    txt_output.write(txt_extract)
                except UnicodeEncodeError:
                    click.echo(f"Problème d'encodage 'utf-8' avec {p}. Changement d'encodage avec 'latin1'.")
                    txt_output.write(txt_extract.encode("latin1", "replace").decode("latin1"))
            except Exception as e:
                click.echo(f"Erreur dans l'extraction du texte : {str(e)}")
                return 0

            click.echo("\n Succès : L'extraction de texte(s) est terminée.\n")
            return 1

    except FileNotFoundError:
        click.echo("Erreur: aucun fichier pdf n'a été trouvé.")
        return 0


@click.command(name="ei", help="Extraction d'image(s) d'un fichier PDF. Cela peut échouer.")
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.option('--page', '-p', type=str,
              help='La page où extraire les images, par défaut tout le fichier PDF est extrait')
def extract_image(filename: str, page: str) -> int:
    """
    Methode d'extraction des images en passant par le parametre 'image' du fichier.
    Cette méthode prend en compte un fichier dont les images ont été compressées.

    :return: 1 ou 0 suivant que l'extraction est réussi
    """
    pdf_read = PdfReader(filename)
    compteur = 0
    if not page:
        pages_total = pdf_read.pages
        for i in range(len(pages_total)):
            for image in pages_total[i].images:
                try:
                    file_output = open(f"{str(compteur)}_page_{i}_{image.name}", "wb")
                    file_output.write(image.data)
                    compteur += 1
                    file_output.close()
                except Exception as e:
                    click.echo(f"Erreur : l'extraction a rencontré un problème : {str(e)}.\n ")
                    return 0
    else:
        page_int = int(page) - 1
        page = pdf_read.pages[page_int]
        for image in page.images:
            try:
                file_output = open(str(compteur) + "_" + image.name, "wb")
                file_output.write(image.data)
                compteur += 1
                file_output.close()
            except Exception as e:
                click.echo(f"Erreur : l'extraction a rencontré un problème : {str(e)}.\n ")
                return 0

        click.echo("\nSuccès : l'extraction des images a bien été effectuée.\n")
        return 1


@click.command(name="eiF", help="Extraction forcée d'images basées sur les métadonnées du fichier. "
                                "Cela peut échouer ou donner des images corrompues.")
@click.argument('filename', nargs=1, type=click.Path(exists=True))
@click.option('--page', '-p', type=str,
              help='La page où extraire les images, par défaut tout le fichier PDF est extrait')
def forced_extraction(filename: str, page: str) -> int:
    """
    Méthode d'extraction "forcée" d'images en se basant sur les données contenu dans le parametre x_object.
    Elle fonctionne si l'attribut "Filtre" est renseigné dans les metadonnées du Xobject et applique l'extension
    JPEG ou PNG en fonction du filtre.
    Elle peut renvoyer des objets "corrompus" si pas de filtre en appliquant JPG par défault.

    :return: 1 ou 0 si l'extraction à pu être faite.
    """

    pdf_read = PdfReader(filename)
    if not page:
        pages = pdf_read.pages
        for i in range(len(pages)):
            p = pdf_read.pages[i]
            x_object = p['/Resources']['/XObject'].get_object()
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
                    else:
                        click.echo(f"Erreur : Aucune métadonnée d'images n'est présente.")
                        return 0
            except Exception as e:
                click.echo(f"Erreur : l'extraction a rencontré un problème : {str(e)}.\n ")
                return 0

    else:
        page_int = int(page) - 1
        page = pdf_read.pages[page_int]
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
                        # Par défaut, on suppose que c'est du JPEG si pas de filtre
                        file_extension = 'jpg'
                    file_output = open(f"image_{page_int}_{obj[1:]}.{file_extension}", "wb")
                    file_output.write(image_data)
                    file_output.close()
                else:
                    click.echo(f"Erreur : Aucune métadonnée d'image n'est présente.")
                    return 0
        except Exception as e:
            click.echo(f"Erreur : l'extraction a rencontré un problème : {str(e)}.\n ")
            return 0
    click.echo(f"Succès !\n Extraction terminée.")
    return 1


@click.group()
def cli():
    """
    Définition du groupe de commande

    """
    pass


if __name__ == "__main__":
    click.echo("-----------FoxyPDF v2.0-----------------")
    cli.add_command(combine_pages)
    cli.add_command(combine_files)
    cli.add_command(extract_text)
    cli.add_command(extract_image)
    cli.add_command(forced_extraction)

    cli()
