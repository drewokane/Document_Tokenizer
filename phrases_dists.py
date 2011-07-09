print("""Phrases_Dist v 0.1.1
Author: Drew E. O'Kane
License: GPLv3
""")

import re,os,sys
sys.path += ['/home/deokane/Dropbox/Documents/Eclipse/MAC_parser/src']

#sys.path += ['C:\\Users\\deokane\\Dropbox\\Documents\\Eclipse\\MAC_parser\\src']
#os.chdir('C:\\Users\\deokane\\Dropbox\\Documents\\Eclipse\\MAC_parser\\src')
os.chdir('/home/deokane/Dropbox/Documents/Eclipse/MAC_parser/src')
from dist_meas import PhraseDist
biz = PhraseDist()


filelist = [f for f in os.listdir(os.getcwd()) if f.rfind('.txt') is not -1]

#Get user input for phrase

#Reserve certain commands for various tasks. Need to add functionality, e.g. 
#change working directory so there isn't a need to have the software in the
#same directory as the text files. Have commands end in () so as to distinguish
#from search terms. ToDo: Build a general function or class that applys the
#desired command.
exstring = re.compile("exit\(\)",re.I)


while 1:

    uinput = str(input("Enter search phrase terms or type exit() to close: "))
    
    if exstring.search(uinput) is not None:
    
        print("Thank you for using Phrases_Dist v 0.1.1")
        break

    else:
    
        phrase = uinput.split()

        biz.search_words(phrase)


        for f in filelist:
            biz.corpus(f)
            biz.whereabouts()
            print(biz.mutual_dist)
         

#############
class DjinnMaker(object):
    '''DjinnMaker is an atempt to create a general class which acts as an interactive prompt.
    It initializes a loop and populates a help list of functions it can perform. It also includes
    a method for exiting.'''

    def __init__(self):
        self.status = True
        self.words = []
        self.words_idx = {}
        self.document = []
        self.mutual_dist = {}
        self.functions = ['help','corpus','search_words','whereabouts','exit']

    def djinn_start(self):
        '''Start the phrase search program.'''
        #Inner class dependent messages and functions
        print("PhraseDjinn\nAuthor:D.E. O'Kane\nLicense: GPLv3\nCopyright (c) 2011 D.E. O'Kane")
        print("For a list of available commands, type help at the prompt.")


        while self.status is True:
            prompt = input("PhraseDjinn :: ")
            uinput = prompt.split()
            action = getattr(self,uinput[0])
            if len(uinput) > 1:
                self.status = action(uinput[1:])
            else:
                self.status = action()
            

    def help(self):
        '''help -> A list of all available commands and the 
        included documentation.'''

        for item in self.functions:
            print(getattr(self,item).__doc__)
        
        return True

    def corpus(self,text):
        '''corpus -> load a text document for searching
        
        Usage: corpus filepath
        corpus - command 
        filepapth - full path to file and name of file
        
        A method which opens a text file, coverts it to UTF-8
        encoding, and then cleans out non-word characters.'''

        print("Opening",text)
        doc = codecs.open(text,'r','utf8',errors='replace').read()
        doc_clean = re.sub("[^a-zA-Z ]"," ",doc)
        doc_low = doc_clean.lower()
        tokens = doc_low.split()
        self.document = tokens

        return True

    def search_words(self,search_terms):
        '''search_words -> word/words to be found in document

        Usage: search_words word1 word2 word3 ...
        search_words - command
        word1... - words that make up search phrase separated by whitespace
        
        A method which accepts a list of the words making 
        up the phrase you wish to find in the document provided 
        by the corpus() method.'''

        self.words = search_terms
        self.words_idx = dict.fromkeys(search_terms,[])
        self.mutual_dist = dict.fromkeys(search_terms,0)

        return True

    def whereabouts(self):
        '''whereabouts -> find closest groupings of words

        Usage: whereabouts
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

        return True

    def exit(self):
        '''exit -> exit program'''

        print('''PhraseDjinn is now exiting...''')

        return False
                            
