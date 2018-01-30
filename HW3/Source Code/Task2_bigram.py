import string
import time
import operator
import collections


index={}
doc_map={}
bigram_list=[]
bigram_tf_table={}
bigram_df_table={}
bigram_term_sort=[]
bigram_doc_sort=[]

filename="end result.txt"
parsed_corpus=".\Parsed\\"


val=0
doc_count=0
doc_list=[]
x=0
title_exclude=['-','_']

def load_URL(lst,filename):
    with open(filename,'r') as f:
        for link in f:
            arr=link.split("\n")
            lst.append(arr[0])
        return lst

def indx_table_to_file(links,filename):
    with open(filename,'wt') as f:
        for key,value in links:
            f.write(str(key) + "," + str(value) + "\n")

def doc_table_to_file(links,filename):
    with open(filename,'wt') as f:
        for key,value in links:
            f.write(str(key) + ", " + (", ".join(str(e) for e in value) + "\n"))

url_list=[]
url_list= load_URL(url_list, filename)
for url in url_list:
    title=url.split("/")[-1]
    title=''.join(ch for ch in title if ch not in title_exclude)
    file=parsed_corpus +title + ".txt"
    temp_dict={}
    bigram_list=[]
    x+=1
    doc_id=x
    doc_map[title]=doc_id
    print " Now working on file : " + file + " " + str(doc_id)
    with open(file,'rt') as f:
        for line in f:
            line=line.split("\n")[0]
            chunks=filter(lambda a: a not in ["-", "--"], line.split())
            #for chunk in chunks:
            for i in range(0, len(chunks)-1):
                bigram_list.append(chunks[i]+' '+chunks[i+1])

    print "bigram list created"
    print time.clock()
    temp_dict = collections.Counter()

    for bigram in bigram_list:
        temp_dict[bigram] +=1
    print "temp_dict created"
    print time.clock()
    for key in temp_dict:
        if key in index:
            index[key].append((doc_id,temp_dict[key]))
        else:
            index[key]=[(doc_id,temp_dict[key])]


with open("bigram_inverted_list", 'wt') as file:
    for key, value in sorted(index.iteritems()):
        file.write(key + ' '+str(value)+ '\n')

doc_ref_list=sorted(doc_map.items(), key=operator.itemgetter(1),reverse=False)
indx_table_to_file(doc_ref_list,"bigram_doc_ref_file")

for i in index:
    value=index[i]
    for key,val1 in value:
        val += val1
        doc_count += 1
        doc_list.append(key)
    bigram_tf_table[i]=val
    doc_list.append(doc_count)
    bigram_df_table[i]=doc_list
    val=0
    doc_count=0
    doc_list=[]


bigram_term_sort= sorted(bigram_tf_table.items(), key=operator.itemgetter(1),reverse=True)
indx_table_to_file(bigram_term_sort, "bigram_tf_table.txt")

bigram_doc_sort= sorted(bigram_df_table.items(), key=operator.itemgetter(0),reverse=False)
doc_table_to_file(bigram_doc_sort, "bigram_df_table.txt")


print time.clock()
