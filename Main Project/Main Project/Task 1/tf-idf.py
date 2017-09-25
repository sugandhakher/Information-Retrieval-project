import file_handler
import string
import operator
import time
import math
import os
import Query_Parser
from collections import OrderedDict

index={}
unigram_index_table={}
unigram_doc_table={}
doc_score_table={}
unigram_index_tbl_link=[]
filename="URLS.txt"
index_file="unigram_index.txt"
unigram_trmfreq_file="unigram_trmfrq_table.txt"
unigram_docfrq_file="unigram_docfrq_table.txt"
parsed_Corpus_dir=".\ParsedCorpus\\"
doc_ref_file="unigram_doc_ref.txt"
query_file='../cacm.query'
normalised_tf_dict={}
query_file_dict=OrderedDict()
val=0
doc_count=0
doc_list=[]
document_map={}
document_list=[]
unigram_doc_tbl_link=[]
x=0
title_exclude=['-','_']
N=3204
# fik= freq of kth term in ith doc - index
# N =number of docs = 1000
# nk = total freq of kth term -  unigram_doc_table
query_dict={}

#def doc_score(term,doc_id,t):
try:
    for file in os.listdir('../ParsedCorpus'):
        # print 'Test Folder/'+filename
        fo = open('../ParsedCorpus/' + file, "r+")

        temp_dict={}
        temp_dict1={}
        x += 1
        doc_id=x
        document_map[doc_id]=file.split(".")[0]
        document_list.append(doc_id)
        print " Now working on file : " + file + " " + str(doc_id)
        total_term=0
        for line in fo:
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
        for key in temp_dict:
            temp_dict1[key]=float(temp_dict[key])/total_term
        normalised_tf_dict[doc_id]=temp_dict1
        for key in temp_dict:
            if key in index:
                index.get(key).update({doc_id:temp_dict[key]})
            else:
                index[key]={doc_id:temp_dict[key]}

    #file_handler.dict_to_file(index,index_file)
    document_ref_list=sorted(document_map.items(), key=operator.itemgetter(0),reverse=False)
    file_handler.indx_table_to_file(document_ref_list,doc_ref_file)


    #print normalised_tf_dict[3]
    print "unigram_index is created."
    print time.clock()
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
        unigram_doc_table[each_index]=doc_count
        #val = 0
        doc_count=0
    #print unigram_doc_table
        #doc_list=[]
    #unigram_index_tbl_link=sorted(unigram_index_table.items(), key=operator.itemgetter(1),reverse=True)
    unigram_doc_tbl_link=sorted(unigram_doc_table.items(), key=operator.itemgetter(0),reverse=False)
    #file_handler.indx_table_to_file(unigram_index_tbl_link,unigram_trmfreq_file)
    file_handler.doc_table_to_file(unigram_doc_tbl_link,unigram_docfrq_file)
    print "unigram_doc_table is created"
    #print unigram_doc_table
    print time.clock()

    query_file_dict = Query_Parser.get_all_queries(query_file)
    print query_file_dict
    for query_id in query_file_dict:
        query = query_file_dict[query_id]
        print "working on query : " + query
        doc_weight_score_dict = {}

        for doc in normalised_tf_dict:
            #print doc
            doc_weight_score = 0.0
            for term in query.split():
                #print term, unigram_doc_table[term],doc,
                if term in unigram_doc_table:
                    idf= math.log(float(N)/(unigram_doc_table[term]))
                else:
                    idf = 0.0
                if term in normalised_tf_dict[doc]:
                    weight = normalised_tf_dict[doc][term] * idf
                else:
                    weight = 0.0
                #print (normalised_tf_dict[doc][term] * idf), unigram_doc_table[term]
                #print weight
                doc_weight_score += weight
            #print doc_weight_score
            doc_weight_score_dict[document_map[doc]]=doc_weight_score
            #print doc_weight_score_dict
            #print str(doc) + " | " + str(doc_weight_score)

        ranked_list = []
        # sorting on the basis of cosine score
        ranked_list = sorted(doc_weight_score_dict.items(), key=operator.itemgetter(1), reverse=True)
        print "tf-idf_score_list created"
        file_handler.print_ranked_doc(ranked_list, query_id, "tf-idf_System", "./Task1"+"Q"+str(query_id)+"_tf-idf_score.txt")
        #doc_weight_score=0
            #print "Printing normalised_tf_dict"
    #print "Printing normalised_tf_dict"
    #print term_weight_doc_dict
    #print normalised_tf_dict[3]
    #print doc_weight_score_dict[1]
    print "scored ranks is created"
    print time.clock()




except Exception as e:
    print(str(e))
