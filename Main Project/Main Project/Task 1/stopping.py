import file_handler
#import string
import operator
import time
import math

index={}
unigram_index_table={}
doc_table={}
doc_score_table={}
unigram_index_tbl_link=[]
filename="URLS.txt"
index_file="unigram_index.txt"
unigram_trmfreq_file="unigram_trmfrq_table.txt"
unigram_docfrq_file="unigram_docfrq_table.txt"
parsed_Corpus_dir=".\ParsedCorpus\\"
doc_ref_file="unigram_doc_ref.txt"
stop_file="common_words"
tf_dict={}
val=0
doc_count=0
doc_list=[]
document_map={}
document_list=[]
unigram_doc_tbl_link=[]
x=0
title_exclude=['-','_']
bm25_score={}
bm25_score_list=[]
N=1000
# fik= freq of kth term in ith doc - index
# N =number of docs = 1000
# nk = total freq of kth term -  unigram_doc_table
query_dict={}
query_file="query.txt"
query_file_dict={}
query_dict={}
#total_term=0
dl={}
sum_dl=0
avdl=0
k1 = 1.2
k2 = 500 # should be between 0 to 1000
b = 1# should be between 0 to 1
k={}
#def doc_score(term,doc_id,t):
# funtion to process query
def process_query(query):
    query_term=query.split()
    for term in query_term:
        if term not in query_dict:
            query_dict[term] = 1
        else:
            query_dict[term]=query_dict[term] + 1
    print query_dict
    print "query_dict is created"
    print time.clock()
        #computing BM25 score here
    for doc in tf_dict:
        bm25_doc_sum = 0
        for term in query_dict:
            p1=0
            p2=0
            p3=0
            if term in tf_dict[doc]:
                p1 = float(N - doc_table[term] + 0.5) / (doc_table[term] + 0.5)
                p2 = ((k1 + 1) * tf_dict[doc][term]) / (k[doc] + tf_dict[doc][term])
                p3 = ((k2 + 1) * query_dict[term]) / (k2 + query_dict[term])
                bm25_doc_sum += math.log(p1) * p2 * p3
            bm25_score[doc]=bm25_doc_sum
        #print bm25_score
    print "BM25_score dict is created"
    print time.clock()
    bm25_score_list=sorted(bm25_score.items(), key=operator.itemgetter(1),reverse=True)
    return bm25_score_list

try:
    URLList=[]
    URLList=file_handler.load_URL(URLList,filename)
    for url in URLList:
        title=url.split("/")[-1]
        title=''.join(ch for ch in title if ch not in title_exclude)
        file=parsed_Corpus_dir+ title + ".txt"
        temp_dict={}
        temp_dict1={}
        x += 1
        doc_id=x
        document_map[doc_id]=title
        document_list.append(doc_id)
        #print " Now working on file : " + file + " " + str(doc_id)
        with open(file,'rt') as f: # reading the parsed file content
            total_term = 0
            for line in f:
                line=line.split("\n")[0]
                chunks=line.split()
                for chunk in chunks:
                    with open(stop_file) as x:
                        for y in x:
                            y=y.split("\n")[0]
                            stop=y.split()
                            #print stop
                            if chunk not in stop:  ## added  to remove - and -- from final list of terms
                                total_term +=1
                                if chunk not in temp_dict:
                                    temp_dict[chunk]=1
                            #total_term +=1
                                else :
                                    temp_dict[chunk]=temp_dict[chunk]+1


                    #total_term +=1

                            #total_term +=1
        #for key in temp_dict:
            #temp_dict1[key]=float(temp_dict[key])/total_term
        tf_dict[doc_id]=temp_dict
        dl[doc_id]= total_term
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
    #print unigram_doc_table
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
    query_file_dict=file_handler.read_query(query_file)
    print query_file_dict
    for query_id in query_file_dict:
        query=query_file_dict[query_id]
        print "working on query : " + query
        bm25_score_list=process_query(query)
        #print bm25_score_list
        file_handler.print_ranked_doc(bm25_score_list,query_id,"Taneja_System","Q"+str(query_id)+"_BM25_score.txt")
        print query + " is processed"
        print time.clock()
except Exception as e:
    print(str(e))



