# TREC CDS 2015
# Extract the PMID from MetaMapped Data.
# Author: Fengmin Hu

import os

Dir = '/storage4/users/vgvinodv/Metamapped_MedLine/parsedData/6'
FileList = os.listdir(Dir)
PMID = list()
for item in FileList:
    if item.startswith('d'):
	Dir_cur = Dir+'/'+item
	InputFile = open(Dir_cur, 'rU')
	Data_Raw = InputFile.readlines()
	for i in Data_Raw:
	    PMID.append(i.strip().split('\t')[0])
	#if i.strip().split('\t')[0] == '17417612':
	#    print item+'\n'+i
	InputFile.close()

OutputFile = open('PMID_6.txt','wb')
for item in PMID:
    OutputFile.writelines(item+'\n')
OutputFile.close()

