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

Publicaciones=Todo.publications
Pu=[]
for Publicacion1 in Publicaciones:
    Pub=Publicacion1.bib
    Pu.append([Pub["title"],
    Pub["abstract"],
    Pub["author"],
    Pub["cites"],
    Pub["cites"],
    Pub["cites_id"],
    Pub["eprint"],
    Pub["journal"],
    Pub["number"],
    Pub["pages"],
    Pub["publisher"],
    Pub["url"],
    Pub["volume"],
    Pub["year"]])
    




