# NOMBRE (Montesdeoca, Emily):

# Carga de librerías necesarias
from Bio import Entrez
import re
import csv
import pandas as pd #para hacer los dataframe y mapas 
import itertools #ayudar a crear una lista interactiva 

def download_pubmed(keyword): 
    """con esta funcion se buscara en pubmed  los articulos asociados con la palabra que se colocara como keyword, siendo la referencia al tema del que se hara la busqueda de los articulos
    """
    Entrez.email = "gualapuro.moises@gmail.com"
    handle = Entrez.esearch (db = "pubmed",
                             term = keyword,
                             usehistory = "y")
    record = Entrez.read (handle)
    id_list = record ["IdList"]
    webenv = record["WebEnv"]
    query_key = record["QueryKey"]
    handle = Entrez.efetch(db="pubmed", 
                           rettype="medline", 
                           retmode="text", 
                           retstart=0, 
                           retmax = 1500, 
                           webenv = webenv, 
                           query_key = query_key)
    my_data = handle.read()
    my_data2 = re.sub(r'\n\s{6}', ' ', my_data)
    return (my_data2)


def science_plots(file):
    """Con esta funcion se va a leer la fuente que se ha empleado en el keyword para la busqueda en Pubmed, por medio del uso de expresiones regulares para delimitar cada posible varinte de lectura, con el de que tome el pais y el autor de cada registro. Ademas generar una dataframe relacionando las coordenadas y el pais con el uso de la data coordenadas.txt/ recalcando que luego se tendra que hacer un arreglo para que se grafique solo los 5 mas abundantes 
    """
    AD = []
    paises1 = []
    paises2 = []
    paises3 = []
    paises4 = []
    paises5 = []
    paises6 = []
    paises7 = []
    paises8 = []
    paises9 = []
    paises10 = []
    paises11 = []
    paises12 = []
    paisesT = []
    
    
    for line in my_data2.splitlines():
        if line.startswith("AD  -"):
            AD.append(line[:])
    for line in my_data2.splitlines():
        if line.startswith("AD  -"):
            AD = line[:]
            pais1 = re.findall(r'\,\s(\w{2,16})\.', AD)
            paises1.append(pais1)
            
            pais2 = re.findall(r'\,\s(\w{2,16}[^0-9\,]\s\w{2,16}[^0-9])\.', AD)
            paises2.append(pais2)
            
            pais3 = re.findall(r'\,\s(\w{3,16}[^0-9\,]\s\w{2,3}[^0-9\,]\s\w{3,16}[^0-9\,])\.', AD)
            paises3.append(pais3)

            pais4 = re.findall(r'\,\s(\w{2,16})\.\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}', AD)
            paises4.append(pais4)

            pais5 = re.findall(r'\,\s(\w{2,16}[^0-9\,]\s\w{2,16}[^0-9])\.\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}', AD)
            paises5.append(pais5)

            pais6 = re.findall(r'\,\s(\w{3,16}[^0-9\,]\s\w{2,3}[^0-9\,]\s\w{3,16}[^0-9\,])\.\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}', AD)
            paises6.append(pais6)
 
            pais7 = re.findall(r'\,\s(\w{2,16})\. Electronic address:\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}\.', AD)
            paises7.append(pais7)

            pais8 = re.findall(r'\,\s(\w{2,16}[^0-9\,]\s\w{2,16}[^0-9])\. Electronic address:\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}\.', AD)
            paises8.append(pais8)

            pais9 = re.findall(r'\,\s(\w{3,16}[^0-9\,]\s\w{2,3}[^0-9\,]\s\w{3,16}[^0-9\,])\. Electronic address:\s[a-z0-9_\.-]+@[\da-z\.-]+\.[a-z\.]{2,6}\.', AD)
            paises9.append(pais9)

            pais10 = re.findall(r'\,\s\w{3,9}[0-9\-]\,\s(\w{2,16})\.', AD)
            paises10.append(pais10)
            
            pais11 = re.findall(r'\,\s\w{3,9}[0-9\-]\,\s(\w{2,16}[^0-9\,]\s\w{2,16}[^0-9])\.', AD)
            paises11.append(pais11)
            
            pais12 = re.findall(r'\,\s\w{3,9}[0-9\-]\,\s(\w{3,16}[^0-9\,]\s\w{2,3}[^0-9\,]\s\w{3,16}[^0-9\,])\.', AD)
            paises12.append(pais12)

            paisesT=paises1+paises2+paises3+paises4+paises5+paises6+paises7+paises8+paises9+paises10+paises11+paises12

    paisesT= list(itertools.chain.from_iterable(paisesT))
    len(paisesT)

    unique_paisesT = list(set(paisesT))
    unique_paisesT.sort()
    len(unique_paisesT)

    import csv
    
    coordenadas = {}
    with open('coordenadas.txt') as f:
        csvr = csv.DictReader(f)
        for row in csvr:
            coordenadas[row['Name']] = [row['Latitude'], row['Longitude']]
    pais = []
    lon = []
    lat = []
    c = []
    for z in unique_paisesT:
        if z in coordenadas.keys():
            pais.append(z)
            lat.append(float(coordenadas[z][0]))
            lon.append(float(coordenadas[z][1]))
            c.append(paisesT.count(z))
            tablaPaises = pd.DataFrame()
    tablaPaises["Pais"] = pais 
    tablaPaises["Numero de autores"] = c
     
    return
    
    