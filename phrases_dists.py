print("""Phrases_Dist v 0.1.1
Author: Drew E. O'Kane
License: GPLv3
""")

import re,os,sys

#sys.path += ['C:\\Users\\deokane\\Dropbox\\Documents\\Eclipse\\MAC_parser\\src']
sys.path += ['/home/deokane/Dropbox/Documents/Eclipse/MAC_parser/src']
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

        #Inner class dependent messages and functions
        print("PhraseDjinn\nAuthor:D.E. O'Kane\nLicense: GPLv3\nCopyright (c) 2011 D.E. O'Kane")
        print("For a list of available commands, type help at the prompt.")
        methods = dir(PhraseDist)

        ##General functions to display all the methods available to utilize
        builtinmethod = re.compile('__(\w*.)__',re.I)
        methods = [method for method in methods if builtinmethod.search(method) is None]

        while self.status is True:
            prompt = str(input("PhraseDjinn: "))
