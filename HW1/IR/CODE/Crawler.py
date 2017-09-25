import urlparse
import urllib
import BeautifulSoup
import time

url="https://en.wikipedia.org/wiki/Sustainable_energy"
urls= [url]
Soup = BeautifulSoup.BeautifulSoup
frst_list=[]
sec_list=[]
count=0
count2=0
f=open("crawled file",'wt')

def crawl():
        while len(urls)>0:
                htmltext= urllib.urlopen(urls[0]).read()
                soup= Soup(htmltext)
                urls.pop(0)
                global count
                global count2
                          
                for i in soup.findAll('a', href=True):
                        if '#' in i['href'] or ':' in i['href'] or '/wiki/' not in i['href']:
                                continue
                        
                        if i['href'] not in frst_list:
                                frst_list.append(i)
                                print i['href']
                                f.write(i['href']+'\n')
                                count=count+1
                                
                                
                        soup2=Soup(urllib.urlopen("https://en.wikipedia.org"+i['href']).read())
                        #frst_list.pop(0)

                        for j in soup2.findAll('a', href=True):
                                if '#' in j['href'] or ':' in j['href'] or '/wiki/' not in j['href']:
                                        continue
                                if j['href'] not in sec_list and (count2+count)<1000:
                                        sec_list.append(j)
                                        print "------------->" + j['href']
                                        f.write(j['href']+'\n')
                                        count2=count2+1
                                   
                        if (count2+count)>=1000:
                                        break
                                
                f.close()
                                
                if (count2+count)>=1000:
                        break      
                                
                           

                        
                time.sleep(1)

crawl()
print (count+count2)

	
		

