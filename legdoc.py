'''
Created on Feb 21, 2011

@author: deokane
'''

import re,math,numpy,codecs
from operator import itemgetter

# An experimental approach is to construct a MAC document class, that contains all the text,
# word counts, and provision statistics as class methods that can be run at will on a given document.
def std(x):
    """Calculates the standard deviation of a sample data set x."""
    mean_sqrd = (math.fsum(x)/float(len(x)))**2
    scnd_raw_moment = math.fsum([i**2 for i in x])/float(len(x))
    std_dev = math.sqrt(scnd_raw_moment-mean_sqrd)
    return std_dev

def where(cond_func,arr):
    """This function returns the indices for which the condition is true.
    cond_func needs to be a function which returns a logical value.""" 
    indices = [i for i in range(len(arr)) if cond_func(arr[i])]
    return indices


def logit_regression(y,X,beta=None,MAX_ITER=200,THRESH=1e-4):
    """ """
    X,y = numpy.asarray(X,dtype=float),numpy.reshape(numpy.asarray(y,dtype=float),(len(y),1))
    assert X.shape(0) is y.shape(0),"Number of rows in array do not match number of observations!"
    N = X.shape(1)
    if beta is None:
        beta = numpy.zeros((N+1,1),dtype=float)
    X = numpy.hstack((numpy.ones((X.shape(0),1),dtype=float),X))
    i = 0
    while i < MAX_ITER:
        beta_old = beta
        p = 1/(1 + numpy.exp(-1*numpy.dot(X,beta)))
        q = 1/(1 + numpy.exp(numpy.dot(X,beta)))
        w = p*q
        X_tilda = w*X
        Xt = numpy.transpose(X)
        hessian = numpy.dot(Xt,X_tilda)
        gradient = numpy.dot(Xt,y-p)
        beta = beta_old + numpy.dot(numpy.linalg.inv(hessian),gradient)
        diff = sum(numpy.fabs(beta-beta_old))
        if diff <= THRESH:
            print("Beta coefficients converged before maximum iteration!")
            print("Convergence threshold met!")
            break
        i += 1
    print("Maximum number of iterations completed!")
    return beta,hessian




