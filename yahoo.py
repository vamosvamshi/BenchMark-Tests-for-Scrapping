import os
import urllib.request
import requests
import bs4 as bs
import time
import datetime
import xlsxwriter
import re

'''
startdate = "06/12/2016"
enddate = "10/12/2017"
ticker = 'GE'
'''
file = open("E:/Graduate Project/finance data/input.txt")
lines = file.readlines()
file.close()
#initialize the month date and year of the starting and ending date = 0
y1 = 0
m1 = 0
d1 = 0
y2 = 0
m2 = 0
d2 = 0

for line in lines:
    #converts the whole line into lower and strips off the extra space at the ends
    line = line.lower().strip()
    if (re.findall(r'\w+tart',line)):
        start_date_match = re.findall(r'\d{2}/\d{2}/\d{4}',line)
        start = re.split('/|-|\|:',start_date_match[0])
    elif (re.findall(r'\w+nd',line)):
        end_date_match = re.findall(r'\d{2}/\d{2}/\d{4}',line)
        end = re.split('/|-|\|:',end_date_match[0])
    elif (re.findall(r'\w+icker',line)):
        ticker = re.split('/|-|\|:|=',line)

#sets the end and start dates from the text file to the values that would be used in the string and convert them to a string
m1 = str(start[0])
d1 = str(start[1])
y1 = str(start[2])

m2 = str(end[0])
d2 = str(end[1])
y2 = str(end[2])
#set the ticker value from the text file, strip and make everything into uppercase
ticker = ticker[1].upper().strip()

startdate = str(m1+"/"+d1+"/"+y1)
enddate = str(m2+"/"+d2+"/"+y2)

print (" start date is %s and type is %s " %(startdate,type(startdate)))
print ("end date is %s and type is %s "%(enddate,type(enddate)))
print("ticker is %s and type is %s" %(ticker,type(ticker)))

timestamp_startdate = int(time.mktime(datetime.datetime.strptime(startdate, "%m/%d/%Y").timetuple()))
timestamp_enddate = int(time.mktime(datetime.datetime.strptime(enddate, "%m/%d/%Y").timetuple()))
timestamp_difference = int(timestamp_enddate) - int(timestamp_startdate)
actual_end = (timestamp_enddate)
actual_start = (timestamp_startdate)

print("start time is ",int(timestamp_startdate))
print("end time is ",int(timestamp_enddate))
print("difference in timestamp is ",((timestamp_enddate)-(timestamp_startdate)))

step = int(10540800)
table_complete = []
for i in range (actual_start,actual_end,step):

    timestamp_startdate = timestamp_enddate - 10540800
    if (timestamp_startdate <= actual_start):
        timestamp_startdate = actual_start
    url_yahoo = "https://finance.yahoo.com/quote/"+ticker+"/history?period1="+str(
        timestamp_startdate)+"&period2="+str(timestamp_enddate)+"&interval=1d&filter=history&frequency=1d"
    print (url_yahoo)

    url1 =urllib.request.urlopen(url_yahoo).read()

    soup = bs.BeautifulSoup(url1,'html.parser')

    table = soup.find_all('tr')
    #append into table_complete the values after each iteration.
    table_complete.append(table)

    timestamp_enddate = timestamp_startdate - 86400

#opening the excel sheet to write the data into
workbook = xlsxwriter.Workbook('E:/Graduate Project/finance data/yahoo_data.xlsx')
worksheet = workbook.add_worksheet()
#initializing values to set the cell numbers
i=0
j=0

for x in table_complete:
    for y in x:
        for z in y:
            worksheet.write(j,i,z.text)
            print (z.text,end=",,")
            i=i+1
        i=0
        print("\n")
        j=j+1

workbook.close()




