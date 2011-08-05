'''
Created July 19, 2011

Author: D.E. O'Kane

License: GPLv3
'''

import os,re,numpy,csv,time,codecs,math
from operator import itemgetter
#####


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


def bowcat(filelist):
    ''' Create a master list of all the words that occur in all of our documents. We must
    go through all documents for the reason that a particular word may be unique to
    a document and may be skipped otherwise. '''
    bag_of_words = []
    checker = lambda word: word not in bag_of_words
    for doc in filelist:
        haywain = codecs.open(doc,"r",'utf8',errors='replace').read()
        haywain = re.sub("[^a-zA-Z ]"," ",haywain)
        haywain = haywain.lower()
        haywain = haywain.split()
        bag_of_words.extend(list(set(filter(checker,haywain))))
    return list(set(bag_of_words))

def wordcount(file,word_dict):
    '''Returns a list of word frequencies in file 
    based on a dictionary provided by word_dict.'''
    doc = codecs.open(file,"r",'utf8',errors='replace').read()
    doc = re.sub("[^a-zA-Z ]"," ",doc)
    doc = doc.lower()
    doc = doc.split()
    word_freq = dict.fromkeys(word_dict,0)
    for word in word_dict:
        word_freq[word] = doc.count(word)
    return word_freq



#####



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



#####




##### MACdoc class

