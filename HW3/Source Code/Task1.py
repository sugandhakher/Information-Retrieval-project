import urllib
import bs4
import string
import time


def load_URL(lst,filename):
    with open(filename,'r') as f:
        for link in f:
            arr=link.split("\n")
            lst.append(arr[0])
        return lst

def string_to_file(filename,str):
    with open(filename, 'wt') as f:
        f.write(str)

title_exclude=['-','_']
file1="C:\Users\sony\Desktop\IR\HWa\HW3\end result.txt"
filenumber=0
#myFile = open('C:\Users\sony\Desktop\IR\HWa\HW1 crawler\taskA_link', 'r')
url_list=[]
url_list= load_URL(url_list,file1)
#url = "https://en.wikipedia.org/wiki/Sustainable_energy"
for url in url_list:
    title= url.split("/") [-1]
    link = urllib.urlopen(url).read()
    string1 = link.decode("utf-8")
    soup = bs4.BeautifulSoup(string1, 'html.parser')
    body = soup.find("div", {"id": "bodyContent"})
    html_string= body.encode("utf-8")
    title=''.join(ch for ch in title if ch not in title_exclude) # remove punctuation from title
    title= title.lower()
    htmlfile=".\Corpus\\" + title + ".txt"
    html_string=title + "\n" + html_string
    filenumber += 1
    print "saving HTML file : " + htmlfile + " " + str(filenumber)
    string_to_file(htmlfile, html_string)

# kill all script and style elements
    for script in body(["script", "style", "a"]):
        script.extract()  # rip it out
# get text
    text = body.get_text()
# break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.encode("utf-8")
    text= title + "\n"+ text
    text=text.lower()

    file= ".\Parsed\\" + title + ".txt"

    punc_set = set(string.punctuation).difference(set("-"))
    punc_set.add('--')

    #removing punctuation but retaining inside digits
    str2=""
    if text[0] in punc_set:
        str2 = str2 + " "
    else:
        str2 = str2 + text[0]
    for ch in range (1,len(text)-1):
        if text[ch] in punc_set:
            if text[ch] in ['/','-',',','.'] and text[ch+1].isdigit() and text[ch-1].isdigit():
                str2 = str2 + text[ch]
            else:
                str2 = str2 + " "
        else:
            str2 = str2 + text[ch]
    if text[-1] in punc_set:
        str2 = str2 + " "
    else:
        str2 = str2 + text[-1]

    text=''.join([i if ord(i) < 128 else '' for i in str2])
    print "saving ParsedHTML file : " + file + " " + str(filenumber)
    string_to_file(file, text)
    print time.clock()