class MACdoc(object):
    '''A general class to hold both the text and relevant features of our MAC definition documents,
    such as the mean word frequency, variation coefficient of the mean word frequency, Yule's K, the
    ratio of words occurring only once in the vocabulary,'''
    
    def __init__(self,doc):
        self.doc = codecs.open(doc,"r",'utf8',errors='replace')
        self.document = self.doc.read()
        self.doclines = self.doc.readlines()
        
    def corpus_tokens(self):
        """A list of the words in the document."""
        document = self.document
        doc_clean = re.sub("[^a-zA-Z ]"," ",document)
        doc_low = doc_clean.lower()
        tokens = doc_low.split()
        #print("Number of tokens: " + str(len(tokens)))
        return tokens
    
    def corpus_types(self):
        """A list of the types (i.e. unique words) found in the document."""
        document = self.corpus_tokens()
        types = list(set(document))
        #print("Number of types: " + str(len(types)))
        return types
    
    def provisions(self,func_list):
        """A flexible method which accepts a user defined function which operates on the document
        and returns the desired value(s) to the user in the form of a dictionary keyed to the
        function name."""
        funcs_names = [f.__name__ for f in func_list]
        func_results = dict.fromkeys(funcs_names,0)
        document = self.doclines
        for f in func_list:
            func_results[f.__name__] = f(document)
        return func_results
    
    def wordfreq(self,word_dict,document_list=None,tf_idf=False):
        """A dictionary containing the word frequencies of the document, based on an outside dictionary"""
        doc = self.corpus_tokens()
        word_count = dict.fromkeys(word_dict,0)
        if (tf_idf is not False) and (document_list is not None):
            print("Calculating tf-idf frequencies for document...")
            N = float(len(doc))
            D = float(len(document_list))
            for word in word_dict:
                tf = float(doc.count(word))/N
                token_doc_count = sum([1 for docu in document_list if word in docu]) 
                idf = math.log(D/(token_doc_count+1))
                word_count[word] = tf*idf
        else:
            print("Performing raw word count...")
            for word in word_dict:
                word_count[word] = doc.count(word)
        return word_count
    
    def word_ranking(self):
        """A ordered list which contains the types (i.e. unique words) found in the document,
        sorted in order of highest frequency first."""
        doc = self.corpus_tokens()
        word_dict = self.corpus_types()
        word_count = dict.fromkeys(word_dict,0)
        for word in word_dict:
            word_count[word] = doc.count(word)
        reorder = sorted(word_count.iteritems(),key=itemgetter(1),reverse=True)
        docs_dict = [thing[0] for thing in reorder]
        return docs_dict
    
    def self_wordfreq(self):
        """A list containing the word frequencies based on the types local to the text, not an outside
        dictionary."""
        doc = self.corpus_tokens()
        word_dict = self.corpus_types()
        word_count = [doc.count(word) for word in word_dict]
        return word_count
    
    def self_ngramfreq(self,n):
        """A dictionary containing the frequencies of n word phrases, i.e. phrases with n words,
        local to the text, not an outside dictionary."""
        tokens = self.corpus_tokens()
        phrases = [" ".join(tokens[i:i+n]) for i in range(len(tokens)-(n-1))]
        phrase_set = self.corpus_ngrams(n)
        phrase_count = dict.fromkeys(phrase_set)
        for phrase in phrase_set:
            phrase_count[phrase] = phrases.count(phrase)
        return phrase_count
    
    def ngramfreq(self,n,phrase_dict):
        """A dictionary containing the frequencies of n word phrases, i.e. phrases with n words,
        local to the text, not an outside dictionary."""
        tokens = self.corpus_tokens()
        phrases = [" ".join(tokens[i:i+n]) for i in range(len(tokens)-(n-1))]
        phrase_count = [phrases.count(phrase) for phrase in phrase_dict]
        return phrase_count
    
    def corpus_ngrams(self,n):
        """A list containing all the n-word phrases in the corpus."""
        tokens = self.corpus_tokens()
        phrases = [" ".join(tokens[i:i+n]) for i in range(len(tokens)-(n-1))]
        phrase_set = list(set(phrases))
        return phrase_set
    
    def mean_wordfreq(self):
        """A global measure of the mean word frequency."""
        tokens = self.corpus_tokens()
        docdict = self.corpus_types()
        V = float(len(docdict))
        N = float(len(tokens))
        f_mu = N/V
        return f_mu
    
    def variation_cof(self):
        tokens = self.corpus_tokens()
        docdict = self.corpus_types()
        V = float(len(docdict))
        N = float(len(tokens))
        f_mu = N/V
        word_count = [tokens.count(word) for word in docdict]
        var_f_mu = numpy.std(word_count)/f_mu
        return var_f_mu
    
    def yules_k(self):
        freqs = self.self_wordfreq()
        freq_set = list(set(freqs))
        M1 = math.fsum([freqs.count(f)*f for f in freq_set])
        M2 = math.fsum([(f**2)*freqs.count(f) for f in freq_set])
        K = (10000)*(M2 - M1)/(M1**2)
        return K

    def singles_typeratio(self):
        freqs = self.self_wordfreq()
        ratio = freqs.count(1)/float(len(freqs))
        return ratio
    
    def singles_corpusratio(self):
        freqs = self.self_wordfreq()
        N = float(len(self.corpus_tokens()))
        ratio = freqs.count(1)/N
        return ratio
    
    def lowf_concentration(self):
        freqs = self.self_wordfreq()
        N = float(len(self.corpus_tokens()))
        lf_con = len(where(lambda x: x <= 5,freqs))/N
        return lf_con
    
    def medlowf_concentration(self):
        freqs = self.self_wordfreq()
        N = float(len(self.corpus_tokens()))
        mlf_con = len(where(lambda x: x <= 10,freqs))/N
        return mlf_con
    
    def max_relfreq(self):
        N = float(len(self.corpus_tokens()))
        freqs = self.self_wordfreq()
        p1 = max(freqs)/N
        return p1
    
    def mfw_concentration(self):
        freqs = sorted(self.self_wordfreq(),reverse=True)
        N = float(len(self.corpus_tokens()))
        mfw_con = math.fsum(freqs[0:9])/N
        return mfw_con
    
    def stereotype_index(self):
        doc = self.corpus_tokens()
        freqs = self.self_wordfreq()
        N = float(len(doc))
        V1 = freqs.count(1)
        V = float(len(self.corpus_types()))
        index_stereo = (N - V)/(V - V1)
        return index_stereo
    


