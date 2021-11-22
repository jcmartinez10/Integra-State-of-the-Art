import pymongo
import sys

client = pymongo.MongoClient()
bd=client["State_Art2"]
Col_Papers = bd["Papers"]

print(Col_Papers.index_information())
