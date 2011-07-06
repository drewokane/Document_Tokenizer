'''

@author: deokane

'''

import urllib.request,json

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

# Open filing list
mergers = open("DEFM14A_filings-"+cyear+"-"+qrtr+".idx","rb")

names = []
ciks = []
dates = []


for line in mergers:
	

# Section to grab ticker data from Yahoo Finance
comp_name = "huntsman"
yahoo_finan = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={!s}&callback=YAHOO.Finance.SymbolSuggest.ssCallback".format(comp_name) 
web_page = urllib.request.urlopen(yahoo_finan)
lines = web_page.read()
lines = lines.decode()
lines = re.sub("YAHOO(.*)\(|\)","",lines)
decoder_ring = json.JSONDecoder()
comp_info = decoder_ring.decode(lines)
results = comp_info["ResultSet"]["Result"]
