import time
import operator

index={}
unigram_index={}
unigram_tf_table={}
unigram_df_table={}
filename="end result.txt"
parsed_corpus=".\Parsed\\"
doc_count=0
doc_list=[]
val=0
doc_map={}
unigram_doc_link=[]
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
url_list= load_URL(url_list,filename)
for url in url_list:
    title=url.split("/")[-1]
    title=''.join(ch for ch in title if ch not in title_exclude)
    file=parsed_corpus +title + ".txt"
    temp_dict={}
    x+=1
    doc_id=x
    doc_map[title]=doc_id
    print " Now working on file : " + file + " " + str(doc_id)

    with open(file,'rt') as f:
        for line in f:
            line=line.split("\n")
            chunks=line[0].split()
            for chunk in chunks:
                if chunk not in ['-', '--']:
                    if chunk not in temp_dict:
                        temp_dict[chunk]=1
                    else:
                        temp_dict[chunk]=temp_dict[chunk]+1
    for key in temp_dict:
        if key in index:
            index[key].update({doc_id:temp_dict[key]})
        else:
            index[key]={doc_id:temp_dict[key]}

with open("unigram_inverted_list", 'wt') as file:
    for key, value in sorted(index.iteritems()):
        file.write(key + "," +str(value)+ "\n")

doc_ref_list=sorted(doc_map.items(), key=operator.itemgetter(1),reverse=False)
indx_table_to_file(doc_ref_list,"unigram_doc_ref_table")

print "unigram_index is saved."
print time.clock()

for i in index:
    value=index[i]
    for key1 in value:
        val += value[key1]
        doc_count += 1
        doc_list.append(key1)
    unigram_tf_table[i]=val
    doc_list.append(doc_count)
    unigram_df_table[i]=doc_list
    val=0
    doc_count=0
    doc_list=[]

unigram_term_sort= sorted(unigram_tf_table.items(), key=operator.itemgetter(1),reverse=True)
indx_table_to_file(unigram_term_sort, "unigram_tf_table.txt")

unigram_doc_sort= sorted(unigram_df_table.items(), key=operator.itemgetter(0),reverse=False)
doc_table_to_file(unigram_doc_sort, "unigram_df_table.txt")

print "unigram_table is saved"
print time.clock()
