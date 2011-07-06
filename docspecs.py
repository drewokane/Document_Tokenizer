'''
Created on Feb 21, 2011

@author: deokane
'''

from scipy import stats
import math
from leglindex import bowcat
from legdoc import *
#import matplotlib.pyplot as pyplot
import os
from operator import itemgetter


path1 = "C:\\Users\\deokane\\Documents\\Eclipse\\MAC_parser\\src"

files = os.listdir(os.getcwd())
defm14as = [name for name in files if name.find(".txt") is not -1]

word_bag = bowcat(defm14as)

doc = MACdoc(defm14as[0])

word_freq = doc.WordFreq(word_bag)
reorder = sorted(word_freq.iteritems(),key=itemgetter(1),reverse=True)
docs_dict_new = [thing[0] for thing in reorder]
rank = [math.log(x) for x in range(1,len(word_freq)+1)]

document_info = dict.fromkeys(defm14as)

#total_freq = []
#total_rank = []

for document in defm14as:
    # Compute the word frequency for each document
    doc = MACdoc(document)
    word_freq = doc.WordFreq(docs_dict_new)
    freq = [word_freq[word] for word in docs_dict_new]
    freq = sorted([math.log(f) for f in freq if f is not 0],reverse=True)
    
    #total_freq += freq
    #total_rank += rank[:len(freq)]
    #fit,residues = linalg.lstsq(rank,freq)
    slope,intercept,r_value,p_value,std_err = stats.linregress(rank[:len(freq)],freq)
    #pyplot.plot(rank[:len(freq)],freq,'.k')
    #pyplot.xlabel("Word Rank (log)")
    #pyplot.ylabel("Word Frequency (log)")
    
    #pyplot.show()
    
    document_info[document] = {"Frequencies":freq,"Slope":slope,"Intercept":intercept,"R-squared":r_value**2,
                               "Standard Error":std_err}
    
    #raw_input("Press enter to continue...")

#pyplot.plot(total_rank,total_freq,'.g')
#pyplot.show()

for document in document_info:
    print "Document: ",document
    print "Slope: ",document_info[document]["Slope"]," Intercept: ",document_info[document]["Intercept"]
    print "R-squared: ",document_info[document]["R-squared"],"Standard Error: ",document_info[document]["Standard Error"]

#print document_info
#print slope
#print intercept
#print r_value**2

#doc_array = []
#
#for i in range(len(docs_dict_new)):
#    doc_array.append([str(document_info[document][i]) for document in defm14as])
#    
#comma = ","
#freq_table = open("freq_table_MACs.csv","w")
#freq_table.write("Word,"+comma.join(defm14as)+"\n")
#for i in range(len(doc_array)):
#    freq_table.write(docs_dict_new[i]+","+comma.join(doc_array[i])+"\n")
#    
#freq_table.close()
#
##plot(rank,freq,'k.-')
##show()
