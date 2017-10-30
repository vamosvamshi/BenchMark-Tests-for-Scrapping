import bs4 as bs
import pickle
import requests
import urllib.request
import xlsxwriter
import re

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

    d2 = str(end[0])
    m2 = str(end[1])
    y2 = str(end[2])
    '''set the ticker value from the text file'''
    ticker = ticker[1].upper().strip()

    list_count = 0
    split_nn_list = []
    xList = []
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    for page_count in range(0,8100,200):

        url1 = "https://finance.google.com/finance/historical?q=NASDAQ:"+ticker+"&startdate="+month[int(
         m1)-1]+"+"+d1+"%2C+"+y1+"&enddate="+month[int(
            m2)-1]+"+"+d2+"%2C+"+y2+"&num=200&ei=HV3FWauPPIi_jAHlsozoAQ&start="+str(page_count)

        #url1 = "https://finance.google.com/finance/historical?q=NASDAQ:MSFT&startdate=Feb+06%2C+2015&enddate=Jan+12%2C
        # +2017&num=200&ei=HV3FWauPPIi_jAHlsozoAQ&start=1"
        print(url1)

        #print('a is',https://finance.google.com/finance/historical?q=NASDAQ:"+ticker.+"&startdate="+month[int(
        # m1)+1]+"+"+d1+"%2C+"+y1+"&enddate="+month[int(m2)+1]+"+"+d2+"%2C+"+y2+"&num=200&ei=HV3FWauPPIi_jAHlsozoAQ&start="+str(page_count))
        a = urllib.request.urlopen(url1).read()

        soup = bs.BeautifulSoup(a,'html.parser')

        table = soup.find_all('table',{'class':'gf-table historical_price'})
        '''xList filters the data from the website and appends it in the form of a string'''
        for x in table:
            xList.append(x.text)
        print("page "+str(page_count/200)+" done")
        '''split_nn_list will hold the total array of data particular to each day, splitting on \n\n'''
        try:
            split_nn_list.append(xList[int(page_count/200)].split('\n\n'))
        except:
            pass

    '''this is to print all whole list of values for all the pages info gathered'''
    #print('split_nn_list is \n',split_nn_list)

    workbook = xlsxwriter.Workbook('E:/Graduate Project/finance data/demo.xlsx')
    worksheet = workbook.add_worksheet()
    '''
    for a in ((split_nn_list)):
        for b in a:
            print(b.replace("\n","\t"))
        print('\n')
            #print(indiv_list[b].replace("\n","\t"))
    '''
    '''j = 1 for incrementing the counter for writing the data into rows of excel'''
    j=1
    for a in split_nn_list:
        for b in a:
            row_string = 'A' + str(j)
            '''indiv_list is the single row element consisting of all the data required to be put in the row'''
            indiv_list = b.split('\n')
            worksheet.write_row(row_string,indiv_list)
            j = j+1
        '''reinitializing the row_string to be zero after each iteration '''
        row_string = ''

    workbook.close()


if __name__ == "__main__":
    main()
