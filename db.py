from pymongo import MongoClient
import uuid, pymongo

client = MongoClient("mongodb+srv://admin:wNiMXwTesv42eYcQ@task.dykvv2y.mongodb.net/?tls=true")

db = client.cafe_db

def generate_id():
    return uuid.uuid4().hex[:20]

def insert_document_mongo(collection_name, id, dict_to_insert):
    
    dict_to_insert['_id'] = id
    
    if db[collection_name].find_one({"_id": id}) is None:
        db[collection_name].insert_one(dict_to_insert)

def insert_cafe(form: dict):
    total_revenue = int(form['number_of_customers']) * float(form['average_spend'])
    
    form.update({
        "total_revenue": total_revenue
    })
    
    insert_document_mongo("cafe", generate_id(), form)
    
    return total_revenue
    
def get_last_five_cafes():
    
    res = db['cafe'].find({}).sort("datetime", pymongo.DESCENDING).limit(5)
    
    last_five = []
    
    for cafe in res:
        last_five.append({
            "cafe_name": cafe['cafe_name'],
            "total_revenue": cafe['total_revenue']
        })
        
    return last_five

if __name__ == "__main__":
    
    # print(get_last_five_cafes())
    pass
