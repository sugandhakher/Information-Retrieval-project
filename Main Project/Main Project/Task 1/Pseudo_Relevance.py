import BM25
import operator
import time
import math

print "starting psuedo relevance model"
print time.clock()
query=""
bm25_score_list=BM25.process_query(query)
top_score_doc=[]
doc_ref_table=BM25.document_map
i=1
query_suggest=""
# loading top_score_dict using bm25_score_list
for key,value in bm25_score_list:
    if i <= 10:
        top_score_doc.append(key)
        i += 1
# going to generate a snippet
for doc in top_score_doc:
    temp_dict={}
    temp_list=[]
    words=0
    doc_snippet_word_list=generateSnippet(doc_ref_table[doc])
    with open(doc_ref_table[doc]+ ".txt",'rt') as f:
        for line in f:
            line=line.split("\n")[0]
            chunks=line.split()
        for chunk in chunks:
            if chunk in doc_snippet_word_list:  # not checking for stop words here, becoz, snippet will not have them
                if chunk not in temp_dict:
                    temp_dict[chunk]=1
                else :
                    temp_dict[chunk]=temp_dict[chunk]+1
                #total_term +=1
        temp_list=sorted(temp_dict.items(), key=operator.itemgetter(1),reverse=True)
        for key,value in temp_list:
            if words <= 4:
                query_suggest=' '.join(key)
                words += 1
print query_suggest












