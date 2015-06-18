# TREC CDS 2015
# Compare the PMID from MetaMapped collection and TREC corpus
# Author: Fengmin Hu

FileTREC = open('PMID_TREC.txt','rU')
Data = FileTREC.readlines()
PMID_TREC = list()
for item in Data:
    PMID_TREC.append(int(item.strip().split()[1]))

PMID_MetaMap = list()
FileMetaMap = open('PMID_5.txt','rU')
Data = FileMetaMap.readlines()
for item in Data:
    PMID_MetaMap.append(int(item.strip()))

FileMetaMap = open('PMID_6.txt','rU')
Data = FileMetaMap.readlines()
for item in Data:
    PMID_MetaMap.append(int(item.strip()))

PMID_MetaMap.sort()
PMID_TREC.sort()
Overlap = list()
i = 0
j = 0
num_TREC = len(PMID_TREC)
num_MetaMap = len(PMID_MetaMap)
while (i < num_TREC) and (j < num_MetaMap):
    if PMID_TREC[i] == PMID_MetaMap[j]:
	Overlap.append(PMID_TREC[i])
	i += 1
	j += 1
    elif PMID_TREC[i] < PMID_MetaMap[j]:
	i += 1
    else:
	j += 1

print len(Overlap)

OutputFile = open('Overlap.txt','wb')
for item in Overlap:
    OutputFile.writelines(str(item)+'\n')
OutputFile.close()

