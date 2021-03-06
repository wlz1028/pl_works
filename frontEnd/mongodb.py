from pymongo import MongoClient
import operator

def query(query, collection_name, db_name='csc326', host="localhost", port=27017, _continue_on_error=True):
    if not isinstance(query, dict):
        raise Exception("query must be a dict")

    if not query:
        return
    client = MongoClient(host, port)
    col = client[db_name][collection_name]
    try:
        return col.find_one(query)
    except:
        raise Exception("Mongodb insertion failed")
    client.close()


def get_word_id(first_word):
    try:
        return query({'word': first_word}, 'word_id_index')['_id']
    except:
        return None

def get_doc_ids(word_id):
    if not word_id:
        return []
    try:
        return query({'_id': word_id}, 'word_id_index')['doc_ids']
    except:
        return []

def get_sorted_docs(doc_ids):
    if not doc_ids:
        return []
    docs = []
    try:
        for doc_id in doc_ids:
            doc = query({'_id': doc_id},'doc_id_index')
            docs.append({'_id': doc['_id'],'url': doc['url'], 'pr':doc['pageRank'],
                'title': doc['title'], 'description': doc['description']
                })
        sorted_docs = sorted(docs, key=lambda x: x['pr'],reverse=True)
        return sorted_docs
    except:
        return []
