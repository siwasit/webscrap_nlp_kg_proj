import spacy


nlp = spacy.load("en_core_web_sm")

doc = nlp("During the Second World War in Europe, Peiper served as personal adjutant to Heinrich Himmler, leader of the SS, and as a tank commander in the Waffen-SS.")
doc0 = nlp("Joachim Peiper (30 January 1915 – 14 July 1976) was a German Schutzstaffel (SS) officer and war criminal convicted for the Malmedy massacre of U.S. Army prisoners of war (POWs).")
doc1 = nlp("German historian Jens Westemeier writes that Peiper personified Nazi ideology, as a purportedly ruthless glory-hound commander who was indifferent to the combat casualties of Battle Group Peiper, and who encouraged, expected, and tolerated war crimes by his Waffen-SS soldiers.")

def extract_subject(data):
    nsubj = ''
    for doc_ind in data:
        subtree_list = [t.dep_ for t in doc_ind.subtree]
        index = 0
        if 'nsubj' in subtree_list: 
            # print(doc_ind.text ,doc_ind.pos_, doc_ind.dep_)
            for i, dep in enumerate(subtree_list):
                if dep == 'nsubj':
                    index = i
                    break
            nsubj = [t for t in doc_ind.subtree][index]
    # print(nsubj)
    return nsubj

def extract_predicate(data, s):
    verb = None
    for doc_ind in data:
        #print('-----------------------------------', doc_ind, doc_ind.pos_ ,doc_ind.dep_)
        if (doc_ind.pos_ == 'VERB' or (doc_ind.pos_ == 'AUX' and doc_ind.dep_ == 'ROOT')) and doc_ind.is_ancestor(s):
            verb = doc_ind

    return verb

def extract_spo(data):
    nsubj = extract_subject(data)
    verb = extract_predicate(data, nsubj)
    raw = []
    n = 0
    for doc_ind in data:
        # print('-----------------------------------', doc_ind, doc_ind.pos_ ,doc_ind.dep_)
        
        if doc_ind.pos_ == 'ADP' and verb.is_ancestor(doc_ind) and list(doc_ind.ancestors) == [verb]: #เช็ค ADP ตัวขยาย verb
            # print(list(doc_ind.ancestors), [doc_ind])
            n = len(list(doc_ind.subtree))
        
        # print('-----------------------------------', doc_ind.pos_ ,doc_ind.dep_)
        # print([t.pos_ for t in doc_ind.subtree])
        if (doc_ind.pos_ == 'NOUN' or doc_ind.pos_ == 'PROPN') and (verb.pos_ in [t.pos_ for t in doc_ind.ancestors]) and (len(list(doc_ind.subtree)) + 1 == n and n != 0): #ออย่าลืม CONJ
            #
                #print(nsubj, [t for t in reversed(list(doc_ind.ancestors))], doc_ind.text)
                raw.append([nsubj, [p for p in reversed(list(doc_ind.ancestors))], doc_ind])
                #print([t.text for t in doc_ind.subtree], 'this is subtree of ',doc_ind.text)
        elif n == 0 and (doc_ind.pos_ == 'NOUN' or doc_ind.pos_ == 'PROPN') and (doc_ind != nsubj) and (list(doc_ind.ancestors) == [verb] or (doc_ind.dep_ == 'conj' and doc_ind.head in list(doc_ind.ancestors))): #and list(doc_ind.ancestors) == [verb]
            raw.append([nsubj, verb, doc_ind])
            #     print(nsubj, verb, doc_ind.text, list(doc_ind.ancestors), doc_ind.dep_, doc_ind.head)
    return raw

# for i in[doc, doc0, doc1]:
#     for j in extract_spo(i):
#         print(j)
#     print('----------------------------')

# def extract_subject_test(data):
#     nsubj = []
#     for doc_ind in data:
#         if 'nsubj' == doc_ind.dep_: 
#             print(doc_ind.text ,doc_ind.pos_, doc_ind.dep_)
#             nsubj.append(doc_ind)
#     # print(nsubj)
#     return nsubj

for i in doc0:
    print(i.text ,i.pos_, i.dep_)
    print('--------------------------------')
    
#Synta
