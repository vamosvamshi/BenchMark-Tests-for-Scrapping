import urllib.request
import bs4 as bs
import time
import datetime
import re
import multiprocessing
import glob
from tkinter import *
import os
import xlsxwriter
from pyexcel.cookbook import merge_all_to_a_book
import glob

'''
startdate = "06/12/2016"
enddate = "10/12/2017"
ticker = 'GE'
'''


def main():
    ''' These lines read data from the input text file which provide the inputs regarding the product and regular
    expressions were used to filter the product names from the input file'''
    file = open("E:/Graduate Project/finance data/input.txt")
    lines = file.readlines()
    file.close()
    # initialize the month date and year of the starting and ending date = 0
    y1 = 0
    m1 = 0
    d1 = 0
    y2 = 0
    m2 = 0
    d2 = 0

    for line in lines:
        # converts the whole line into lower and strips off the extra space at the ends
        line = line.lower().strip()
        if (re.findall(r'\w+tart', line)):
            start_date_match = re.findall(r'\d{2}/\d{2}/\d{4}', line)
            start = re.split('/|-|\|:', start_date_match[0])
        elif (re.findall(r'\w+nd', line)):
            end_date_match = re.findall(r'\d{2}/\d{2}/\d{4}', line)
            end = re.split('/|-|\|:', end_date_match[0])
        elif (re.findall(r'\w+icker', line)):
            ticker = re.split('/|-|\|:|=', line)

    # sets the end and start dates from the text file to the values that would be used in the string and convert them to a string
    m1 = str(start[0])
    d1 = str(start[1])
    y1 = str(start[2])

    m2 = str(end[0])
    d2 = str(end[1])
    y2 = str(end[2])
    # set the ticker value from the text file, strip and make everything into uppercase
    #ticker = ticker[1].upper().strip()
    ticker = "GE"

    startdate = str(m1 + "/" + d1 + "/" + y1)
    enddate = str(m2 + "/" + d2 + "/" + y2)

    # Timestamp value for startdate and enddate is the complete numerical representation of date, month and year
    # representation of date.
    timestamp_startdate = int(time.mktime(datetime.datetime.strptime(startdate, "%m/%d/%Y").timetuple()))
    timestamp_enddate = int(time.mktime(datetime.datetime.strptime(enddate, "%m/%d/%Y").timetuple()))
    timestamp_difference = int(timestamp_enddate) - int(timestamp_startdate)
    actual_end = (timestamp_enddate)
    actual_start = (timestamp_startdate)

    print("start time is ", int(timestamp_startdate))
    print("end time is ", int(timestamp_enddate))
    print("difference in timestamp is ", ((timestamp_enddate) - (timestamp_startdate)))

    # This is the value need to make it a shift by one day i.e. 24 hours in time stamp conversion.
    step = int(10540800)
    table_complete = []

    pool_input_list = []
    pool_input_tuple = ()
    j=0

    #The range starts from descending order from the last date to the date which comes by subtracting the one page
    # value of timestamp.
    for i in range(actual_start, actual_end, step):
        timestamp_startdate = timestamp_enddate - 10540800
        if (timestamp_startdate <= actual_start):
            timestamp_startdate = actual_start
        # Ticker name is company name in 2-4 letters is unique for every product, this needs to be changed to get value
        #  of each product.
        url_page = "https://finance.yahoo.com/quote/" + ticker + "/history?period1=" + str(
            timestamp_startdate) + "&period2=" + str(timestamp_enddate) + "&interval=1d&filter=history&frequency=1d"

        # Creates a list of URLs, one for each page. We can only do this if we get the total no. of pages in the previous
        #  step.
        pool_input_list.append([[j,url_page]])
        timestamp_enddate = timestamp_startdate - 86400
        j = j+1

    # All the pages are then appended into a list in the previous step and converted into a tuple.
    pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)

    # The multiprocessing process is initiated with a total number of processes as 4. The URLs and the URL numbers
    # are passed as a input.
    p = multiprocessing.Pool(processes=4)
    p.map(ParsingPage, pool_input_tuple)


    #This function is specific to excel sheets combining.
    merge_all_to_a_book(glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/*.xlsx"), "C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/Yahoo Data combined.xlsx")

    # All the files that were created per page are accessed and combined into a single Combined file.
    rd = glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/*.txt")
    with  open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/Yahoo Data combined.txt","wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    # The single file is opened and all the lines are read, this is done to display the output to the screen.
    file = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/Yahoo Data combined.csv")
    lines = file.readlines()
    print (lines)
    file.close()
    workbook = xlsxwriter.Workbook(
        'C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/"+str(ticker)+"/Yahoo Data combined.xlsx')
    worksheet = workbook.add_worksheet()
    workbook.close()

    # Output for Tkinter.
    # root = Tk()
    # root.title("Yahoo Extracted data")
    # s = Scrollbar(root)
    # s.pack(side=RIGHT, fill=Y)
    # t = Text(root, height=800, width=1600)
    # t.pack(side=LEFT, fill=Y)
    # s.config(command=t.yview)
    # t.pack(side=TOP)
    # t.insert(END, lines)
    # root.mainloop()


def ParsingPage(poolinput):
    # The last file name is obtained to get the name of the folder to be created using regular expressions.
    k = re.findall("[A-Z]+", poolinput[0][1])
    print("k is {}",k)
    table_complete=[]

    # Scraping process starts here
    for i in range(len(poolinput)):

        url = poolinput[i][1]
        print(poolinput[i][0])

        url1 = urllib.request.urlopen(url).read()

        soup = bs.BeautifulSoup(url1, 'html.parser')

        table = soup.find_all('tr')
        # append into table_complete the values after each iteration.
        table_complete.append(table)

    # If there exists a folder with this name, it replaces files in it, if not it creates a new folder and saves
    # the files in that folder.
    if not os.path.exists("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/" + k[0]):
        os.makedirs("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/" + k[0] + "/")
    workbook  = xlsxwriter.Workbook("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/" + str(k[0]) + "/" + str(
        poolinput[i][0]).strip() + ".xlsx")
    worksheet = workbook.add_worksheet()

    f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/yahoo/" + str(k[0]) + "/" + str(poolinput[i][0]).strip()+".txt","w+")
    print("process " + str(poolinput[i][0]) + " done")

    # initializing values to set the cell numbers
    i = 0
    j = 0
    # this is for printing the commments and writing the lines to the file.
    for x in table_complete:
        for y in x:
            f.write(y.text + "\n\n")
            for z in y:
                #f.write(y.text + "\n\n")
                worksheet.write(j, i, z.text)
                print(z.text, end=",,")
                #yield (str(z.text + "\n"))
                i = i + 1
            i = 0
            print("\n")
            j = j + 1
    workbook.close()


if __name__ == "__main__":
    main()

