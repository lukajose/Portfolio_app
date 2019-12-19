import urllib.request as req
import time as t
import re
import json
from bs4 import BeautifulSoup

#Generator get next url to iterate
def url_change_letter_tickers():
    i = 65
    while i != 91:
        url = 'http://eoddata.com/stocklist/NASDAQ/' + chr(i) + '.htm' 
        yield (url,chr(i))
        i += 1

if __name__ == "__main__":
    
    File = open('ticker_text.json','w')
    data = {}
    for url_char in url_change_letter_tickers():
        url,char = url_char
        html = req.urlopen(url)
        bsobj = BeautifulSoup(html,"lxml")
        seen = set()
        for link in bsobj.findAll("a"):
            if 'href' in link.attrs:
                if '/stockquote/NASDAQ/' in link.attrs['href']:
                    seen.add(link.attrs['href'].split('/stockquote/NASDAQ/')[1][:-4])
        print(seen)
        data[char] = list(seen)
        print('=======================================')
        t.sleep(3)
    json.dump(data,File,indent=4,sort_keys=True)
    File.close()


