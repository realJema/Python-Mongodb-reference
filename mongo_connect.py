import pymongo

'''
Creating a database
'''
# ****Be ware that your database won't be created until you insert the first data into a collection*****
myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/") # connect to local mongodb(yours might be different)

mydb = myclient["pythonDb"] # creates database 
mycol = mydb["customers"] # crate collection in mydb

# Variables holding data   
mydict = {"name" : "John", "address": "highway"}
mylist = [
  { "name": "Amy", "address": "Apple st 652"},
  { "name": "Susan", "address": "One way 98"},
  { "name": "Vicky", "address": "Yellow Garden 2"},
  { "name": "Ben", "address": "Park Lane 38"},
  { "name": "William", "address": "Central st 954"},
  { "name": "Chuck", "address": "Main Road 989"},
  { "name": "Viola", "address": "Sideway 1633"}
]
mylist2 = [
  { "_id": 1, "name": "John", "address": "Highway 37"},
  { "_id": 9, "name": "Susan", "address": "One way 98"},
  { "_id": 10, "name": "Vicky", "address": "Yellow Garden 2"},
  { "_id": 11, "name": "Ben", "address": "Park Lane 38"},
  { "_id": 12, "name": "William", "address": "Central st 954"},
  { "_id": 13, "name": "Chuck", "address": "Main Road 989"},
  { "_id": 14, "name": "Viola", "address": "Sideway 1633"}
]

# inserting into collection
x = mycol.insert_one(mydict)
y = mycol.insert_many(mylist)
z = mycol.insert_many(mylist2)

# printing details   
print(myclient.list_database_names())
print(mydb.list_collection_names())
print(x.inserted_id)
print(y.inserted_ids)

dblist = myclient.list_database_names()
collist = mydb.list_collection_names()

# checks for debugging purposes 
if "pythonDb" in dblist:
    print("The database exists")

if "customers" in collist:
    print("The collection exist")

'''
Searching in a database
'''
print('*'*50 + '\nSearching database \n' +'*'*50)
print('\nFind One' +'_'*50)
a = mycol.find_one() # finds the first element in collection
print(a)

print('\nFind All' +'_'*50)
# find all elements 
for x in mycol.find():
    print(x)

print('\nFilter results' +'_'*50)
myquery = {"address": "Park Lane 38"}
mydoc = mycol.find(myquery)
for x in mydoc:
    print("Search Simple: -> ", x)

# advanced queries 
myquery2 = {"address" : { "$gt": "S"}}
mydoc2 = mycol.find(myquery2)
for x in mydoc2:
    print("Search advanced: -> ", x)

# regex search
myquery3 = {"address": { "$regex": "^S"}}
mydoc3 = mycol.find(myquery3)
for x in mydoc3:
    print("Search regex: -> ", x)

print('\nReturn only some fields' +'_'*50)
for x in mycol.find({}, {"_id": 0, "name": 1, "address": 1 }): # fields to return are in 1
    print(x)

'''
Sorting results
'''
mydoc = mycol.find().sort("name", -1) # find all and sort by name, -1 sorts items in descending order, exculde for alternative
for x in mydoc:
    print(x)

'''
Updating in a database
'''

myquery = {"address": "Valley 345"}
newvalues = { "$set": {"address": "Canyon 123"}}

mycol.update_one(myquery, newvalues)
for x in mycol.find():
    print(x)

# update many 
myquery = {"address": {"$regex": "^S"}}
newvalues = {"$set": {"name": "Minnie"}}
x = mycol.update_many(myquery, newvalues)
print(x.modified_count, "documents updated.")

'''
Limit results
'''
myresult = mycol.find().limit(5)
for x in myresult:
    print(x)

'''
Deleting in a database
'''
myquery = {"address": "Mountain 21"}
mycol.delete_one(myquery)

# filtered deletion
myquery = {"address": {"$regex": "^S"}}
x = mycol.delete_many(myquery)
print(x.deleted_count, " documents delted.")

# delete everything
x = mycol.delete_many({})
print(x.deleted_count, " docuements deleted.")

'''
Deleting collection
'''
mycol.drop()