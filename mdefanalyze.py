'''
Created on Feb 14, 2011

@author: deokane
'''
# macparser.py
# Coded by: D.E. O'Kane
# Description: This script loads a merger agreement file, and parses out the
# Definitions section so that word counts can be done.

__author__="deokane"
__date__ ="$Nov 3, 2010 10:30:00 AM$"
__license__="GPLv3"

# Import a needed utility that strips HTML markup from the document, making it
# human readable.

#from htmllaundry import StripMarkup
from legdoc import *
from leglindex import *
from operator import itemgetter
import re,os,csv,numpy,time


# This section is a work in progress, which at this moment only searches for a
# word or collection of words in each line of the definitions article. The user
# may either search for words or exit the program simply by typing exit.
def papersearch(macdef):

    uinput = str(input("Enter search term or type exit to close: "))
    uinput = uinput.replace(" ","|");
    exstring = re.compile("exit",re.IGNORECASE);
    search_string = re.compile(uinput,re.IGNORECASE);

    while exstring.match(uinput) is None:

        if uinput == 'exit':

            return;

        else:

            counter = 0;
            linenum = 1;

            for line in macdef:

                # This section will only print the line in which the word is
                # found, even if it is embeded in a word, i.e. a compound word,
                # and even if the search terms are not together.

                if search_string.search(line) is not None:

                    print("Line: "+str(linenum))
                    print(line)
                    counter = counter + 1;
                    
                linenum = linenum + 1;

            if counter == 0:

                print("Search term not found :(")

            else:

                print("Instances found: " + str(counter))

        uinput = str(input("Enter search terms or type exit to close: "))
        uinput = uinput.replace(" ","|");
        search_string = re.compile(uinput,re.IGNORECASE);
        # To cover the use of phrases and combinations of search terms, we split the
        # string into separate words, using the .replace() function, with the character 
        # to replace set to " ", and the replacing character to "|", so as to not split 
        # up the word into individual letters, and provide a useable search string to
        # the regular expressions search function.
#########################################################################################
# Collect all the MAC definition functions into one list which will then be used later.

MAC_funcs = [MBOF,MSelAbil,MExessLos,MPrspects,MAssets,MReasExp,MDispEffct,EChEcon,EChGen,
             EChSecM,EChPrVol,EChIntR,EChExch,EWar,ETerror,EGod,ERedCust,EAnnTran,EChAction,EChGAAP]


funcs_names = [f.__name__ for f in MAC_funcs]

MAC_results = dict.fromkeys(funcs_names,0)

#############################################################################
# Strip out the HTML markup for a cleaner document to search through. We also
# implement a function of our own writing to make undecoded html
# human readable.
#def htmldecode(string):
#
#        string1 = StripMarkup(string)
#        string2 = re.sub("[^a-zA-Z ]","",string1)
#        return string2

initial_startup = str(input("Do you wish to load a MAC definition or snip one from a raw merger document?\nType definition or rawmerger: "));
raw_string = re.compile("rawmerger",re.I);
define_string = re.compile("definition",re.I);


