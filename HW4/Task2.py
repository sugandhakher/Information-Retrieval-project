import time
import operator
import math

index={}
unigram_index={}
unigram_tf_table={}
unigram_df_table={}
filename="URLS.txt"
parsed_corpus=".\Parsed_temp\\"
doc_count=0
doc_list=[]
val=0
doc_map={}
unigram_doc_link=[]
x=0
title_exclude=['-','_']
N=1000
normalised_tf_dict={}

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
            f.write(str(key) + ", " + str(value) + "\n")

def read_query(filename):
    t_dict={}
    with open(filename,'rt') as f:
        for line in f:
            line=line.split("\n")[0]
            line=line.split("|")
            t_dict[line[0]]=line[1]
    return t_dict

def print_ranked_doc(cosine_score_list,query_id,system_name,filename):
    i=1
    with open(filename,'wt') as f:
            for key,value in cosine_score_list:
                if i <= 100:
                    f.write(str(query_id) + " Q0 " + str(key) + " "+str(i) + " " + str(value) + " " + system_name + "\n")
                    i += 1
                else:
                    break

url_list=[]
url_list= load_URL(url_list,filename)
for url in url_list:
    title=url.split("/")[-1]
    title=''.join(ch for ch in title if ch not in title_exclude)
    file=parsed_corpus +title + ".txt"
    temp_dict={}
    tf_dict={}
    x+=1
    doc_id=x
    doc_map[doc_id]=title
    #print " Now working on file : " + file + " " + str(doc_id)

    with open(file,'rt') as f:
        terms=0
        for line in f:
            line=line.split("\n")
            chunks=line[0].split()
            for chunk in chunks:
                if chunk not in ['-', '--']:
                    terms +=1
                    if chunk not in temp_dict:
                        temp_dict[chunk]=1
                    else:
                        temp_dict[chunk]=temp_dict[chunk]+1
                        #terms+=1

    #print temp_dict normalised
    print time.clock()
    for key in temp_dict:
        tf_dict[key]=float(temp_dict[key])/terms
    normalised_tf_dict[doc_id]=tf_dict

    for key in temp_dict:
        if key in index:
            index[key].update({doc_id:temp_dict[key]})
        else:
            index[key]={doc_id:temp_dict[key]}

unigram_doc_ref= sorted(doc_map.items(), key=operator.itemgetter(0),reverse=False)
doc_table_to_file(unigram_doc_ref, "unigram_doc_ref.txt")

for i in index:
    value=index[i]
    for key1 in value:
        #val += value[key1]
        doc_count += 1
    #unigram_tf_table[i]=val
    #doc_list.append(doc_count)
    unigram_df_table[i]=doc_count
    #val=0
    doc_count=0
    #doc_list=[]


# unigram_term_sort= sorted(unigram_tf_table.items(), key=operator.itemgetter(1),reverse=True)
# indx_table_to_file(unigram_term_sort, "unigram_tf_table.txt")

unigram_doc_sort= sorted(unigram_df_table.items(), key=operator.itemgetter(0),reverse=False)
doc_table_to_file(unigram_doc_sort, "unigram_df_table.txt")

print time.clock()

for doc in normalised_tf_dict:
    for term in normalised_tf_dict[doc]:
        idf= 1+ math.log(N/unigram_df_table[term])
        normalised_tf_dict[doc][term] *= idf
print normalised_tf_dict[1]


# query_dict={}
# query_dict1={}
# total_term=0
# query="global warming potential"
# query_term=query.split()
# for term in query_term:
#     if term not in query_dict:
#         query_dict[term]=1
#         total_term +=1
#     else:
#         query_dict[term] +=1
#         total_term +=1
#
# for key in query_dict:
#     query_dict1[key]=float(query_dict[key])/total_term
# for term in query_dict1:
#     idf= 1+ math.log(N/unigram_df_table[term])
#     query_dict1[term] *= idf
#
# print query_dict1


#processing dij
doc_weight=0
doc_weight_dict={}
for doc in normalised_tf_dict:
    for term in normalised_tf_dict[doc]:
        idf= 1 + math.log(float(N)/unigram_df_table[term])
        normalised_tf_dict[doc][term] *= idf
        doc_weight += normalised_tf_dict[doc][term] * normalised_tf_dict[doc][term]
    doc_weight_dict[doc]=doc_weight
    doc_weight=0
    print "Printing normalised_tf_dict"

#processing qij
query_dict=read_query("query")
print query_dict
for id in query_dict:
    query=query_dict[id]
    query_temp_dict={}
    total_term=0
    query_weight=0
    query_term=query.split()
    for term in query_term:
        if term not in query_temp_dict:
            query_temp_dict[term]=1
            total_term+=1
        else:
            query_temp_dict[term] +=1

    for key in query_temp_dict:
        query_temp_dict[key]=float(query_temp_dict[key])/total_term
    for term in query_temp_dict:
        idf=1
        query_temp_dict[term] *=idf
        query_weight += query_temp_dict[term] * query_temp_dict[term]
    print query_temp_dict

#calculating cosine formula
    sum=0
    temp_sum=0
    cosine_score={}
    for doc in normalised_tf_dict:
        for term in query_term:
            if term in normalised_tf_dict[doc]:
                temp_score=normalised_tf_dict[doc][term] * query_temp_dict[term]
            else:
                temp_score=0
            sum += temp_score

        temp_sum=math.sqrt(doc_weight_dict[doc] * query_weight)
        cosine_score[doc_map[doc]]=float(sum)/temp_sum
        sum=0

    cosine_score_list=[]
    cosine_score_list=sorted(cosine_score.items(),key=operator.itemgetter(1),reverse=True)
    print cosine_score
    print_ranked_doc(cosine_score_list,id,"Sugandha","Q"+id+".txt")







