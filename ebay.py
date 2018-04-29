from bs4 import BeautifulSoup
import requests
import os
import re
import time
import multiprocessing
global t1
global pool_input
import glob
from tkinter import *


def main():
    ''' These lines read data from the input text file which provide the inputs regarding the product and regular
    expressions were used to filter the product names from the input file'''
    t1 = time.time()
    file = open("E:/Graduate Project/finance data/input.txt")
    lines = file.readlines()
    file.close()
    item_no = []
    for line in lines:
        line = line.lower().strip()
        if (re.findall(r'\w+temnumber', line)):
            item_no = re.split('/|-|\|:|=', line)
    #
    '''item number of the product, different items have different items numbers in ebay'''
    '''change the ones that says itm =  "some number" to change the comments displayed'''
    item_number = item_no[-1].strip()
    # item_number = 272758290709

    # Item no is unique for every product, this needs to be changed to get value of each product.
    url1 = "https://www.ebay.com/urw/product-reviews/" + str(item_number) + "?_itm=1000047616"

    #Headers are in place to spoof the website that it is actually a browser that's accessing it, else it will block
    # the request if it's from an automated script.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    a = requests.get(url1, headers=headers)

    # Let's the BeautifulSoup know that the parsed content is of the type HTML.
    soup = BeautifulSoup(a.content, "html.parser")

    '''to find the page number of the last page, so as to make it possible to loop so many times'''
    page_number = []
    try:
        # ebay has its last page number in this class in this parameter as button, we need to get to that.
        table1 = soup.find_all("a", {"class": " spf-link"})
        for item in table1:
            page_number.append(item.text)
        '''last page it the second from the last'''
        print("last page number is " + page_number[-2])
        last_page = page_number[-2]
    except IndexError:
        last_page = 1

    pool_input_list = []
    pool_input_tuple = ()

    # Creates a list of URLs, one for each page. We can only do this if we get the total no. of pages in the previous
    #  step.
    for i in range(int(last_page) + 1):
        url_last_page = url1 + "&pgn=" + str(i).strip()
        # print("url for page %d is %s"%(i,url_last_page))
        pool_input_list.append([[i, url_last_page]])

    # All the pages are then appended into a list in the previous step and converted into a tuple.
    pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)

    '''
    pool_input1 = ([[0, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=0'],
                   [1, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=1']],
                 [[0, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=0'],
                  [1, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=1']])

    pool_input1 = ([[0, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=0']],
                    [[1, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=1']],
                   [[0, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=0']],
                    [[1, 'https://www.ebay.com/urw/product-reviews/110891711?_itm=1000047616&pgn=1']])'''

    # The multiprocessing process is initiated with a total number of processes as 4. The URLs and the URL numbers
    # are passed as a input.
    p = multiprocessing.Pool(processes=4)
    p.map(ParsingPage, pool_input_tuple)
    print("total time taken in multiprocessing pool is " + str(time.time() - t1))

    # All the files that were created per page are accessed and combined into a single Combined file.
    rd = glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+str(item_number)+"/*.txt")
    with open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+str(item_number)+"/Ebay Comments combined.txt","wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    # The single file is opened and all the lines are read, this is done to display the output to the screen.
    file = open("E:/Graduate Project/finance data/Ebay Comments combined.txt")
    lines = file.readlines()
    file.close()

    # Output for Tkinter.
    # root = Tk()
    # s = Scrollbar(root)
    # s.pack(side=RIGHT, fill=Y)
    # t = Text(root, height=800, width=1600)
    # t.pack(side=LEFT, fill=Y)
    # s.config(command=t.yview)
    # t.pack(side=TOP)
    # t.insert(END, lines)
    # root.mainloop()


def ParsingPage(pool_input1):
    # The last file name is obtained to get the name of the folder to be created, this is using regular expressions
    # filtering.
    k = re.findall("\d+",pool_input1[0][1])
    print(k)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    # Scraping process starts here
    for i in range(len(pool_input1)):

        # If there exists a folder with this name, it replaces files in it, if not it creates a new folder and saves
        # the files in that folder.
        if not os.path.exists("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+k[0]):
            os.makedirs("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+k[0]+"/")
        f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/"+k[0]+"/"+ str(pool_input1[i][0]).strip() + ".txt","w+")
        #f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/ebay/" + str(pool_input1[i][0]).strip() + ".txt",  "w+")
        print("url from ParsingPage "+pool_input1[i][1])
        a = requests.get(pool_input1[i][1], headers=headers)
        soup = BeautifulSoup(a.content, "html.parser")
        table2 = soup.find_all("p", {"itemprop": "reviewBody"})
        print("process " + str(pool_input1[i][0]) + " done")
        print(pool_input1[i][1])

        # this is for printing the commments and writing the lines to the file.
        for item in table2:
            print(item.text)
            try:
                f.write(item.text + "\n\n")
            except:
                pass
        f.close()

if __name__ == "__main__":
    main()

