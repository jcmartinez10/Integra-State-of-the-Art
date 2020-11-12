# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 17:05:15 2020

@author: Toshiba
"""
from scholarly import scholarly

Autor=next(scholarly.search_author('David Álvarez Martínez'))

Autor.affiliation
Autor.fill()

Todo=Autor.fill()

Todo_dic=vars(Todo)



Publicaciones=Todo.publications
Prueba=Publicaciones[0]
d=Prueba.fill().bib
print(d)
Pu=[]


for p in Publicaciones:
    Pu.append(p.fill().bib)

Pu[1].keys()


#### Inviable crear tablas porque en cada pulicación no exiten todos los campos. 
'''for Publicacion1 in Publicaciones:
    Pub=Publicacion1.fill().bib
    print(Pub["title"])
    LI=[Pub["title"],
    Pub["abstract"],
    Pub["author"],
    Pub["cites"],
    Pub["cites_id"],
    Pub["eprint"],
    Pub["journal"],
    Pub["number"],
    Pub["pages"],
    Pub["publisher"],
    Pub["url"],
    #Pub["volume"],
    Pub["year"]]
    Pu.append(LI)'''

####Se propone gestionas una  base de datos NoSQL ####   
##Almacenamiento inicial en mongo BD#

import pymongo

#Se debe tener previamente corriendo en servidor de MongoDB
client = pymongo.MongoClient()
#Como prueba se imprimen la lista de BD que se están gestionando desde Mongo-server
for bd in client.list_databases(): print(bd)

#Conexion a una DB llamada "Journals1" como prueba inicial para agregar una primera colección
bd=client["Journals1"]
mycol = bd["Autores"]

for p in Pu:
    mycol.insert_one(p)




