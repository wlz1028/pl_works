from crawler import crawler

def main():
    print "Case one depth=1"
    bot = crawler(None, "urls.txt")
    bot.crawl(depth=1)
    print bot.get_inverted_index()
    print bot.get_resovled_inverted_index()

    print "Case two depth=2"
    bot = crawler(None, "urls.txt")
    bot.crawl(depth=2)
    print bot.get_inverted_index()
    print bot.get_resovled_inverted_index()

if __name__ == "__main__":
    main()
