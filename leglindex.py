'''
Created on Feb 21, 2011

@author: deokane
'''

import re,codecs

# A function to perform a "bag-of-words" comparison of our definition documents, with
# the frequency of each word in the documents

# Function to accumulate our bag-of-words
def bowcat(filelist):
    bag_of_words = []
    # Create a master list of all the words that occur in all of our documents. We must
    # go through all documents for the reason that a particular word may be unique to
    # a document and may be skipped otherwise.
    checker = lambda word: word not in bag_of_words
    for doc in filelist:
        haywain = codecs.open(doc,"r",'utf8',errors='replace').read()
        haywain = re.sub("[^a-zA-Z ]"," ",haywain)
        haywain = haywain.lower()
        haywain = haywain.split()
        bag_of_words.extend(list(set(filter(checker,haywain))))
    return list(set(bag_of_words))

# Function to count the instances of words in a document
def wordcount(file,word_dict):
    doc = codecs.open(file,"r",'utf8',errors='replace').read()
    doc = re.sub("[^a-zA-Z ]"," ",doc)
    doc = doc.lower()
    doc = doc.split()
    word_freq = dict.fromkeys(word_dict,0)
    for word in word_dict:
        word_freq[word] = doc.count(word)
    return word_freq

########################################################################################
# We also create functions to tally the various provisions
# Function to find business, operations, or financial conditions clause
def MBOF(macdef):

    print("Beginning automatic search for MAC on business, operations, financial condition, etc...")

    count = 0;

    biz = re.compile("business",re.I)
    ops = re.compile("operation",re.I)
    fin = re.compile("financial|financial(.*)condition",re.I)

    for linenum in range(1,len(macdef)-1):


        if (((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           or ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None)) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;


# Function to find ability to close deal clause **Consider reworking the operation of this function
def MSelAbil(macdef):

    print("Beginning automatic search for MAC on Seller's/Purchaser's ability to close the deal...")

    count = 0;

    biz = re.compile("seller|purchaser|buyer| deal|company",re.I);
    ops = re.compile("consummat| close",re.I);
    fin = re.compile("ability|prevent",re.I);

    for linenum in range(1,len(macdef)-1):


        if (((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           or ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None)) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

# Function that searches for MAC on losses over a threshold
#
def MExessLos(macdef):

    print("Beginning automatic search for MAC on losses over a certain threshold...")

    count = 0;

    biz = re.compile("loss",re.I);
    ops = re.compile("threshold|limit",re.I);
    fin = re.compile("over|exceed",re.I);

    for linenum in range(1,len(macdef)-1):


        if (((biz.match(macdef[linenum - 1]) or biz.match(macdef[linenum]) or biz.match(macdef[linenum + 1])) is not None) \
           or ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None)) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
# Mac on benefits contemplated

def MBenCont(macdef):

    print("Beginning automatic search for MAC on the benefits contemplated by the agreement...")

    count = 0;

    biz = re.compile("benefit",re.I);
    ops = re.compile("contemplat",re.I);
    fin = re.compile("agreement",re.I);


    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):


            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#

def MBuyBiz(macdef):

    print("Beginning automatic search for MAC on the ability of the buyer/target to continue to operate in substatially the same manner after merger...")

    count = 0;

    biz = re.compile("operat|business",re.I)
    ops = re.compile("continue",re.I)
    fin = re.compile("ability",re.I)


    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):


            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def MPrspects(macdef):

    print("Beginning automatic search for MAC on the prospects of the Company/Target...")

    count = 0;

    biz = re.compile("change|effect",re.I);
    ops = re.compile("reasonabl|prospect",re.I);
    fin = re.compile("expectation",re.I);


    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):


            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;
        
        
#
#
def MAssets(macdef):

    print("Beginning automatic search for MAC concerning purchased assets or securities...")

    count = 0;

    biz = re.compile("asset",re.I);
    ops = re.compile("change|effect",re.I)

    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1

