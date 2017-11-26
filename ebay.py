from bs4 import BeautifulSoup
import requests
import re
import time
import multiprocessing
global t1
global pool_input
import glob
from tkinter import *


def main():
    t1 = time.time()
    file = open("E:/Graduate Project/finance data/input.txt")
    lines = file.readlines()
    file.close()
    item_no = []
    for line in lines:
        line = line.lower().strip()
        if (re.findall(r'\w+temnumber', line)):
            item_no = re.split('/|-|\|:|=', line)

    '''item number of the product, different items have different items numbers in ebay'''
    '''change the ones that says itm =  "some number" to change the comments displayed'''
    item_number = item_no[-1].strip()

    url1 = "https://www.ebay.com/urw/product-reviews/" + str(item_number) + "?_itm=1000047616"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    a = requests.get(url1, headers=headers)
    soup = BeautifulSoup(a.content, "lxml")

    '''to find the page number of the last page, so as to make it possible to loop so many times'''
    page_number = []
    try:
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
    for i in range(int(last_page) + 1):
        url_last_page = url1 + "&pgn=" + str(i).strip()
        # print("url for page %d is %s"%(i,url_last_page))
        pool_input_list.append([[i, url_last_page]])
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

    p = multiprocessing.Pool(processes=4)
    p.map(ParsingPage, pool_input_tuple)
    print("total time taken in multiprocessing pool is " + str(time.time() - t1))
    rd = glob.glob("E:/Graduate Project/finance data/Ebay Comments*.txt")
    with open("E:/Graduate Project/finance data/Ebay Comments combined.txt", "wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    file = open("E:/Graduate Project/finance data/Ebay Comments combined.txt")
    lines = file.readlines()
    file.close()

    root = Tk()
    s = Scrollbar(root)
    s.pack(side=RIGHT, fill=Y)
    t = Text(root, height=800, width=1600)
    t.pack(side=LEFT, fill=Y)
    s.config(command=t.yview)
    t.pack(side=TOP)
    t.insert(END, lines)
    root.mainloop()


def ParsingPage(pool_input1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    for i in range(len(pool_input1)):
        f = open("E:/Graduate Project/finance data/Ebay Comments" + str(pool_input1[i][0]).strip() + ".txt", "w+")
        print("url from ParsingPage "+pool_input1[i][1])
        a = requests.get(pool_input1[i][1], headers=headers)
        soup = BeautifulSoup(a.content, "lxml")
        table2 = soup.find_all("p", {"itemprop": "reviewBody"})
        print(pool_input1[i][1])
        for item in table2:
            print(item.text)
            try:
                f.write(item.text + "\n\n")
            except:
                pass
        f.close()

if __name__ == "__main__":
    main()
