from crawler import crawler
from pagerank import page_rank
from write_mongo import write_records
from mongodb import drop_db

def doc_id_index(links, inverted_doc_id, desc):
    """
    Build doc_id_index
    """
    pr_results = page_rank(links)
    mongo_doc = [{"_id": doc_id,
                "pageRank": link_id,
                "url": inverted_doc_id[doc_id],
                "title": desc[doc_id]['title'],
                "description": desc[doc_id]['description']} for doc_id,link_id in pr_results.items()]
    write_records(mongo_doc, "csc326", "doc_id_index")

def word_id_index(lexcon, inverted_index):
    """
    Build word_id_index
    """
    mongo_doc = [{"_id": word_id, "doc_ids": list(inverted_index[word_id]), "word": word} for word, word_id in lexcon.items() ]
    write_records(mongo_doc, "csc326", "word_id_index")

def main(urls_file, _depth):
    drop_db()
    bot = crawler(None, urls_file)
    bot.crawl(depth=_depth)

    doc_id_index(bot.get_links(), bot.get_inverted_doc_id_cache(), bot.get_url_description())

    word_id_index(bot.get_word_id(), bot.get_inverted_index())

if __name__ == "__main__":
    main("urls.txt", 1)
