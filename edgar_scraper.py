'''
Created on May 17, 2011

@author: deokane
'''

from ftplib import FTP
import datetime,time,re,os

# Logon to sec ftp
print("Opening anonymous ftp with EDGAR...")
edgar = FTP("ftp.sec.gov")
edgar.login()

# Get the current year and month
print("Retreaving current date...")
now = datetime.date.today()
cyear = str(now.year)
qrtr = "QTR"

# Since financial markets operate on a quarterly schedule, convert months
# to which quarter we are presently in
if now.month < 4:
    qrtr += "1"
elif (now.month < 7) and (now.month > 3):
    qrtr += "2"
elif (now.month < 10) and (now.month > 6):
    qrtr += "3"
elif (now.month > 9):
    qrtr += "4"

####


# Set the working directory to current year and quarter
current_dir = "/edgar/full-index/"+cyear+"/"+qrtr

print("Opening directory:",current_dir)

edgar.cwd(current_dir)

#edgar.dir()

# Save a file of the current quarter's filings by form
print("Retrieving list of current quarter\'s filings...")
t0 = time.clock()
edgar.retrbinary("RETR form.idx",open("cur_qrtly_filings-"+cyear+"-"+qrtr+".idx","wb").write)
dt = str(float(time.clock() - t0)/60)
print("Elapsed time to perform retrieval:",dt,"minutes")
forms_idx = open("cur_qrtly_filings-"+cyear+"-"+qrtr+".idx","r").readlines()

# Write out a file containing only the merger filings
merg_filings = open("DEFM14A_filings-"+cyear+"-"+qrtr+".idx","w")
paths = []
defm14 = re.compile("DEFM14A ")

# Also collect ftp paths for each merger so we can download them.
for line in forms_idx:
	if defm14.match(line) is not None:
		print(line)
		paths.append(line.split()[-1])
		merg_filings.write(line)

merg_filings.close()

os.chdir("C://Documents and Settings//!law-visitor//My Documents//MAC parser project//EDGAR//"+cyear+"//"+qrtr)

i = 1
for path in paths:
	filing_path = path.split("/")
	name = filing_path[-1]
	name = re.sub("-","",name)
	filing_path[-1] = name[:-4]
	folder = "/".join(filing_path)
	edgar.cwd("/"+folder+"/")
	files = [file for file in edgar.nlst() if file.endswith(".htm") and ("index" not in file)]
##	try:
##            name = files[-1]
##	    print("Downloading",name,"File",str(i),"of",str(len(paths)))
##	    edgar.retrbinary("RETR "+name,open(filing_path[-1]+".htm","wb").write)
##	    i += 1
##	except IndexError as IE:
##                print("HTML filing document does not exist for file",folder)
##                print(IE)
	if len(files) > 0:
		name = files[-1]
		print("Downloading",name,"File",str(i),"of",str(len(paths)))
		edgar.retrbinary("RETR "+name,open(filing_path[-1]+".htm","wb").write)
		i += 1
	else:
		print("HTML filing document does not exist for file",folder)

####

# End the session on EDGAR
edgar.close()
print("Finished updating merger files!")

# Execute the ticker scraping script

exec(open("securities_info_scrobbler.py","r").read())

