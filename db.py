from pymongo import MongoClient
import uuid, pymongo

#Connect to the MongoDB remote database
client = MongoClient("mongodb+srv://admin:wNiMXwTesv42eYcQ@task.dykvv2y.mongodb.net/?tls=true")

db = client.cafe_db

#Input: None
#Output: randomly generated id
def generate_id():
    return uuid.uuid4().hex[:20]

#Input: the collection name, id, and dictionary to insert
#Output: None
def insert_document_mongo(collection_name, id, dict_to_insert):
    
    dict_to_insert['_id'] = id
    
    if db[collection_name].find_one({"_id": id}) is None:
        db[collection_name].insert_one(dict_to_insert)

#Input: dictionary containing cafe information
#Output: calculated total revenue
#Note: cafe information is inserted to the database
def insert_cafe(form: dict):
    total_revenue = int(form['number_of_customers']) * float(form['average_spend'])
    
    form.update({
        "total_revenue": total_revenue
    })
    
    insert_document_mongo("cafe", generate_id(), form)
    
    return total_revenue

#Input: None
#Output: last 5 cafe total revenue calculations with total revenue and cafe name
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
    
    pass
