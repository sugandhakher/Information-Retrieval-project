import bs4
import collections
#from xml.dom.minidom import parse
#import xml.dom.minidom


def process_query():
    fo = open('../cacm.query', "r+")
    soup = bs4.BeautifulSoup(fo, 'html.parser')
    bodyContent = soup.find_all('doc')
    query_dict=collections.OrderedDict()
    for k in bodyContent:

        query_id=k.docno.get_text().encode("utf-8").strip()
        #query_id.strip()
        #print query_id

        query=k.contents[2].encode("utf-8").replace('\n'," ").rstrip().lstrip()
        #query=query.rstrip()
        #query=query.lstrip()


        query_dict[query_id]=query

    #print query_dict
    #query_page_loc="../cacm.query"
    # fo = open(filename, "r+")
    # soup = BeautifulSoup(fo.read())
    # bodyContent = soup.find_all("DOC")
    #
    # print bodyContent
#tree = ET.parse(query_page_loc)

#doc_no=tree.findtext("DOC/DOCNO")
#print doc_no

#query_page_loc="../cacm.query"
#process_query(query_page_loc)


