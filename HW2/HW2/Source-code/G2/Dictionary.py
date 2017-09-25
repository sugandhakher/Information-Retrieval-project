#creating a dictionary out of the graph file

class page_rank_dict:
    dict1 = {}
    dict2 = {}

    #initialising
    def __init__(self): pass

    #creating inlink dictionary-- dict1 and outlink dictionary-- dict2
    def inlink_dic(self):
        myFile = open('C:\Python27\IR\HW2\Task1\G2.txt', 'r')
        
        #myFile = open('C:\Python27\IR\Page_Rank\sample graph.txt', 'r')
        for line in myFile:
            line1=line.split('\n')
            line2=line1[0].split(' ')
            key=line2[0]
            value=line2[1:]
            page_rank_dict.dict1[key]=value
            # if value not in page_rank_dict.dict1[key]:
            #     continue
            page_rank_dict.dict2[key]=[]
        for key in page_rank_dict.dict1:
            value=page_rank_dict.dict1[key]
            if len(value) >0:
                for link in value:
                    page_rank_dict.dict2[link].append(key)



c = page_rank_dict()
c.inlink_dic()
#print c.dict1
#print c.dict2
# print c.dict1.keys()
# print c.dict1.values()
# print c.dict2.keys()
# print c.dict2.values()





