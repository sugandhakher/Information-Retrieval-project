import string
import operator
import time
import collections


index={}
doc_map={}
doc_ref_list=[]
trigram_tf_table={}
trigram_df_table={}
trigram_term_sort=[]
trigram_doc_sort=[]

val=0
doc_count=0
doc_list=[]
x=0
title_exclude=['-','_']
trigram_list=[]
filename="end result.txt"
parsed_corpus=".\Parsed\\"


def load_URL(lst,filename):
    with open(filename,'r') as f:
        for link in f:
            arr=link.split("\n")
            lst.append(arr[0])
        return lst

def indx_table_to_file(links,filename):
    with open(filename,'wt') as f:
        #print "start file"
        for key,value in links:
            #print links
            #f.write(str(key) + ", " + (", ".join(str(e) for e in value) + "\n"))
            f.write(str(key) + "," + str(value) + "\n")

def doc_table_to_file(links,filename):
    with open(filename,'wt') as f:
        #print "start file"
        for key,value in links:
            #print links
            #f.write(str(key) + "," + str(value) + "\n")
            f.write(str(key) + ", " + (", ".join(str(e) for e in value) + "\n"))

url_list=[]
url_list= load_URL(url_list, filename)
for url in url_list:
    title=url.split("/")[-1]
    title=''.join(ch for ch in title if ch not in title_exclude)
    file=parsed_corpus +title + ".txt"
    x+=1
    doc_id=x
    doc_map[title]=doc_id
    temp_dict={}
    trigram_list=[]
    print "Now working on file : " + file + " " + str(doc_id)

    with open(file,'rt') as f:
        for line in f:
            line=line.split("\n")[0]
            chunks=filter(lambda a: a not in ["-", "--"], line.split())
            for i in range(0, len(chunks)-2):
                trigram_list.append(chunks[i]+' '+chunks[i+1]+' '+chunks[i+2])

    print "trigram list created"
    print time.clock()

    temp_dict=collections.Counter()
    for trigram in trigram_list:
        temp_dict[trigram]+=1
    print "temp_dict created"
    print time.clock()

    for key in temp_dict:
        if key in index:
            index[key].append((doc_id,temp_dict[key]))
        else:
            index[key]=[(doc_id,temp_dict[key])]

with open("trigram_inverted_list", 'wt') as file:
    for key, value in sorted(index.iteritems()):
        file.write(key + ' '+str(value)+ '\n')

doc_ref_list=sorted(doc_map.items(), key=operator.itemgetter(1),reverse=False)
indx_table_to_file(doc_ref_list,"trigram_doc_ref_table")

for i in index:
    value=index[i]
    for key, val1 in value:
        val += val1
        doc_count += 1
        doc_list.append(key)
    trigram_tf_table[i]=val
    doc_list.append(doc_count)
    trigram_df_table[i]=doc_list
    val=0
    doc_count=0
    doc_list=[]


trigram_term_sort= sorted(trigram_tf_table.items(), key=operator.itemgetter(1),reverse=True)
indx_table_to_file(trigram_term_sort, "trigram_tf_table.txt")


trigram_doc_sort= sorted(trigram_df_table.items(), key=operator.itemgetter(0),reverse=False)
doc_table_to_file(trigram_doc_sort, "trigram_df_table.txt")

print "trigram_table is saved"
print time.clock()
