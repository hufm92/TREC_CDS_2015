# TREC CDS 2015
# Extract the pmc-id from TREC-format output
# Author: Fengmin Hu

import sys
import re
Filename = sys.argv[1]
Outname = sys.argv[2]
inputfile = open(Filename, 'rU')
outputfile = open(Outname,'wb')
data = inputfile.readlines()
pattern = re.compile(r'\/\d*\.')
for item in data:
    tmp = item.strip().split()
    Reg_Match = re.search(pattern,tmp[2])
    doc_num = Reg_Match.group()[1:-1]
    tmp[2] = doc_num
    outputfile.writelines(" ".join(tmp)+'\n')

inputfile.close()
outputfile.close()