class MACdoc(object):
    '''A general class to hold both the text and relevant features of our MAC definition documents,
    such as the mean word frequency, variation coefficient of the mean word frequency, Yules K, the
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
        """A flexible method that accepts a user defined function (or list of functions which 
        operates on the document and returns the desired value(s) to the user in the form of 
        a dictionary keyed to the function name."""
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




##### Doc Mole
class DocMole(object):
    '''DocMole is a general tool for inputing collections of documents and generating usable
    data from them.'''

    def __init__(self):
        self.status = True
        self.docs_dict = []
        self.provisions = []
        self.words_freq = []
        self.lexical_param = []
        self.boolean = []
        self.document_list = []
        self.mutual_dist = {}
        self.kitchen_sink = []
        self.functions = ['help','exit','chdir','doc_list','list','process','generate']

    def mole_start(self):
        '''Start the phrase search program.'''
        #Inner class dependent messages and functions
        print("DocMole\nAuthor:D.E. O'Kane\nLicense: GPLv3\nCopyright (c) 2011 D.E. O'Kane")
        print("For a list of available commands, type help at the prompt.")


        while self.status is True:
            prompt = input("DocMole :: ")          
            uinput = prompt.split()

            try:
                action = getattr(self,uinput[0])
                if len(uinput) > 1:
                    self.status = action(*uinput[1:])
                else:
                    self.status = action()
            except (AttributeError,IndexError):
                print("DocMole does not recognize that command!")
                action = getattr(self,'help')
                self.status = action()
            except TypeError:
                print(getattr(self,uinput[0]))
            

    def help(self):
        '''help -> A list of all available commands and the 
        included documentation.'''

        print("""DocMole v 1.0
        Help documentation
        Please read the available commands below
        For technical support, please email deokane@gmail.com""")

        for item in self.functions:
            print(getattr(self,item).__doc__)
        
        return True

    def exit(self):
        '''exit -> exit program'''

        print('''DocMole is now exiting...''')

        return False

    def list(self):
        '''list -> list the current directory's files
        Usage: list
        list - command'''

        files = os.listdir(os.getcwd())

        for item in files:
            print(item)

        return True

    def chdir(self,new_dir):
        '''chdir -> change working directory

        Usage: chdir directory
        chdir - command
        directory - the full directory path you wish to make your current working directory'''

        print("Changing to directory:",new_dir)

        try:
            os.chdir(new_dir)

        except OSError as errmsg:
            print("Directory does not exist or is mispelled!")
            print("Error message: {0}".format(errmsg))

        return True

    def doc_list(self):
        '''doc_list -> generate the list of documents to be used in analysis

        Usage: doc_list
        doc_list - command'''
        
        print("You are currently working in:",os.getcwd())
        uinput = input("Do you wish to change to a different directory (y or n)? ")
        
        if re.search('y',uinput,re.I) is not None:
            print("Use the chdir command to change directories...")
        
        elif re.search('n',uinput,re.I) is not None:
            files = os.listdir(os.getcwd())
            self.document_list = sorted([name for name in files if name.find(".txt") is not -1])

        else:
            print("Command not recognized! Please try again.")
        
        return True

    def process(self,provisions=[MBOF,MSelAbil,MExessLos,MPrspects,MAssets,MReasExp,MDispEffct,EChEcon,EChGen,
             EChSecM,EChPrVol,EChIntR,EChExch,EWar,ETerror,EGod,ERedCust,EAnnTran,EChAction,EChGAAP],tf_idf=False):
        '''process -> process the list of documents input by doc_list using the input functions

        Usage: process [provisions=[] tf_idf=False]
        process - command
        provisions - list of function names'''

        funcs_names = [f.__name__ for f in provisions]

        MAC_results = dict.fromkeys(funcs_names,0)

        self.docs_quant_info = dict.fromkeys(self.document_list,{})

        print("Automatic search for MAC clauses finished...\nBeginning concatenation/comparison processing...")

        docs_dict = bowcat(self.document_list)
    
        print("Creating ordered word frequencey dictionary using " + self.document_list[0])
        words = wordcount(self.document_list[0],docs_dict)
        word_pairs = words.items()
        reorder = sorted(word_pairs,key=lambda x: x[1],reverse=True)
        docs_dict_new = [str(thing[0]) for thing in reorder]
        self.docs_dict = docs_dict_new
        self.provisions = funcs_names
      

        self.word_freq = numpy.zeros((len(self.document_list),len(docs_dict_new)),dtype=float)
        self.boolean = numpy.zeros((len(self.document_list),len(funcs_names)+1),dtype=float)
        self.lexical_param = numpy.zeros((len(self.document_list),10),dtype=float)

        i = 0

        for defm14a in self.document_list:
            #Grab the name of the target & buyer then read the document, replacing any encoding errors
            csv_name = defm14a.split(".")
            target = csv_name[0].split("_")
            print("Opening " + target[0] + " & "+ target[-1] + "Document " + str(i+1) + " of " + str(len(self.document_list))  +" for processing...")
            macdef = codecs.open(defm14a, "r",'utf8',errors='replace').readlines()

            #Calculate the boolean searches for the provision functions
            for f in provisions:
                MAC_results[f.__name__] = f(macdef)

            inclusions = ["MBOF","MSelAbil","MExessLos","MPrspects","MAssets","MReasExp","MDispEffct"]
            M = sum([MAC_results[item] for item in inclusions])
            exclusions = ["EChEcon","EChGen","EChSecM","EChPrVol",
                          "EChIntR","EChExch","EWar","ETerror",
                          "EGod","ERedCust","EAnnTran","EChAction","EChGAAP"]
            E = sum([MAC_results[item] for item in exclusions])
            mac_score = float(M)/float(M + E + 1)

            results = [mac_score] + [float(MAC_results[f]) for f in funcs_names]
            self.boolean[i,:] = results

            doc = MACdoc(defm14a)
            print("Calculating word frequencey statistics & lexical parameters for " + defm14a)
            if tf_idf is True:
                doc_wfreq = doc.wordfreq(docs_dict_new,document_list=self.document_list,tf_idf=True)
            else:
                doc_wfreq = doc.wordfreq(docs_dict_new)

            freqs = [float(doc_wfreq[key]) for key in docs_dict_new]

            self.word_freq[i,:] = freqs

            lex_param_list = [doc.mean_wordfreq(),doc.variation_cof(),
                          doc.yules_k(),doc.singles_typeratio(),
                          doc.singles_corpusratio(),doc.lowf_concentration(),
                          doc.medlowf_concentration(),doc.max_relfreq(),
                          doc.mfw_concentration(),doc.stereotype_index()]

            self.lexical_param[i,:] = lex_param_list

            i += 1

        return True

    def generate(self,name):
        '''generate -> generate csv files with the provision codings, word frequencies, and
        buyer friendliness measure.

        Usage: generate name
        generate - command
        name - name of csv file to be written out (exclude .csv ending). name should be all one word, only alphanumeric characters
        tf_idf - an optional command flag which is set to False by default. recalculates frequency 
        counts in terms of token frequency inverse document frequency.'''

        print('Generating tables....')
        funcs_names = self.provisions
        docs_dict_new = self.docs_dict

        #CSV file for provision codings
        print('Opening',name+'.csv')
        MAC_csv = csv.writer(open(name + ".csv","w"),lineterminator='\n')
        col_names = ["Target","Buyer","Mean_Word_Freq.","Var._Coef.","Yules_K",
                        "F1_Type_Freq.","F1_Corpus_Freq.","LFW_Concentration",
                        "MLFW_Concentration","Max._Rel._Freq.","MFW_Concentration",
                        "Stereotype_Index"] + \
                        ['Friendliness'] + ["_".join(word.split()) for word in funcs_names] + \
                        ["_".join(word.split()) for word in docs_dict_new]

        MAC_csv.writerow(col_names)

        self.kitchen_sink = numpy.zeros((len(self.document_list),len(col_names)-2),dtype=float)

        i = 0

        print('Writing data to table...')

        for document in self.document_list:
            print('Writing data for',document,'...')
            csv_name = document.split(".")
            target = csv_name[0].split("_")
            results = self.boolean[i,:]
            results = [str(result) for result in results]
            
            freqs = self.word_freq[i,:]
            freqs = [str(freq) for freq in freqs]

            lpl = self.lexical_param[i,:]
            lpl = [str(item) for item in lpl]

            row = [target[0],target[-1]] + lpl + results + freqs

            MAC_csv.writerow(row) 

            i += 1


        return True
        


DocMole().mole_start()
