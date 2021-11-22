


import pymongo
client = pymongo.MongoClient()
bd=client["State_Art2"]
Col_Papers = bd["Papers"]

g=list(Col_Papers.aggregate([{'$sample': {'size':1}}]))
print(g[0]["_id"])
print(g[0]["Titulo"])
print(g[0]["Resumen"])
print(g[0]["doi"])
