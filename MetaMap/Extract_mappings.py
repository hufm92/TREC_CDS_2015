# 2015 TREC CDS
# Extract mappings from Metamapped data
# Author: Fengmin Hu

import re
import os
import time
import string

def Parse(elem):
    phrase_st = elem[0].strip()
    mappings_st = elem[1].strip()
    if mappings_st == 'mappings([]).':
	return None
    phrase_pattern_1 = re.compile(r'phrase\(\'(.*?)\'')
    phrase_pattern_2 = re.compile(r'phrase\((.*?),')
    phrase_match_1 = re.match(phrase_pattern_1, phrase_st)
    if phrase_match_1 is not None:
	phrase = phrase_match_1.group(1)
    else:
	phrase_match_2 = re.match(phrase_pattern_2, phrase_st)
	if phrase_match_2 is None:
	    return None
	phrase = phrase_match_2.group(1) 
    phrase = phrase.strip(string.punctuation)
    mappings_pattern = re.compile(r'mappings\(\[(.*)\]\)') 
    mappings_raw = re.match(mappings_pattern, mappings_st).group(1).split('map(')
    if mappings_raw[0] == '':
	del mappings_raw[0]
    mappings = list()
    for item in mappings_raw:
	score = int(item.split(',',1)[0])
	map_text = item.split(',',1)[1].rstrip('),').strip('[]')
	mapping_cur = list()
	candidate_list = map_text.split('ev(')
	if candidate_list[0] == '':
	    del candidate_list[0]
	for candidate in candidate_list:
	    tmp_list = candidate.strip(',()').split(',',4)[:4]
	    for i in xrange(len(tmp_list)):
		tmp_list[i] = tmp_list[i].strip('\'')
	    mapping_cur.append(tmp_list)
	mappings.append([score,mapping_cur]) 
    return [phrase, mappings]

inputfile = open('PMID_Overlap.txt','rU')
PMID = list()
raw_data = inputfile.readlines()
for item in raw_data:
    tmp = item.strip().split()
    PMID.append(tmp)
inputfile.close()

print time.ctime()
Dir = '/storage6/users/vgvinodv/Metamapped_Medline/unzip/7b/'
Dir_new = '/storage6/users/hufm/TREC/TREC_CDS_2015/MetaMap/metamap-text/metamap-text-'
utterance_pattern = re.compile(r'utterance\(\'([\w.]*)\'')
text_out = os.listdir(Dir)
# text_out = ['text.out_650']
for text_out_cur in text_out:
    pmid_cur = list()
    pmcid_cur = list()
    for item in PMID:
	if item[-1] == text_out_cur:
	    pmid_cur.append(item[1])
	    pmcid_cur.append(item)

    print time.ctime()
    print text_out_cur, len(pmid_cur)
    inputfile = open(Dir+text_out_cur,'rU')
    
    count = 0
    pmid_hit = list()
    line = inputfile.readline()
    while True:
	if not line:
	    break
    	if line.startswith('utterance(') is False:
	    line = inputfile.readline()
	    continue
	utter_match = utterance_pattern.match(line)
	if utter_match is None:
	    line = inputfile.readline()
	    continue	
	utter = utter_match.group(1)
	pmid_tmp = utter.split('.')[0]
	if pmid_tmp not in pmid_cur:
	    line = inputfile.readline()
	    continue
	pmid_hit.append(pmid_tmp)
	pmcid_info = pmcid_cur[pmid_cur.index(pmid_tmp)]
	count += 1
	
	Flag = False
	Mappings = dict()
	# rawdata = dict()
	while not Flag:
	    utter_match = utterance_pattern.match(line)
	    if utter_match is None:
		Flag = True
		break
	    utter = utter_match.group(1)
	    if not utter.startswith(pmid_tmp):
		Flag = True
		break
	    Mappings[utter] = list()
	    # rawdata[utter] = list()
	    line = inputfile.readline()
	    while line.startswith('phrase'):
		phrase = line
		candidates = inputfile.readline()
		mapping = inputfile.readline()
		parse_phrase = Parse([phrase, mapping])
	
		if parse_phrase is not None:
		    Mappings[utter].append(parse_phrase)
		    # rawdata[utter].append([phrase,mapping])
		line = inputfile.readline()
	
	    while True:
		if not line:
		    Flag = True
		    break
		line = inputfile.readline()
		if line.startswith("utterance"):
		    break
	
	Directory = Dir_new + pmcid_info[3]
	if os.path.exists(Directory) == False:
	    os.mkdir(Directory)
	Outputfile = open(Directory+pmcid_info[0]+'.txt','wb')
        for utter in Mappings.keys():
	    Outputfile.writelines(utter+'\n\n')
	    for item in Mappings[utter]:
		phrase_out = item[0]
		score = str(item[1][0][0])
		Outputfile.writelines(score+','+phrase_out+'\n')
		CUI = list()
		for mapping in item[1]:
		    for candidate in mapping[1]:
			CUI.append(candidate[1])
		CUI = list(set(CUI))
		Outputfile.writelines(','.join(CUI)+'\n')
	    Outputfile.writelines('\n')
	Outputfile.close()
	
    for item in pmid_cur:
	if item not in pmid_hit:
	    print item,pmcid_cur[pmid_cur.index(item)]
	# Outputfile = open('Extract_Mapping_Test_raw.txt','wb')
	# for utter in rawdata.keys():
	#     Outputfile.writelines(utter+'\n')
	#     for item in rawdata[utter]:
	#         Outputfile.writelines(item[0]+'\n'+item[1]+'\n')
	# Outputfile.close()

    inputfile.close()
    print time.ctime()
