from bs4 import BeautifulSoup
import requests
import re
from time import sleep
import multiprocessing
import glob
from tkinter import *
import os

def main():
    file = open("E:/Graduate Project/finance data/input.txt")
    lines = file.readlines()
    file.close()

    asin = []
    for line in lines:
        line = line.strip()
        if (re.findall(r'\w{6}\s+\w{4}', line)):
            asin = re.split('/|-|\|:|=', line)
            print(asin)

    ASIN = 'B01LYHL9YY'
    print(asin[:])

    # unique for every product, this needs to be changed to get value of each product.
    #ASIN = asin[-1].strip()

    url2 = "http://www.amazon.com/product-reviews/" + ASIN + "/ref" \
                                                             "=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews"

    print(url2)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    a = requests.get(url2, headers=headers)

    #soup = BeautifulSoup(a.content, "lxml")
    soup = BeautifulSoup(a.content, "html.parser")
    table1 = soup.find_all("li", {"class": "page-button"})

    print("hi")
    page = []
    # this is for printing the page numbers
    for item in table1:
        page.append(int(item.text))
    #print("page is "+page)
    #print("the last page number is " + str(page[-1]))
    print(page)
    page_max = page[-1]
    # table = soup.find_all("div","span", { "class":"a-row review-data","class":"a-size-base review-text",\

    pool_input_list=[]
    pool_input_tuple=()
    for i in range(page_max):
        url2 = "http://www.amazon.com/product-reviews/" + ASIN + "/ref" \
                "=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=" + str(i)
        pool_input_list.append([[i, url2]])
    pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)

    p = multiprocessing.Pool(processes=4)
    p.map(ParsingPage, pool_input_tuple)

    rd = glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/"+str(ASIN)+"/*.txt")
    with open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/"+str(ASIN)+"/Amazon Comments combined.txt", "wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    file = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/"+str(ASIN)+"/Amazon Comments combined.txt")
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

def ParsingPage(pool_input):
    k = re.findall("[A-Z0-9]+", pool_input[0][1])
    print("k is ")
    print (k)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    for i in range(len(pool_input)):
        #f = open("E:/Graduate Project/finance data/Amazon Comments.txt" + str(pool_input[i][0]).strip() + ".txt", "w+")
        if not os.path.exists("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/" + k[0]):
            os.makedirs("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/" + k[0] + "/")
        f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/amazon/"+str(k[0])+"/" + str(pool_input[i][0]).strip()+".txt","w+")
        print(pool_input[i][1])
        url=pool_input[i][1]
        a = requests.get(url, headers=headers)
        #soup = BeautifulSoup(a.content, "lxml")
        soup = BeautifulSoup(a.content, "html.parser")
        table2 = soup.find_all("span", {"class": "review-text"})
        print("process " + str(pool_input[i][0]) + " done")
        # this is for printing the commments and writing the lines to the file.
        for item in table2:
            print(item.text + "\n")
            try:
                f.write(item.text + "\n\n")
            except:
                pass

    f.close()


if __name__ == "__main__":
     main()
