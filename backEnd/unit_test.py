import crawler as cs
import crawler_multi_Thread as cmt
import time
import master
from mongodb import get_word_id, get_doc_ids, get_sorted_docs,get_sorted_urls,drop_db

"""
test.html file has 15 unique words and 5 redundent words, and 2 url links
test_url.txt has test.html path to be passed to crawler
"""

def test_single_thread_crawler():
    """
    crawl on test.html which fixed number of word_id and urls will be parsed
    """
    try:
        bot = cs.crawler(None, "test_url.txt")
        bot.crawl(depth=0)
        assert len(bot.get_links()) == 2
        assert len(bot.get_word_id()) == 15
        assert len(bot.get_inverted_index()) == 15
    except:
        return False
    return True

def test_multi_thread_crawler():
    """
    1) test multithread crawler on test.html
    2)
        a) single thread crawl http://www.eecg.toronto.edu
        b) multi thread crawl http://www.eecg.toronto.edu
        c) compare result
        NOTE: single thread and multi thread result may be different
        due to different timeout, so please try multiple runs
    """
    try:
        #1) test local testcase
        print "    test multi thread on test.html"
        bot = cmt.crawler(None, "test_url.txt")
        bot.crawl(depth=0)
        assert len(bot.get_links()) == 2
        assert len(bot.get_word_id()) == 15
        assert len(bot.get_inverted_index()) == 15

        # 2)compare again single thread result

        # a)single thread crawl http://www.eecg.toronto.edu
        print "    compare multi thread result with single thread"
        start_time = time.time()
        single = cs.crawler(None, "urls.txt")
        single.crawl(depth=1)
        single_time = time.time() - start_time

        # b)multi thread crawl http://www.eecg.toronto.edu
        start_time = time.time()
        multi = cmt.crawler(None, "urls.txt")
        multi.crawl(depth=1)
        multi_time = time.time() - start_time

        delta = single_time - multi_time
        print "/////IMPROVE//////////"
        print "//////%d secs/////////" % delta
        print "////////////////////"

        # c)compare result
#        print "####Compare num of links"
        print "links"
        print len(single.get_links())
        print len(multi.get_links())
        assert len(single.get_links()) == len(multi.get_links())
#        print "####Compare num of word id"

        print "word_id"
        print len(single.get_word_id())
        print len(multi.get_word_id())
        assert len(single.get_word_id()) == len(multi.get_word_id())
#        print "####Compare num of inverted index"
        print "inverted"
        print len(single.get_inverted_index())
        print len(multi.get_inverted_index())
        assert len(single.get_inverted_index()) == len(multi.get_inverted_index())
    except:
        return False
    return True

def test_persistent():
    try:
        drop_db()
        #Crawl local test.html, and save information to mongodb
        master.main("test_url.txt", 0)

        #Crawl local test.html and save info in memory
        bot = cs.crawler(None, "test_url.txt")
        bot.crawl(depth=0)

        #compare in mem data with persistent data
        _id = bot._word_id_cache['xsfd']
        assert get_word_id('xsfd') == bot._word_id_cache['xsfd'] 
        _doc_ids = bot._inverted_index[_id]
        assert get_doc_ids(_id) == list(bot._inverted_index[_id])
    except:
        return False
    return True

def main():
    count = 0

    print "- test single thread crawler"
    if test_single_thread_crawler():
        count += 1
        print "passed"
    else:
        print "Failed"

    print "- test multi thread crawler"
    if test_multi_thread_crawler():
        count += 1
        print "passed"
    else:
        print "****May be casued by timeout please try again"
        print "Failed"

    print "- test persistent database(local mongoDB required)"
    if test_persistent():
        count += 1
        print "passed"
    else:
        print "Failed"

    print "Passed %d/3 tests" %count

if __name__ == '__main__':
    main()