def phrfind(words):
    '''This function provides a more abstract method of searching for provisions,
    by means of using a dictionary which contains the words of the phrase
    and their distances from the 'center of mass' of the phrase. The user
    inputs the dictionary as {"firstword":distance1,"secondword":distance2,etc....}.'''
# Unpack our group of words

    
# Another useful class to create is that of a collection of document classes.
class BagOfDocs(object):
    
    '''A class based on the MACdoc class that holds multiple instances of 
    the MACdoc class and performs some aggregate operations of interest, 
    e.g. principal component analysis, spreadsheet creation, etc.'''
    
    def __init__(self,file_list):
        self.documents = file_list
        self.names = [doc.split(".")[0] for doc in self.documents]
        self.types = []
        self.docinst = [MACdoc(doc) for doc in self.documents]
    
    def bowcat(self):
        bag_of_words = []
        '''Create a master list of all the words that occur in all of our documents. We must
        go through all documents for the reason that a particular word may be unique to
        a document and may be skipped otherwise.'''
        for doc in self.docinst:
            haywain = doc.corpus_tokens()
            bag_of_words.extend(list(set(haywain)))
        return list(set(bag_of_words))
    
    def aggregate_bag(self):
        ''' '''
        i = 0
        
        docs_dict_new = self.bowcat()
        
        col_names = ["Target","Mean_Word_Freq.","Var._Coef.","Yules_K",
                     "F1_Type_Freq.","F1_Corpus_Freq.","LFW_Concentration",
                     "MLFW_Concentration","Max._Rel._Freq.","MFW_Concentration",
                     "Stereotype_Index"] + \
                     ["_".join(word.split()) for word in docs_dict_new]
        col_names = [name + "_" for name in col_names]
                     
        word_table = numpy.zeros((len(self.names),len(col_names)-1),dtype=float)
                     
        for doc in self.docinst:
            print("Calculating word frequencey statistics & lexical parameters for "+doc+"...")
            doc_wfreq = doc.wordfreq(docs_dict_new)
            freqs = [str(doc_wfreq[key]) for key in docs_dict_new]
            target = self.names[i].split("_")
            lex_param_list = [target[0],doc.mean_wordfreq(),doc.variation_cof(),
                              doc.yules_k(),doc.singles_typeratio(),
                              doc.singles_corpusratio(),doc.lowf_concentration(),
                              doc.medlowf_concentration(),doc.max_relfreq(),
                              doc.mfw_concentration(),doc.stereotype_index()]
            lpl = [str(item) for item in lex_param_list]
            data = lpl + freqs
            words_csv.writerow(data)
            datanew = [float(item) for item in data[1:]]
            word_table[i,:] = datanew
            i += 1

        #kitchen_sink = numpy.hstack((word_table,booleans))

                         

    def booleans(self,functions):
        '''This method takes an input of a list of functions.'''

    def pca(self):
        '''This method performs a pca (principal component analysis)
        on the aggregate statistics.'''

        
        
    
        
        
        
