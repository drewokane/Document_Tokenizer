'''

@author: deokane

'''

import sys
sys.path += ['C:\\Users\\deokane\\Dropbox\\Documents\\Eclipse\\MAC_parser\\src']

import re,os,numpy,codecs


def where(cond_func,arr):
    '''This function returns the indices for which the condition is true.
    cond_func needs to be a function which returns a logical value.'''
    indices = [i for i in range(len(arr)) if cond_func(arr[i])]
    return indices

    
def zroes(length,value=0):
    '''Create a list initialized with a certain value, 
    e.g. 0 by default, of a prescribed length.'''
    arr = dict.fromkeys(range(length),value)
    neuarr = list(arr.values())
    return neuarr
#
class PhraseDist(object):
    '''A flexible class to find the minimum distances 
    between words of a phrase in a provided corpus.'''

    def __init__(self):
        self.words = []
        self.words_idx = {}
        self.document = []
        self.mutual_dist = {}

    def corpus(self,text):
        '''Usage: corpus filname
        corpus - command 
        filename - name of file
        
        A method which opens a text file, coverts it to UTF-8
        encoding, and then cleans out non-word characters.'''

        print("Opening",text)
        doc = codecs.open(text,'r','utf8',errors='replace').read()
        doc_clean = re.sub("[^a-zA-Z ]"," ",doc)
        doc_low = doc_clean.lower()
        tokens = doc_low.split()
        self.document = tokens

    def search_words(self,search_terms):
        '''Usage: search_words word1 word2 word3 ...
        search_words - command
        word1... - words that make up search phrase separated by whitespace
        
        A method which accepts a list of the words making 
        up the phrase you wish to find in the document provided 
        by the corpus() method.'''

        self.words = search_terms
        self.words_idx = dict.fromkeys(search_terms,[])
        self.mutual_dist = dict.fromkeys(search_terms,0)

    def whereabouts(self):
        '''Usage: whereabouts
        whereabouts - command
        
        This method performs a search for the words specified
        in the search_words method and finds the minimum distance 
        between the set of words, relative to the word with the 
        least number of indicies. The resulting distances are 
        placed in the self.mutual_dist dictionary and can be accessed 
        by a call to it.'''

        if len(self.words) == 0:
            print("No search terms found!\n\
            Please input phrase terms with PhraseDist.search_words method.")
        elif len(self.document) == 0:
            print("No corpus loaded!\n\
            Please load document for processing using the PhraseDist.corpus method.")
        else:
            print("Starting search for indicies...")
            for word in self.words:
                self.words_idx[word] = where(lambda x: re.search(word,x,flags=re.I),self.document)
            center = sorted(list(self.words_idx.values()),key=lambda y: len(y))[0]
            for key in self.words_idx.keys():
                d = zroes(len(center))
                for i in range(len(center)):
                    d[i] = abs(numpy.subtract(self.words_idx[key],center[i])).min()
                try:
                    self.mutual_dist[key] = min(d)
                    print("Indicies found\nFinding minimum distance between phrase words...")
                except ValueError:
                    print("Error:",key,"does not occur in corpus!")
                    print("Revise search phrase if possible...")
                    self.mutual_dist[key] = None
                            
                
        
    

