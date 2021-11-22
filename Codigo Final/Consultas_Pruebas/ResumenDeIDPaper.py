import pymongo
import sys

client = pymongo.MongoClient()
bd=client["State_Art2"]
Col_Papers = bd["Papers"]

id = sys.argv[1]

Res=Col_Papers.find_one({'_id':id},{'Resumen' , 'abstract'})
print(Res)




