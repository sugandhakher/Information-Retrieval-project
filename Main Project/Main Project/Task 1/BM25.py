import file_handler
#import string
import operator
import time
import math
import os

index={}
unigram_index_table={}
doc_table={}
doc_score_table={}
unigram_index_tbl_link=[]
index_file="unigram_index.txt"
unigram_trmfreq_file="unigram_trmfrq_table.txt"
unigram_docfrq_file="unigram_docfrq_table.txt"
parsed_Corpus_dir=".\ParsedCorpus\\"
doc_ref_file="unigram_doc_ref.txt"
tf_dict={}
val=0
doc_count=0
doc_list=[]
document_map={}
document_list=[]
unigram_doc_tbl_link=[]
x=0
title_exclude=['-','_']
N=0
query_file_dict={}
dl={}
sum_dl=0
avdl=0
k1 = 1.2
k2 = 500 # should be between 0 to 1000
b = 0.75 # should be between 0 to 1
k={}
parsed_corpus_dir="./ParsedCorpus/"

# funtion to process query


try:
    for filename in os.listdir(parsed_corpus_dir):
        #title=filename.split("/")[-1]
        title=filename.split('.')[0]
        #title=''.join(ch for ch in title if ch not in title_exclude)
        #file=filename
        temp_dict={}
        temp_dict1={}
        N += 1
        x += 1
        doc_id=x
        document_map[doc_id]=title
        document_list.append(doc_id)
        #print " Now working on file : " + file + " " + str(doc_id)
        with open(parsed_corpus_dir+filename,'rt') as f: # reading the parsed file content
            total_term = 0
            for line in f:
                line=line.split("\n")[0]
                chunks=line.split()
                for chunk in chunks:
                    #total_term +=1
                    if chunk not in ['-','--']:  ## added  to remove - and -- from final list of terms
                        total_term +=1
                        if chunk not in temp_dict:
                            temp_dict[chunk]=1
                            #total_term +=1
                        else :
                            temp_dict[chunk]=temp_dict[chunk]+1
                            #total_term +=1
        #for key in temp_dict:
            #temp_dict1[key]=float(temp_dict[key])/total_term
        tf_dict[doc_id]=temp_dict
        #tf_dict[title]=temp_dict
        dl[doc_id] = total_term
        sum_dl += total_term
        for key in temp_dict:
            if key in index:
                index.get(key).update({doc_id:temp_dict[key]})
            else:
                index[key]={doc_id:temp_dict[key]}
    #print dl
    #file_handler.dict_to_file(index,index_file)
    document_ref_list=sorted(document_map.items(), key=operator.itemgetter(0),reverse=False)
    file_handler.indx_table_to_file(document_ref_list,doc_ref_file)
    print "unigram_index is created."
    #print index
    print time.clock()

    avdl=float(sum_dl)/N
    for doc in tf_dict:
        k[doc]=k1*((1-b) + b*(float(dl[doc])/avdl))
    #print k
    print "k dict is created"
    print time.clock()
    #print normalised_tf_dict[3]

    #doing task 3 for unigrams
    for each_index in index:
        #command to read value of each index
        value = index[each_index]
        for key in value:
            #print value[key]
            #val += value[key]
            doc_count += 1
            #doc_list.append(key)
        #unigram_index_table[each_index]= val
        #doc_list.append(doc_count)
        #unigram_doc_table[each_index]=doc_list
        doc_table[each_index]=doc_count
        #val = 0
        doc_count=0
    #print doc_table
        #doc_list=[]
    #unigram_index_tbl_link=sorted(unigram_index_table.items(), key=operator.itemgetter(1),reverse=True)
    #unigram_doc_tbl_link=sorted(unigram_doc_table.items(), key=operator.itemgetter(0),reverse=False)
    #file_handler.indx_table_to_file(unigram_index_tbl_link,unigram_trmfreq_file)
    #file_handler.doc_table_to_file(unigram_doc_tbl_link,unigram_docfrq_file)
    print "unigram_doc_table is created"
    #print unigram_doc_table
    print time.clock()



    #print doc_table
    #print "doc_table printed"
    #print tf_dict
    #print "tf_dict printed"
    ## processing of query##############################
    # query_file_dict=file_handler.read_query(query_file)
    # print query_file_dict
    # for query_id in query_file_dict:
    #     query=query_file_dict[query_id]
    #     print "working on query : " + query
    #     bm25_score_list=process_query(query)
    #     #print bm25_score_list
    #     file_handler.print_ranked_doc(bm25_score_list,query_id,"Taneja_System","Q"+str(query_id)+"_BM25_score.txt")
    #     print query + " is processed"
    #     print time.clock()
except Exception as e:
    print(str(e))



