import pymongo
import sys

client = pymongo.MongoClient()
bd=client["State_Art2"]
Dominios=bd["Busquedas"]
Res=list(Dominios.find({},{"keywords"}))

for i in Res: print(i["keywords"])
