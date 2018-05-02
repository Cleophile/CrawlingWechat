import urllib.request
import ssl
from html.parser import HTMLParser
import re

def analyzeArticle():
    class ArticleParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.loveletters = []

        def handle_data(self, data):
            if "❤表白" in data:
                l = data.split(':')
                ks = ':'.join(l[1:])
                self.loveletters.append(ks)

    page_code = {b'charset=utf-8': 'utf-8',
                 b'charset=gbk': 'gbk',
                 b'charset=gb2312': 'gb2312',
                 b'charset=iso8859-1': 'iso8859-1',
                 b'charset=gb18030': 'gb18030',
                 }

    # Fuck SSL
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    articles_links = open('articles.txt', 'r', encoding='utf-8')

    with open("words.txt", 'w', encoding='utf-8') as f:
        for line in articles_links:
            try:
                infolist = line.split(',')
                title = infolist[1].rstrip()
                link = infolist[3].rstrip()
                req = urllib.request.Request(link)
                rowpage = urllib.request.urlopen(req).read()
                decodeFormat = 'utf-8'
                for info, fm in page_code.items():
                    if rowpage.find(info) != -1:
                        decodeFormat = fm
                        break
                htmlpage = rowpage.decode(decodeFormat)
                parser = ArticleParser()
                parser.feed(htmlpage)
                parser.close()
                f.write(','.join(parser.loveletters) + ',')

            except:
                pass