#
#
def MEnfable(macdef):

    return 0


#
#


def MReasExp(macdef):

    print("Beginning automatic search for clause stating reasonable expectation of an event to have a material adverse effect/change...")

    count = 0;

    biz = re.compile("change|effect",re.I);
    ops = re.compile("reasonabl",re.I);
    fin = re.compile("expectation",re.I);


    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):


            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

    
#
#
def MNoDef(macdef):

    return 0

#
# Function that searches for disproportionate effects language
def MDispEffct(macdef):

    print("Beginning automatic search for disproportionate effects language...")

    count = 0;

    biz = re.compile("disproportionate",re.I);
    
    for linenum in range(1,len(macdef)-1):


        if (biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None :

            print("Found an instance of a MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1

#
#

def NoMAC(macdef):

    return 0

#
#
def EChEcon(macdef):

    print("Beginning automatic search for MAC relating to changes in the economy or business in general...")

    count = 0;

    biz = re.compile("business|economy|industry",re.I);
    ops = re.compile("change|effect|affect",re.I);


    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None):
           
            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;


#
#
def EChGen(macdef):

    print("Beginning automatic search for MAC relating to changes in general conditions of the specific industry...")

    count = 0;

    biz = re.compile("industry",re.I);
    ops = re.compile("company|subsidiar|business",re.I);
    fin = re.compile("affect|effect|change",re.I);

    for linenum in range(1,len(macdef)-1):


        if (((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           or ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None)) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
# Difference from N&P on Avaya Inc
def EChSecM(macdef):

    print("Beginning automatic search for MAC relating to changes in securities markets...")

    count = 0;

    biz = re.compile("(securities|financial)(.*)market",re.I)
    ops = re.compile("change|affect",re.I)

    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def EChPrVol(macdef):

    print("Beginning automatic search for MAC relating to changes in trading price or trading volume of Company's stock...")

    count = 0;

    biz = re.compile("price|market price|trading volume",re.I);
    ops = re.compile("decrease|change|decline",re.I);
    fin = re.compile("stock|securit",re.I);

    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def EChIntR(macdef):

    print("Beginning automatic search for MAC relating to changes in interest rates...")

    count = 0;

    biz = re.compile("credit|financial",re.I);
    ops = re.compile("change",re.I);
    fin = re.compile("market",re.I);
    int_rat = re.compile("interest(.*)rate",re.I);

    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None) \
           and ((int_rat.search(macdef[linenum - 1]) or int_rat.search(macdef[linenum]) or int_rat.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def EChExch(macdef):

    print("Beginning automatic search for MAC relating to changes in exchange rates...")

    count = 0

    biz = re.compile("change",re.I);
    ops = re.compile("exchange",re.I);
    int_rat = re.compile("rate",re.I);

    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           and ((int_rat.search(macdef[linenum - 1]) or int_rat.search(macdef[linenum]) or int_rat.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def EWar(macdef):

    print("Beginning automatic search for MAC relating to Acts of war or major hostilities...")

    count = 0

    biz = re.compile(" act",re.I)
    ops = re.compile(" war",re.I)
    fin = re.compile("hostilit",re.I)
    
    for linenum in range(1,len(macdef)-1):


        if (((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None))\
           or ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1

            break

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def ETerror(macdef):

    print("Beginning automatic search for MAC relating to Acts of Terrorism...")

    count = 0

    biz = re.compile("terrorism|sabotage",re.I);
    
    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1

            break

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def EGod(macdef):

    print("Beginning automatic search for MAC relating to Acts of God...")

    count = 0

    biz = re.compile(" act|force|natural",re.I);
    int_rat = re.compile("God|majeure|disaster");
    
    
    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
            and ((int_rat.search(macdef[linenum - 1]) or int_rat.search(macdef[linenum]) or int_rat.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#

# Mac on changing political conditions

def EPolCond(macdef):

    print("Beginning automatic search for MAC on changes in political conditions...")

    count = 0;

    biz = re.compile("change",re.I)
    ops = re.compile("political",re.I)
    fin = re.compile("condition",re.I)


    for linenum in range(1,len(macdef)):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum])) is not None) \
           and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum])) is not None) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum])) is not None):


            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def ENatCal(macdef):

    return 0
    
