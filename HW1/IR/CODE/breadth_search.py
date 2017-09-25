import urlparse
import urllib
import BeautifulSoup
import time

Soup = BeautifulSoup.BeautifulSoup
lst=[]

count=0
count2=0
frst_list=[]
sec_list=[]
f=open("breadth_file",'wt')

def crawl_breadth(url,key):
    htmltext= urllib.urlopen(url).read()
    soup= Soup(htmltext)
    #urls.pop(0)
    global count
    global count2
              
    for i in soup.findAll('a', href=True):
        if key not in i['href']  and '#' in i['href'] or ':' in i['href'] or '/wiki/' not in i['href']:
            continue
            
        if i['href'] not in frst_list:
            frst_list.append(i)
            print i['href']
            f.write(i['href']+'\n')
            count=count+1
                    
                    
        soup2=Soup(urllib.urlopen("https://en.wikipedia.org"+i['href']).read())
            #frst_list.pop(0)

        for j in soup2.findAll('a', href=True):
            if key not in i['href']  and '#' in i['href'] or ':' in i['href'] or '/wiki/' not in i['href']:
                continue
            if j['href'] not in frst_list and (count2+count)<1000:
                frst_list.append(j)
                print "------------->" + j['href']
                count2=count2+1
                f.write(j['href']+'\n')
                print count2
                   
            if (count2+count)>=1000:
                break
                    
                f.close()
                    
        if count>=5:
            break      
                    
        time.sleep(1)            

crawl_breadth("https://en.wikipedia.org/wiki/Sustainable_energy", 'solar')
print count

	
