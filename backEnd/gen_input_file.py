import crawler_multi_Thread as c

def gen_link_file():
    counter = 0
    bot = c.crawler(None, "urls.txt")
    bot.crawl(depth=1)
    outlinks = {}
    for k,v in bot.get_links():
        if k not in outlinks:
            outlinks[k] = []
            counter += 1
        if v not in outlinks:
            outlinks[v] = []
            counter += 1
        outlinks[k].append(str(v))
    with open("_url.txt", "w") as f:
        pg = str(1.0 / counter)
        for _id, links in outlinks.items():
            if not links:
                links = [str(_id)]
            line = "\t".join([str(_id)]+[pg]+list(set(links)))
            f.write(line+"\n")


if __name__ == "__main__":
    gen_link_file()