#
#
def EIntlCal(macdef):

    return 0
    
#
#
def EChLwReg(macdef):

    return 0
    
#
#
def EChIntrp(macdef):

    return 0
    
#
#
def EChBnkR(macdef):

    return 0
    
#
#
def EChTax(macdef):

    return 0
    
#
#
def EEeAtt(macdef):

    return 0
    
#
#
def ELayOffs(macdef):

    return 0
    
#
#
def EChLabor(macdef):

    return 0


#
# Not entirely sane search...unsure if this is a coding bug or Nixon Peabody problem (Andrew Corp)
def ERedCust(macdef):

    print("Beginning automatic search for MAC relating to reduction of customers or decline in business...")

    count = 0

    biz = re.compile("impact|reduction|decline|loss|adverse",re.I);
    ops = re.compile("relation(.*)customer|customer|client",re.I);
    
    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
            and ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None):
            
            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def ECustBR(macdef):

    return 0
    
#
#
def ERedRev(macdef):

    return 0
    
#
#
def EDelaySP(macdef):

    return 0
    
#
#
def EFctDscl(macdef):

    return 0


#
#
def EAnnTran(macdef):

    print("Beginning automatic search for MAC relating to effects of announcing the transaction...")

    count = 0

    ops = re.compile("negotiation|announcement|disclosure",re.I);
    fin = re.compile("agreement|transaction",re.I);


    for linenum in range(1,len(macdef)-1):


        if ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):


            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1;

            break;

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;


#
#
def EExpTran(macdef):

    return 0
    

#
#
def EChAction(macdef):

    print("Beginning automatic search for MAC relating to changes caused by the taking of any action required in connection with the agreement...")

    count = 0;

    ops = re.compile("execution|action|compliance with|consummation",re.I);
    fin = re.compile("agreement|transaction|terms",re.I);

    for linenum in range(1,len(macdef)-1):


        if ((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           and ((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1

            break

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1;

#
#
def EChGAAP(macdef):

    print("Beginning automatic search for MAC relating to changes caused by the taking of any action required in connection with the agreement...")

    count = 0

    biz = re.compile("change",re.I);
    ops = re.compile("GAAP",re.I);
    fin = re.compile("accounting",re.I);
    int_rat = re.compile("principles|practices",re.I);

    for linenum in range(1,len(macdef)-1):


        if ((biz.search(macdef[linenum - 1]) or biz.search(macdef[linenum]) or biz.search(macdef[linenum + 1])) is not None) \
           and (((ops.search(macdef[linenum - 1]) or ops.search(macdef[linenum]) or ops.search(macdef[linenum + 1])) is not None) \
           or (((fin.search(macdef[linenum - 1]) or fin.search(macdef[linenum]) or fin.search(macdef[linenum + 1])) is not None) \
           and ((int_rat.search(macdef[linenum - 1]) or int_rat.search(macdef[linenum]) or int_rat.search(macdef[linenum + 1])) is not None))):

            print("Found an instance of MAC")
            try:
                print(macdef[linenum - 1])
                print(macdef[linenum])
                print(macdef[linenum + 1])
            except UnicodeEncodeError:
                print(macdef[linenum])

            count += 1

            break

        linenum = linenum + 1;

    if count is 0:

        print("No instance of a MAC!")
        return 0

    elif count > 0:

        return 1

#
#
def ETrgFail(macdef):

    return 0
    
#
#
def EActTar(macdef):

    return 0
    
#
#
def ELitTran(macdef):

    return 0
