from Dictionary import *
import math
import decimal
import operator

#dict1 is the inlink dictionary
#dict2 is the outlink dictionary
#class page_rank_dict() calls for the function that creates the dictionary

c = page_rank_dict()
c.inlink_dic()
# P is the set of all pages i.e., keys in the inlink dictionary dict1 (unordered)
P = []
P = c.dict1.keys
# N is the total number of pages i.e., |P|=N
N = len(c.dict1.keys())
#d is the PageRank damping factor
d = 0.85

# calculating links with no inlinks in dict1 in G1
no_inlink = []
count1 = 1
for link in P():
    value=c.dict1[link]
    if len(value) == 0:
        no_inlink.append(link)
        count1 += 1
# with open("G1_no_inlink.txt",'wt') as f:
#     for link in no_inlink:
#         f.write(link +'\n')
# print count1

# sink is the set of sink nodes i.e., pages with no outlinks (keys in dict2 having null values)
Sink = []
count=0
for link in P():
    value=c.dict2.get(link, None)
    if len(value) == 0:
        Sink.append(link)
        count +=1
# with open("G1_no_outlink.txt",'wt') as f:
#     for link in Sink:
#         f.write(link +'\n')
# print count



def page_rank():
    PR = {}
    newPR = {}
    entropy=0
    new_entropy=0
    new_perplexity = 0
    diff_per = 0
    j=0
    x=0
    for p in P():
        num = 1/float(N)
        PR[p]=num
    while j < 4:
        x+=1
        sinkPR = 0
        for p in Sink:
            sinkPR += PR[p]
        for p in P():
            newPR[p] = (1 - d)/N
            newPR[p] += (d * sinkPR)/N
            str_in = c.dict1[p]
            if len(str_in) > 0:
                for i in str_in:
                    pg=i
                    pr_value= PR[pg]
                    str_out = c.dict2[pg]
                    str_out_list_len = len(str_out)
                    newPR[p] += (d * pr_value) / (str_out_list_len)

        new_entropy=0
        entropy=0
        for p in P():
            new_entropy += (newPR[p] * math.log(newPR[p], 2))
        new_entropy = -new_entropy
        print 'new_entropy= ' + str(entropy)
        for p in P():
            entropy += (PR[p] * math.log(PR[p], 2))
        entropy = -entropy
        #print 'entropy= ' + str(new_entropy)
        for p in P():
            PR[p] = newPR[p]

        perplexity=math.pow(2,entropy)
        new_perplexity=math.pow(2,new_entropy)
        print "perplexity for loop " + str(x)
        print str(new_perplexity)
        diff_per = new_perplexity - perplexity
        if diff_per < 1:
            j += 1
        else:
            j=0
        print 'End of loop ' + str(x)
        #print diff_per
    PR=sorted(PR.items(), key=operator.itemgetter(1), reverse=True)
    #print PR
    # getting top 50 page ranks in a file
    i=0
    with open("page-rank-file-G1",'wt') as f:
         for link in PR:
             if i>= 50:
                 break
             f.write(str(link)+'\n')
             i+=1








page_rank()



