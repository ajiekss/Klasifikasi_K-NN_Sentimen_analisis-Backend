from pymongo import MongoClient

class DBModel:
    
    client = MongoClient()

    def get_data_all(self, database, collection):
        db = self.client[database]
        cursor = db[collection].find({}, {'_id': False})
        return cursor
    
    def insert_data(self, database, collection, documents):
        db = self.client[database]
        db[collection].drop()
        results = db[collection].insert_one(documents)
        
        return results