import file_handler
import BM25
import time
import Query_Parser as qp
import collections
import operator
import math

query_file="../cacm.query"
query_file_dict=collections.OrderedDict()
bm25_res_dir="./bm25_result/"
rel_doc="../cacm.rel"
#query_dict={}
R={}


def find_query(task_name):
    if task_name=="task1":
        query_file_dict=qp.get_all_queries(query_file)
        create_R_dict()
    print query_file_dict
    #creating a dictionary R which has relevance info given by her
    for query_id in query_file_dict:
        RI={}
        #for query_id,query in row:
        query=query_file_dict[query_id]
        print "working on query : " + query
        # adding relevance info
        RI=create_R_dict(query_id,query)
        if query_id in R:
            rel_doc_count=len(R[query_id])
        else:
            rel_doc_count=0
        bm25_score_list=process_query(query,RI,rel_doc_count)
        #print bm25_score_list
        file_handler.print_ranked_doc(bm25_score_list,query_id,"Taneja_System",bm25_res_dir+"Q"+str(query_id)+"_BM25_score.txt")
        print query + " is processed"
        print time.clock()


def process_query(query,ri,rel_dc_cnt):
    bm25_score={}
    query_dict={}
    query_term=query.split()
    for term in query_term:
        if term not in query_dict:
            query_dict[term] = 1
        else:
            query_dict[term]=query_dict[term] + 1
    #print query_dict
    print "query_dict is created"
    print time.clock()
        #computing BM25 score here
    for doc in BM25.tf_dict:
        bm25_doc_sum = 0
        for term in query_dict:
            p1=0
            p2=0
            p3=0
            if term in BM25.tf_dict[doc]:
               # print "ri for " + str(term) + " is " + str(ri[term])
                #print "N is " + str(BM25.N)
                #print "doc table value is " + str(BM25.doc_table[term])
                #print "R is " + str(rel_dc_cnt)
                p1 = float((ri[term] +0.5)*(BM25.N - BM25.doc_table[term] - rel_dc_cnt + ri[term]+ 0.5)) / \
                     ((rel_dc_cnt - ri[term] + 0.5)*(BM25.doc_table[term] - ri[term] + 0.5))
                p2 = float((BM25.k1 + 1) * BM25.tf_dict[doc][term]) / (BM25.k[doc] + BM25.tf_dict[doc][term])
                p3 = float((BM25.k2 + 1) * query_dict[term]) / (BM25.k2 + query_dict[term])
                # added if cond to prevent math domain error caused because log cant processes -ve value
                #if p1 > 0:
                bm25_doc_sum += math.log(p1) * p2 * p3
        bm25_score[doc]=bm25_doc_sum
        #print bm25_score
    print "BM25_score dict is created"
    print time.clock()
    bm25_score_list=sorted(bm25_score.items(), key=operator.itemgetter(1),reverse=True)
    return bm25_score_list


def create_R_dict():
    with open(rel_doc,'rt') as f:
        for line in f:
            chunk=line.split()
            if chunk[0] not in R:
                R[chunk[0]]=[chunk[2]]
            else:
                R[chunk[0]].append(chunk[2])
    #print R

def create_RI_dict(queryid,query):
    temp={}
    chunks=query.split()
    for chunk in chunks:
        count=0
        if queryid in R:
            for page in R[queryid]:
                file=BM25.parsed_corpus_dir+page+".txt"
                #if chunk in open(file).read():
                b=check_chunk(chunk,file)
                if b is True:
                    #print "Chunk "  + str(chunk) + "found in doc " + str(file)
                    count += 1
        temp[chunk]=count
    return temp

def check_chunk(chunk1,file1):
    b=False
    with open(file1,'rt') as f:
        for line in f:
            chunks=line.split()
            for chunk in chunks:
                if chunk1==chunk:
                    #print "In file " + str(file1) + "at line : " + str(line)
                    b=True
                break
        return b



def process_query_without_relevance(query):
    temp_ri=create_RI_dict('S1',query)
    rel_doc=0
    process_query(query,temp_ri,rel_doc)

