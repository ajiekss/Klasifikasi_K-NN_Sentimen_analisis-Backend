from pymongo import MongoClient

class DBModel:
    
    client = MongoClient()

    def get_data_all(self, database, collection):
        db = self.client[database]
        cursor = db[collection].find({}, {'_id': False})
        return cursor