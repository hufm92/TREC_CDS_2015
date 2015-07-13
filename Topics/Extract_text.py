# 2015 TREC CDS
# Extract free text information from xml file
# Author: Fengmin Hu

import xml.etree.ElementTree as ET

Dir = '/storage6/users/hufm/TREC/TREC_CDS_2015/Topics/topics-text/2014-original/'
topics_tree = ET.parse('topics2014.xml')
# topics_tree = ET.parse('topics2015A.xml')

root = topics_tree.getroot()
for topic in root:
    number = topic.attrib['number']
    topic_type = topic.attrib['type']
    text = list()
    text.append(topic_type+'.')
    for item in topic:
	text.append(item.text)
    outputfile = open(Dir+str(number)+'.txt','wb')
    for item in text:
	outputfile.writelines(item+'\n')
    outputfile.close()
