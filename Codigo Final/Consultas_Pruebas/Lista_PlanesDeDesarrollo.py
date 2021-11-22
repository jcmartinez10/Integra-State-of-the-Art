import pymongo
import sys

client = pymongo.MongoClient()
bd=client["State_Art2"]
Dominios=bd["PlanesDesarrollo"]
Pag=bd["PaginasPlanesDesarrollo"]

Res=list(Dominios.find({}))
#print("Plan Des.","  ","Alcance","  ","Ent. Terr.","  ","Vigencia","  ","Documento") 
for i in Res:
     Res_Pag=Pag.find({"Id_PdD":i["_id"]}).count(True)
     print(i["_id"],"  ",i["PlanDeDesarrollo"], "  ", i["Alcance"], "  ", i["EntidadTerritorial"], "  ", i["Vigencia"], "  ", i["NombreDelDocumento"],"  ",Res_Pag)

r=input("Quieres editar algún Plan de Desarrollo(y/n)?")
if r=="y":
     r2=input("Ingresa el ID")
     


