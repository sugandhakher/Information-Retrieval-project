import urlparse
import urllib
import BeautifulSoup
import time


Soup = BeautifulSoup.BeautifulSoup
lst=[]
#url="https://en.wikipedia.org/wiki/Sustainable_energy"

count=0
count2=0
f=open("depth_file",'wt')

def crawl_depth(url,d, key)  :  
    while len(url)>0:
        htmltext= urllib.urlopen(url).read()
        soup= Soup(htmltext)
        #url.pop(0)
        global count
                                  
        for i in soup.findAll('a', href=True):
            if key not in i['href']  and '#' in i['href'] or ':' in i['href'] or '/wiki/' not in i['href']:
                continue
            print i['href']
            if i['href'] not in lst:
                lst.append(i)
                
                lst.pop(0)
                f.write(i['href'])
                count=count+1
                if count>1000:
                    break
                if i['href'][0]=="/":
                        prefix=url
                else:
                        prefix=""
                
                crawl_depth(prefix + i['href'],d+1,'solar')
            if d>5:
                break
            f.close()

                       
            time.sleep(1)

crawl_depth("https://en.wikipedia.org/wiki/Sustainable_energy",0,'solar')
print (count)


	
		

