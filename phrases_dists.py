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

exstring = re.compile("exit",re.IGNORECASE)

while 1:

    uinput = str(input("Enter search phrase terms or type exit to close: "))
    
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
