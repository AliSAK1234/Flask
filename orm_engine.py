from mongoengine import *
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["file-demo"]

dblist = myclient.list_database_names()
if "file-demo" not in dblist:
  print("The database is not exists.")

class models():
    id = IntField(primary_key=True,autoincrement=True)
    create_date = DateTimeField()
    write_date = DateTimeField()

    # To Create
    def create(self,list_values):
        db = self.__tablename__
        collist = mydb.list_collection_names()
        if db not in collist:
            print("The collection is not exists and it will be created.")
        mycol = mydb[db]
        inserting = mycol.insert_one(list_values)
        return inserting

    # To Update
    def write(self,self_id,list_values):
        db = self.__tablename__
        collist = mydb.list_collection_names()
        if db not in collist:
            print("The collection is not exists and it will be created.")
        mycol = mydb[db]
        update = mycol.update_one({'_id': self_id},{"$set":list_values}, upsert=False)
        return update

    # To Delete
    def unlink(self):
        return True

    def search(self,search_dict_query,limit=None):
        db = self.__tablename__
        collist = mydb.list_collection_names()
        if db not in collist:
            print("The collection is not exists and it will be created.")
        mycol = mydb[db]
        data = {}
        if mycol:
            if limit is not None:
                if limit == 1:
                    fetch_db = mycol.find_one(search_dict_query)
                else:
                    fetch_db = mycol.find(search_dict_query).limit(limit)
            else:
                fetch_db = mycol.find(search_dict_query)
            if fetch_db:
                return fetch_db
            else:
                return False

        raise ValueError("Wrong DB Name")




