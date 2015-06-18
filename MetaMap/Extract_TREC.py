# TREC CDS 2015
# Extract the PMID from TREC Collection
# Fengmin Hu

import os
import re

Dir = '/storage6/users/vgvinodv/trec-cds/orig_data/pmc-text/'

DirList = os.listdir(Dir)
FolderList = list()
for item in DirList:
    if os.path.isdir(Dir+item):
	FolderList.append(Dir+item+'/')

Num_upper = len(FolderList)
for i in xrange(Num_upper):
    Tmp = FolderList[0]
    DirList = os.listdir(Tmp)
    del FolderList[0]
    for item in DirList:
	if os.path.isdir(Tmp+item):
	    FolderList.append(Tmp+item+'/')

PMID = list()
PMCID = list()
Wrong = list()
Num_notype = 0
pattern = re.compile(r'"pmid">(\d*)<')
pattern_type = re.compile(r'article-type="(.*?)"')
for Folder in FolderList:
    print Folder
    FileList = os.listdir(Folder)
    for item in FileList:
	if item.endswith('.nxml'):
	    Dir_Tmp = Folder+item
	    InputFile = open(Dir_Tmp,'rU')
	    Article_Raw = InputFile.readline()
	    Reg_Match = re.search(pattern, Article_Raw)
	    Type_Match = re.search(pattern_type, Article_Raw)
	    if Type_Match is not None:
		Type_Cur = Type_Match.group(1)
	    else:
		Type_Cur = 'None'
		Num_notype += 1
	    if Reg_Match is not None:
		PMID_tmp = Reg_Match.group(1)
		PMID.append(PMID_tmp+'\t'+Type_Cur)
		PMCID.append(item[:-5])
	    else:
		Wrong.append(item+'\t'+Type_Cur)
	    InputFile.close()

print Num_notype

OutputFile = open('PMID_TREC.txt','wb')
Num_PMID = len(PMID)
for i in xrange(Num_PMID):
    OutputFile.writelines(PMCID[i]+'\t'+PMID[i]+'\n')
OutputFile.close()

OutputFile = open('Wrong.txt','wb')
for item in Wrong:
    OutputFile.writelines(item+'\n')
OutputFile.close()
