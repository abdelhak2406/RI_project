import tp
import math
import copy

stopwordsfile='stopwords/stopwords_eng.txt'
datapath='data/cacm.all'
stopword_list=open(stopwordsfile, "r", encoding="utf-8").read().splitlines()

#from file, makes dictionarry with doc_id as its key, and
#title+ resume as its content
def read_data() :
    docs={}
    with open(datapath, 'r+', encoding='utf-8') as file:
        res=''
        title=''
        for lines in file :
            if (lines[0]=='.') & (lines[1]=='I') :
                id=lines.strip('.I ')
                id=id.strip()

            if (lines[0]=='.') & (lines[1]=='T'):
                nex=next(file).strip()
                while nex[0]!='.' :
                    title=title+' '+nex
                    nex=next(file).strip()
            
                if (nex[0]=='.') & (nex[1]=='W'):
                    nex=next(file).strip()
                    while nex[0]!='.' :
                        res=res+' '+nex
                        nex=next(file).strip()
                
            if (lines[0]=='.') & (lines[1]=='X'):
                docs[id]={'title':title,'resume':res}
                res=''
                title=''

    file.close()
    return docs


#cleans list_doc
def tokenization(docs) :
    detailed_doc={}
    for key in docs:
        title=doc[key]['title']
        resume=doc[key]['resume']
        
        title = tp.Stopword_elimination(title)
        resume = tp.Stopword_elimination(resume)
        content=title+resume
        content=tp.dict_freq(content)

        detailed_doc[key]=content
        
    return detailed_doc
        

#list of terms, contains list of docs it appears in + its frequency
def idf(data):
    idf_list={}
    for d in data :
        for element in data[d]:
            if element not in idf_list :
                doc_fr={}
                for d2 in data :
                    if element in data[d2]:
                        doc_fr[d2]=data[d2][element]
                idf_list[element]=doc_fr
    return idf_list
                

def get_doc_details(data_doc,di):
    return data_doc[di]

def get_term_details(data_term,term):
    return data_term[term]

def maxFreq(dj):
    all_values = dj.values()
    max_value = max(all_values)
    return max_value


def idf_ponderation(idfL,list_doc):

    for term in idfL:
        ni=len(term)
        for doc in idfL[term]:
            max=maxFreq(list_doc[str(doc)])
            idfL[term][doc]=(idfL[term][doc]/max)*math.log(len(list_doc)/ni+1,10)
    
    return idfL



def replace_logical_by_mathematical_operators(request):
    request = request.replace("and", "*").replace("or", "+")
    partitioned_request = list(request.partition("not"))
    for i in range(0, len(partitioned_request)-1):
        if partitioned_request[i] == "not":
            partitioned_request[i] = "int(not"
            partitioned_request[i+1] = partitioned_request[i+1] + ")"
    
    temp_request = ""
    for i in range(0, len(partitioned_request)):
        temp_request += partitioned_request[i]
    return temp_request


def boolean_model(request:str,list_doc):
    request = request.lower()
    operator_list={'and','or','not','(',')'}
    request_list = request.split()
    termes_in_doc = {}
    pertinent_docs = []

    for i in range(1,len(list_doc)+1):
        for term in request_list:
            if term not in operator_list and term in list_doc[str(i)].keys():
                termes_in_doc[term] = 1
            else:
                termes_in_doc[term] = 0

        temp_request = request
        for term in termes_in_doc.keys():
            if term not in operator_list:
                temp_request = temp_request.replace(term, str(termes_in_doc[term]))
        
        if eval(replace_logical_by_mathematical_operators(temp_request)):
            pertinent_docs.append(i)

    return pertinent_docs


if __name__ == '__main__':
    doc=read_data()
    list_doc=tokenization(doc)
    idf_list=idf(list_doc)
    idf_clone = copy.deepcopy(idf_list)
    weighted_idf=idf_ponderation(idf_clone,list_doc)

    print(list_doc)
    print('----------------\n'*5,idf_list)
    print('----------------\n',weighted_idf)
    print('-----------------\n',boolean_model('goal or parameters',list_doc))
    