if raw_string.match(initial_startup) is not None:
    # The first task is to open the appropriate definitive proxy statement, in this
    # case the everlast document, but in general, whatever document we tell the
    # program to read. We then save the cleaned up file under a new name,
    # "MAC_blahblah.txt", which we construct from the old file name.

    defm14a = str(input("Input the file name you wish to open: "))
    mergaqlines = open(defm14a, "r").readlines()
    defm14a_name = defm14a.split("-")
    merg_name = "MERG_" + defm14a_name[2]
    mergefile = open(merg_name,"w")


    mergaqlist = []

    for line in mergaqlines:

        #line1 = StripMarkup(line);

        #line2 = htmldecode(line1);
        
        line2 = line

        mergefile.write(line2);

    mergefile.close()
    mergaqlist = open(merg_name,"r").readlines();

    # This section searches for the beginning of the actual merger agreement, and
    # then will go on to look for the beginning of the definitions section of the
    # proxy statement and finds the starting line number, to be used next to write
    # that section to a new file.

    appendix = re.compile("((Appendix|APPENDIX|Annex|ANNEX) A)");
    mergerag = re.compile("agreement and plan of merger",re.IGNORECASE);

    SOM = 1;

    appannex = 1;

    counter = 0;

    ##

    while 1:

        if (appannex >= len(mergaqlist)) and (counter is 0):

            print("Beginning of merger document not found!")
            break

        elif (appannex >= len(mergaqlist)) and (counter is not 0):

            usin = input("Input beginning line number of merger or exit close: ")

            exstring = re.compile("exit",re.IGNORECASE);

            if exstring.match(usin) is not None:

                break

            else:

                SOM = int(usin);

                break

        if (appendix.search(mergaqlist[appannex]) or mergerag.search(mergaqlist[appannex])) is not None:

            # Have the user input which line number is the beginning of the
            # merger document, based on all the instances found.

            print("Line number: " + str(appannex))
            print(mergaqlist[appannex])

            counter += 1;

        appannex += 1;

    ## Find the end of the merger and write the merger to a file

    appendix = re.compile("(Appendix|APPENDIX|Annex|ANNEX) B");

    EOM = len(mergaqlist);

    bppannex = SOM;

    counter = 0;

    while SOM is not 1:

        if (bppannex >= len(mergaqlist)) and (counter is 0):

            print("End of merger document not found!")
            break

        elif (bppannex >= len(mergaqlist)) and (counter is not 0):

            usin = input("Input ending line number of merger or type exit to close: ");

            if exstring.match(usin) is not None:

                break

            else:

                EOM = int(usin);

                break

        if (appendix.search(mergaqlist[bppannex]) is not None):

            # Have the user input which line number is the end of the
            # merger document, based on all the instances found.

            print("Line number: " + str(bppannex))
            print(mergaqlist[bppannex])

            counter += 1;

        bppannex += 1;

    ## Write out the merger to a file

    mergerfile = open(merg_name,"w");

    n = SOM;

    while n < EOM:

        mergerfile.write(mergaqlist[n]);

        n += 1;

    mergerfile.close()

    # Create the document that will hold the definition section of the merger.

    def_name = "DEF_" + defm14a_name[2];
    macdeffile = open(def_name,"w");

    mergaqlist = open(merg_name,"r").readlines();

    # Search for the definition section after the beginning of the merger document

    start = 1;

    def_string = re.compile("Definition|DEFINITION");
    def_string1 = re.compile("Material(.*)Adverse");

    counter = 0;

    found = 1;

    while 1:

        if (start >= len(mergaqlist)) and (counter is 0):

            print("Definition section not found!")
            found = 0
            break

        elif (start >= len(mergaqlist)) and (counter is not 0):

            usin = input("Input definition section line number or exit close: ")

            if exstring.match(usin) is not None:

                found = 0

                break

            else:

                start = int(usin);

                break

        if ((def_string.search(mergaqlist[start]) or (def_string1.search(mergaqlist[start]))) is not None):

            # Have the user input which line number is the beginning of the
            # definitions section, based on all the instances found.

            print(mergaqlist[start-1])
            print("Line number " + str(start) + ": " + mergaqlist[start])
            print(mergaqlist[start+1])

            counter += 1;

        start += 1;


    end_string = re.compile("\W");

    nstart = start;

    counter = 0

    ender = 1

    finish = len(mergaqlist);

    while 1 and (found is not 0):

        if (nstart - start) > 100:

            usin = input("Input definition section end line number or exit to close: ");

            if exstring.match(usin) is not None:

                break

            else:

                finish = int(usin);

                break;

            # Have the user input which line number is the end of the
            # definitions section, based on all the instances found.

        print("Line number " + str(nstart) + ": " + mergaqlist[nstart])

        nstart += 1;

    while (start <= finish) and (ender is not 0) and (found is not 0):

        macdeffile.write(mergaqlist[start])

        if start > finish:

            break

        start += 1;

    # Housekeeping. Close all the files, and subsequently open the definitions file
    # so as to save on memory.

    macdeffile.close();

    if found is not 0:

        macdef = open(def_name,"r").readlines();
        print("Opening definition section for search...")

    else:

        macdef = open(merg_name,"r").readlines();
        print("Opening merger agreement for search...")

    for f in MAC_funcs:

        MAC_results[f.func_name] = f(macdef)

    papersearch(macdef)

