from pymongo import MongoClient

def write_records(records, db_name, collection_name, host="localhost", port=27017, _continue_on_error=True):
    if not records:
        return
    client = MongoClient(host, port)
    col = client[db_name][collection_name]
    try:
        col.insert(records, continue_on_error = _continue_on_error)
    except:
        raise Exception("Mongodb insertion failed")
    client.close()
