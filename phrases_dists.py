print("""Phrases_Dist v 0.1.1
Author: Drew E. O'Kane
License: GPL v 2.0
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
exstring = re.compile("exit\(\)",re.IGNORECASE)

def command_parser(string):
    command = re.compile("\w*.\(\)",re.I)
    if command.search(string) is not None:
        #This is where the list of commands goes, possibly a dictionary
        pass
    else:
        return None


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
         


##phrase = ['business','financ','operat']
##biz.search_words(phrase)
##
##
##for f in filelist:
##    biz.corpus(f)
##    biz.whereabouts()
##    print(biz.mutual_dist)
