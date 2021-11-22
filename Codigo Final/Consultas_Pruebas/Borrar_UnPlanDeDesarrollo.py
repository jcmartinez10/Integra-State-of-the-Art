import pymongo
import sys
from bson.objectid import ObjectId

id = sys.argv[1]

client = pymongo.MongoClient()
bd=client["State_Art2"]
Dominios=bd["PlanesDesarrollo"]
Pag=bd["PaginasPlanesDesarrollo"]


Res_Pag=Pag.find({"Id_PdD":ObjectId(id)}).count()
if Res_Pag>0:
     r=input("Hay páginas indexadas del Plan de Desarrollo, Deseas eliminarlas también(y/n)?")
     if r=="y":
          x=Res_Pag.delete_many({"Id_PdD":ObjectId(id)})
          Dominios.delete_one({'_id': ObjectId(id)})
          print(x.deleted_count, " páginpythonas borradas")
     else:
          print("No se ha borrado") 
else:
     Dominios.delete_one({'_id': ObjectId(id)})
