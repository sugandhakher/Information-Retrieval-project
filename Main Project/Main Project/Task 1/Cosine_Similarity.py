import file_handler
import string
import operator
import time
import math
#import File_Convertor

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
normalised_tf_dict={}
val=0
doc_count=0
doc_list=[]
document_map={}
document_list=[]
unigram_doc_tbl_link=[]
x=0
title_exclude=['-','_']
N=1000
# fik= freq of kth term in ith doc - index
# N =number of docs = 1000
# nk = total freq of kth term -  unigram_doc_table
query_dict={}
query_file="query.txt"
query_file_dict={}
#def doc_score(term,doc_id,t):
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
            total_term=0
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
    # revising weights using inverse doc frequency
    # for doc in normalised_tf_dict:
    #     for term in normalised_tf_dict[doc]:
    #         idf=1+ math.log(N/unigram_doc_table[term])
    #         normalised_tf_dict[doc][term]= normalised_tf_dict[doc][term] * idf
    # changing it to update for terms present in query only
    # query="global warming potential"
    # query_term=query.split()
    # term_weight_doc_dict={}
    # print "going to create weight_term_doc_dict"
    # for term in query_term:
    #     for doc in normalised_tf_dict:
    #         if term in normalised_tf_dict[doc]:
    #             idf = 1 + math.log(N/unigram_doc_table[term])
    #             if doc in term_weight_doc_dict:
    #                 print "if doc is present in weight_term_doc_dict and term is present in normalised_tf_dict"
    #                 term_weight_doc_dict[doc].update({term:normalised_tf_dict[doc][term] * idf})
    #             else:
    #                 "if doc is not present in weight_term_doc_dict and term is present in normalised_tf_dict"
    #                 term_weight_doc_dict[doc]={term:normalised_tf_dict[doc][term] * idf}
    #         else:
    #             if doc in term_weight_doc_dict:
    #                 "if doc is present in weight_term_doc_dict and term is not present in normalised_tf_dict"
    #                 term_weight_doc_dict[doc].update({term : 0})
    #             else:
    #                 "if doc is not present in weight_term_doc_dict and term is present in normalised_tf_dict"
    #                 term_weight_doc_dict[doc]={term : 0}
    doc_weight_score=0
    doc_weight_score_dict={}
    #for doc in normalised_tf_dict:
    for doc in normalised_tf_dict:
        for term in normalised_tf_dict[doc]:
            idf= 1 + math.log(float(N)/unigram_doc_table[term])
            normalised_tf_dict[doc][term] = normalised_tf_dict[doc][term] * idf
            doc_weight_score += normalised_tf_dict[doc][term] * normalised_tf_dict[doc][term]
        doc_weight_score_dict[doc]=doc_weight_score
        #print str(doc) + " | " + str(doc_weight_score)
        doc_weight_score=0
            #print "Printing normalised_tf_dict"
    print "Printing normalised_tf_dict"
    #print term_weight_doc_dict
    #print normalised_tf_dict[3]
    #print doc_weight_score_dict[1]
    print "normalised_tf_dict is created"
    print time.clock()

    ## processing of query##############################
    query_file_dict=file_handler.read_query(query_file)
    print query_file_dict
    for query_id in query_file_dict:
        query=query_file_dict[query_id]
        print "working on query : " + query
        query_temp_dict={}
        total_term=0
        query_weight_score=0
        query_term=query.split()
        # doc_weight_score=0
        # doc_weight_score_dict={}
        # #for doc in normalised_tf_dict:
        # for doc in normalised_tf_dict:
        #     for term in normalised_tf_dict[doc]:
        #         idf= 1 + math.log(float(N)/unigram_doc_table[term])
        #         normalised_tf_dict[doc][term] = normalised_tf_dict[doc][term] * idf
        #         if term in query_term:
        #             doc_weight_score += normalised_tf_dict[doc][term] * normalised_tf_dict[doc][term]
        #     doc_weight_score_dict[doc]=doc_weight_score
        # #print str(doc) + " | " + str(doc_weight_score)
        #     doc_weight_score=0
        # print "Now printing doc_weight_score_dict"
        # print doc_weight_score_dict

        for term in query_term:
            if term not in query_temp_dict:
                query_temp_dict[term] = 1
                total_term += 1
            else:
                query_temp_dict[term]=query_temp_dict[term] + 1
                total_term += 1
        for key in query_temp_dict:
            query_temp_dict[key]=float(query_temp_dict[key])/total_term
        for term in query_temp_dict:
            #idf=1 + math.log(float(N)/unigram_doc_table[term])
            idf = 1
        #print str(unigram_doc_table[term])
        #print str(idf) + "for term" + term
            query_temp_dict[term]= query_temp_dict[term] * idf
            query_weight_score += query_temp_dict[term] * query_temp_dict[term]
        print query_temp_dict
        print "query weight score is " + str(query_weight_score)

    # calculating cosine formula
        num_sum=0
        den_sum=0
        cosine_score={}
        for doc in normalised_tf_dict:
            for term in query_term:
                if term in normalised_tf_dict[doc]:
                    temp_score=normalised_tf_dict[doc][term] * query_temp_dict[term]
                else:
                    temp_score=0
                num_sum += temp_score

            den_sum = math.sqrt(doc_weight_score_dict[doc] * query_weight_score)
            if den_sum == 0:
                cosine_score[document_map[doc]]=0
            else:
                cosine_score[document_map[doc]]=float(num_sum)/den_sum
            #print str(doc) + " | " + str(cosine_score[doc]) + "\n"
            num_sum=0
        #print cosine_score
        cosine_score_list=[]
        # sorting on the basis of cosine score
        cosine_score_list=sorted(cosine_score.items(),key=operator.itemgetter(1),reverse=True)
        print "cosine_score_list created"
        file_handler.print_ranked_doc(cosine_score_list,query_id,"Taneja_System","Q"+query_id+".txt")
except Exception as e:
    print(str(e))



