The crawler craws on a given list of urls. An inverted index is a python dictionay which the key is word_id  and value is a set of url_id which the word appears. A resolved_inverted_index has the same information as inverted index. But instead of word_id and urls_lis, it stores actual word and url.

usage:
input:
Urls are stored in urls.txt which one url on each line

Function calls:
tester.py shows how to make crolwer calls, and get inverted_index and resolved_inverted_index
To crawl on more website, you should modify the urls.txt
The default crawl depth is 2, but you can alway control the depth by:
    e.g.
    crawler.crawl(depth=1)