if define_string.match(initial_startup) is not None:

    files = os.listdir(os.getcwd())
    defm14as = [name for name in files if name.find(".txt") is not -1]

    # Generate a csv file to put in the Boolean search values so we can compare later

    MAC_csv = open("MACs_0708.csv","w")

    comma = ","
    commadash = "_,"

    MAC_csv.write("Target,Buyer," + comma.join(funcs_names) + "\n")
    
    booleans = numpy.zeros((len(defm14as),len(funcs_names)),dtype=int)
    friendliness_csv = csv.writer(open("mac_buyer_seller_adv.csv","w"),lineterminator="\n")
    friendliness_csv.writerow(["Target","BuyerFriendliness"])
    
    i = 0

    for defm14a in defm14as:

        csv_name = defm14a.split(".")
        target = csv_name[0].split("_")
        print("Opening " + target[0] + " & "+ target[-1] + "Document " + str(i+1) + " of " + str(len(defm14as))  +" for processing...")
        macdef = codecs.open(defm14a, "r",'utf8',errors='replace').readlines()

        for f in MAC_funcs:
            MAC_results[f.__name__] = f(macdef)

        results = [str(MAC_results[name]) for name in funcs_names]
        MAC_csv.write(target[0] + "," + target[-1] + "," + comma.join(results) + "\n")        
        results2 = [int(item) for item in results]        
        booleans[i,:] = results2
        i += 1

        inclusions = ["MBOF","MSelAbil","MExessLos","MPrspects","MAssets","MReasExp","MDispEffct"]
        M = sum([MAC_results[item] for item in inclusions])
        exclusions = ["EChEcon","EChGen","EChSecM","EChPrVol",
                      "EChIntR","EChExch","EWar","ETerror",
                      "EGod","ERedCust","EAnnTran","EChAction","EChGAAP"]
        E = sum([MAC_results[item] for item in exclusions])
        mac_score = float(M)/float(M + E + 1)
        friendliness_csv.writerow([target[0],mac_score])

    MAC_csv.close()
    
    print("Automatic search for MAC clauses finished...\nBeginning concatenation/comparison processing...")

    docs_dict = bowcat(defm14as)
    
    print("Creating ordered word frequencey dictionary using " + defm14as[0])
    words = wordcount(defm14as[0],docs_dict)
    word_pairs = words.items()
    reorder = sorted(word_pairs,key=lambda x: x[1],reverse=True)
    docs_dict_new = [str(thing[0]) for thing in reorder]
    
    words_csv = csv.writer(open("Word_stats_MACs_0708.csv","w"),lineterminator="\n")
    col_names = ["Target","Mean_Word_Freq.","Var._Coef.","Yules_K",
                        "F1_Type_Freq.","F1_Corpus_Freq.","LFW_Concentration",
                        "MLFW_Concentration","Max._Rel._Freq.","MFW_Concentration",
                        "Stereotype_Index"] + \
                        ["_".join(word.split()) for word in docs_dict_new]
    col_names = [name + "_" for name in col_names]
    words_csv.writerow(col_names)
    
    word_table = numpy.zeros((len(defm14as),len(col_names)-1),dtype=float)
    
    i = 0
    
    for defm14a in defm14as:
        doc = MACdoc(defm14a)
        #MAC_results = doc.provisions(MAC_funcs)
        #print(MAC_results)
        print("Calculating word frequencey statistics & lexical parameters for " + defm14a)
        
        doc_wfreq = doc.wordfreq(docs_dict_new)
        freqs = [str(doc_wfreq[key]) for key in docs_dict_new]
        csv_name = defm14a.split(".")
        target = csv_name[0].split("_")
        lex_param_list = [target[0],doc.mean_wordfreq(),doc.variation_cof(),
                          doc.yules_k(),doc.singles_typeratio(),
                          doc.singles_corpusratio(),doc.lowf_concentration(),
                          doc.medlowf_concentration(),doc.max_relfreq(),
                          doc.mfw_concentration(),doc.stereotype_index()]
        lpl = [str(item) for item in lex_param_list]
        #digram_list = [str(item) for item in doc.ngramfreq(2,digrams)]
        #trigram_list = [str(item) for item in doc.ngramfreq(3,trigrams)]
        data = lpl + freqs
        words_csv.writerow(data)
        datanew = [float(item) for item in data[1:]]
        word_table[i,:] = datanew
        i += 1
    
    kitchen_sink = numpy.hstack((word_table,booleans))
    
    for i in range(kitchen_sink.shape[1]):
        kitchen_sink[:,i] = kitchen_sink[:,i] - numpy.mean(kitchen_sink[:,i])
    
    print("Computing the principal components of the matrix...")
    t0 = time.clock()
    U,D,Vt = numpy.linalg.svd(kitchen_sink)
    dt = time.clock() - t0
    print("Elapsed time to compute singular value decomposition: ",dt)
    pc_matrix = csv.writer(open("principal_component_matrix.csv","w"),lineterminator="\n")
    
    Z = U*D
    
    
    for i in range(kitchen_sink.shape[0]):
        pc_matrix.writerow(Z[i,:])
        
    #for defm14a in defm14as:
    #    print("Calculating lexical parameters for " + defm14a)
        
    print("There are ",str(len(defm14as))," documents.")
    
    
