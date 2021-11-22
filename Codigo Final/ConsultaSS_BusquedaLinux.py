# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 06:51:20 2021

@author: Toshiba
"""
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import simplejson
import os
import requests 
import pymongo




client = pymongo.MongoClient()
bd=client["State_Art2"]
Col_Busqueda=bd["Busquedas"]
Col_Papers = bd["Papers"]

#display = Display(visible=1)
#display.start()
#driver=webdriver.Firefox()



#Se inicia el scrap para consultar la web de semanticScholar (Se decide por el scrap)
#Dado que SemanticScholar no tiene API para hacer consultas por palabras clave. 
def CorrerScrap(PalabraDeB):
    ColBus={"keywords":PalabraDeB}
    display = Display(visible=0)
    display.start()
    driver=webdriver.Firefox()
    driver.get("https://www.semanticscholar.org/search?q="+PalabraDeB+"&sort=influence")
    #time.sleep(5)
    #Se debe añadir un tiempo de espera de las respuestas.. 
    rs=WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"result-page")))
    results=driver.find_element_by_class_name("result-page")
    results=results.find_elements_by_class_name("cl-paper-row")
    #Se crea esta lista para almacenar TODOS los resultados (artículos) de la consulta.
    ListasID=[]
    ListaRe=[]
    #Se itera sobre cada artículo resultante
    #Capturar el Id, el título del document y el resto de información
    for i in results:
        #Se crea un diccionario para que guarde la información de cada resultado capturado. 
        Dic={}
        tit=i.find_element_by_tag_name("a").get_attribute('href')
        Dic["url"]=tit
        ListasID.append(tit.split("/")[-1])
        if Col_Papers.find_one({'_id':tit.split("/")[-1]})==None:
            Resumen={}
            try:
                tldr=i.find_element_by_class_name("tldr-abstract-replacement")
                tldr=tldr.find_elements_by_tag_name('span')
                tldr=tldr[1].text
                Resumen["TLDR"]=tldr
            except:
                Resumen["TLDR"]=""
            Dic["Resumen"]=Resumen
            Fecha=i.find_element_by_class_name("cl-paper-pubdates").text
            Dic["Fecha"]=Fecha
            #Para las estadisticas (por las tiene)
            '''
            try:
                Stats=i.find_elements_by_class_name("cl-paper-stats__action-stat")
                Citaciones=Stats[0].text
                Dic["NoCitaciones"]=int(Citaciones.replace(",",""))
            except:
                Dic["NoCitaciones"]=0
            '''
            #Se consulta la API de Scholar Semantic para capturar el resto de información
            Dic=ConsultaAPI1SS(Dic,tit)
            ListaRe.append({'Titulo':Dic['Titulo'],'_id':Dic["_id"]})
            Col_Papers.insert_one(Dic)
            #Dic2={}
        else:
            b=Col_Papers.find_one({'_id':tit.split("/")[-1]},{'Resumen.TLDR':1})
            if b['Resumen']['TLDR']=="":
                try:
                    tldr=i.find_element_by_class_name("tldr-abstract-replacement")
                    tldr=tldr.find_elements_by_tag_name('span')
                    tldr=tldr[1].text
                    Col_Papers.update_one({'_id':tit.split("/")[-1]},{'$set': {'Resumen.TLDR':tldr}})
                except:
                    pass
            '''b=Col_Papers.find_one({'_id':tit.split("/")[-1]},{'Fecha':1})
            if b['Fecha']=="":
                try:
                    Fecha=i.find_element_by_class_name("cl-paper-pubdates").text
                    Col_Papers.update_one({'_id':tit.split("/")[-1]},{'$set': {'Fecha':Fecha}})
                except:
                    pass    '''
    ColBus["Ids"]=ListasID
    Col_Busqueda.insert_one(ColBus)
    display.stop()
    driver.quit()
    return (ListaRe)
    
def ConsultaAPI1SS(Dic,url):
    print("Paper: ",url)
    response = requests.get('https://api.semanticscholar.org/v1/paper/URL:'+url)
    D=response.json()
    Dic["abstract"]=D["abstract"]
    Dic["autores"]=D["authors"]
    Dic["citaciones"]=D["citations"]
    Dic["NoCitaciones"]=len(D["citations"])   
    Dic["VelocidadCitaciones"]=D["citationVelocity"]
    Dic["corpusId"]=D["corpusId"]
    Dic["doi"]=D["doi"]
    Dic["CamposdeEstudio"]=D["fieldsOfStudy"]
    Dic["CuentaCotacionesInflu"]=D["influentialCitationCount"]
    Dic["Acceso_abierto"]=D["isOpenAccess"]
    Dic["Publicacion_licencia"]=D["isPublisherLicensed"]
    Dic["_id"]=D["paperId"]
    Dic["referencias"]=D["references"]
    Dic["Titulo"]=D["title"]
    Dic["Topicos"]=D["topics"]
    Dic["url2"]=D["url"]
    Dic["Evento"]=D["venue"]
    Dic["Ano"]=D["year"]
    if not Dic["doi"] is None:
        response = requests.get('https://api.openaccessbutton.org/metadata?id='+Dic["doi"])
        D=response.json()
        if D:
                if "crossref_type" in D: Dic["crossref_type"]=D["crossref_type"]
                if "journal" in D: Dic["Revista"]=D["journal"]
                if "journal_short" in D: Dic["Revista_Nombrecorto"]=D["journal_short"]
                if "issue" in D: Dic["issue"]=D["issue"]
                if "volume" in D: Dic["Volumen"]=D["volume"]
                if "page" in D: Dic["Paginas"]=D["page"]
                if "keyword" in D: Dic["keyword"]=D["keyword"]
                if "issn" in D: Dic["issn"]=D["issn"]
                if 'publisher' in D: Dic["Publisher"]=D["publisher"]
                if 'published' in D: Dic["published"]=D["published"]
                if 'url' in D: Dic["doiURl"]=D["url"]
    return (Dic)

def ConsultaBD(ListaBuG):
    l=list(Col_Papers.find({'_id':{"$in":ListaBuG["Ids"]}}, {"Titulo"})) 
    l.sort(key=lambda thing: ListaBuG["Ids"].index(thing['_id']))
    return(l)


#Generalización 
# 1. Consulta en Base de datos si existe ya registros de la palabra de busqueda
#   Si existe----> trae la informacion de la Base de datos
#   Si No -------> Hace la consulta a SS y almacena la información. 

#Entrada
#PalabraDeB="Colombia"
def ConsultaG(PalabraDeB):
    ListaBuG=Col_Busqueda.find_one({'keywords':PalabraDeB},{'Ids':1})
    if ListaBuG:
        l=ConsultaBD(ListaBuG)
        return ({"Validacion": "Ya tenemos registros guardados con esa palabra clave", "Papers": l})
    else: 
        l=CorrerScrap(PalabraDeB)
        return ({"Validacion": "Se hizo consulta de Semantic Scholar", "Papers": l})
        

