import bs4 as bs
import datetime
import urllib.request
import xlsxwriter
import time
#from tkinter import *
import math
import multiprocessing
#import tkinter
import re
import glob

def main():
    file = open("E:/Graduate Project/finance data/input.txt")
    lines = file.readlines()
    file.close()
    '''initialize the month date and year of the starting and ending date = 0'''
    y1 = 0
    m1 = 0
    d1 = 0
    y2 = 0
    m2 = 0
    d2 = 0
    start_string = []
    end_string = []
    ticker_string = []
    date_match = []
    for line in lines:
        '''converts the whole line into lower and strips off the extra space at the ends'''
        line = line.lower().strip()
        if (re.findall(r'\w+tart',line)):
            start_date_match = re.findall(r'\d{2}/\d{2}/\d{4}',line)
            start = re.split('/|-|\|:',start_date_match[0])
        elif (re.findall(r'\w+nd',line)):
            end_date_match = re.findall(r'\d{2}/\d{2}/\d{4}',line)
            end = re.split('/|-|\|:',end_date_match[0])
        elif (re.findall(r'\w+icker',line)):
                ticker = re.split('/|-|\|:|=',line)

    '''sets the end and start dates from the text file to the values that would be used in the string and convert them to a string'''
    d1 = str(start[0])
    m1 = str(start[1])
    y1 = str(start[2])
    start_date = ("{}/{}/{}".format(d1, m1, y1))
    print("start date is {}".format(start_date))

    d2 = str(end[0])
    m2 = str(end[1])
    y2 = str(end[2])
    end_date = ("{}/{}/{}".format(d2, m2, y2))
    print("end date is {}".format(end_date))
    '''set the ticker value from the text file'''
    ticker = ticker[1].upper().strip()

    start_timestamp = time.mktime(datetime.datetime.strptime(start_date, "%d/%m/%Y").timetuple())
    end_timestamp = time.mktime(datetime.datetime.strptime(end_date, "%d/%m/%Y").timetuple())

    days = (end_timestamp - start_timestamp) / 86400
    effective_days = days * (5 / 7)
    pages = effective_days / 200
    print("timestamp difference {} days is {} and effective days is {} pages is{}".format((
        end_timestamp - start_timestamp), days, effective_days, math.ceil(pages)))

    no_of_pages = math.ceil(pages)

    list_count = 0

    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    pool_input_list = []
    pool_input_tuple = ()
    for i in range(no_of_pages):
        url_page = "https://finance.google.com/finance/historical?q=NASDAQ:"+ticker+"&startdate="+month[int(
             m1)-1]+"+"+d1+"%2C+"+y1+"&enddate="+month[int(
                m2)-1]+"+"+d2+"%2C+"+y2+"&num=200&ei=HV3FWauPPIi_jAHlsozoAQ&start="+str(i*200)
        pool_input_list.append([[i, url_page]])
        pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)


    p = multiprocessing.Pool(processes=4)
    p.map(ParsingPage, pool_input_tuple)
        #print("total time taken in multiprocessing pool is " + str(time.time() - t1))
    rd = glob.glob("E:/Graduate Project/finance data/Google Data*.txt")
    with open("E:/Graduate Project/finance data/Google Data combined.txt", "wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())


def ParsingPage(poolinput):
    split_nn_list = []
    xlist = []
    for i in range(len(poolinput)):

        url1 = poolinput[i][1]
        a = urllib.request.urlopen(url1).read()
        soup = bs.BeautifulSoup(a, 'html.parser')

        table = soup.find_all('table', {'class': 'gf-table historical_price'})
        '''xList filters the data from the website and appends it in the form of a string'''
        for x in table:
            xlist.append(x.text)
        '''split_nn_list will hold the total array of data particular to each day, splitting on \n\n'''
    try:
        for l in xlist:
            split_nn_list.append(l.split('\n\n'))
    except:
        pass

    file = open("E:/Graduate Project/finance data/Google Data" + str(poolinput[i][0]).strip() + ".txt", "w+")
    print("page "+str(poolinput[i][0])+" done")
    for e in split_nn_list:
        for f in e:
            print(f.replace("\n", "\t"))
            try:
                file.write(f.replace("\n", "\t")+"\n")
            except:
                pass

    file.close()



if __name__ == "__main__":
    main()