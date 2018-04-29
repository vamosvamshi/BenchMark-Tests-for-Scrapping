from bs4 import BeautifulSoup
import requests
import re
import multiprocessing
import time
from tkinter import *
import glob
import os


t1 = time.time()
def main():
    ''' These lines read data from the input text file which provide the inputs regarding the product and regular
    expressions were used to filter the product names from the input file'''
    file = open("E:/Graduate Project/finance data/input.txt")
    lines = file.readlines()
    file.close()

    product_no = []
    for line in lines:
        line = line.lower().strip()
        if (re.findall(r'\w+estbuy\s\w+roductid', line)):
            product_no = re.split('/|-|\|:|=', line)

    print(product_no[-1])

    product_id = product_no[-1].strip()
    # product id is unique for every product, this needs to be changed to get value of each product.
    url = "https://www.bestbuy.com/site/reviews/s/" + product_id
    # url = "https://www.bestbuy.com/site/reviews/s/"+str(product_id)+"?page=2&sort=MOST_HELPFUL"
    print(url)

    #Headers are in place to spoof the website that it is actually a browser that's accessing it, else it will block
    # the request if it's from an automated script.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    a = requests.get(url, headers=headers)

    # Let's the BeautifulSoup know that the parsed content is of the type HTML.
    soup = BeautifulSoup(a.content, "html.parser")

    # bestbuy has its last page number in this class in this parameter as button, we need to get to that.
    page_number = []
    table1 = soup.find_all("span",{"class":"message-text"})
    for item in table1:
        page_number.append(item.text)
        print(item.text)

    print("items in page_number are ",page_number[:])
    split_message = page_number[0].split(" ")
    print("the number of reviews are ",split_message[-2].replace(",",""))
    last_page = int(split_message[-2].replace(",",""))
    last_page=(last_page/20)+1
    print("last page is ",last_page)


    pool_input_list = []
    pool_input_tuple = ()

    # Creates a list of URLs, one for each page. We can only do this if we get the total no. of pages in the previous
    #  step.
    for i in range(int(last_page) + 1):
        url_last_page = "https://www.bestbuy.com/site/reviews/s/" + str(product_id) + "?page=" + str(
            i) + "&sort=MOST_HELPFUL"
        pool_input_list.append([[i, url_last_page]])

    # All the pages are then appended into a list in the previous step and converted into a tuple.
    pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)

    # The multiprocessing process is initiated with a total number of processes as 4. The URLs and the URL numbers
    # are passed as a input.
    p = multiprocessing.Pool(processes=4)
    p.map(ParsingPage, pool_input_tuple)

    # All the files that were created per page are accessed and combined into a single Combined file.
    print("total time taken in multiprocessing pool is " + str(time.time() - t1))
    rd = glob.glob("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+str(product_id)+"/*.txt")
    with open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+str(product_id)+"/BestBuy Comments combined.txt",
              "wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    # The single file is opened and all the lines are read, this is done to display the output to the screen.
    file = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+str(product_id)+"/BestBuy Comments combined.txt")
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
    k = re.findall("\d+", pool_input1[0][1])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    # Scraping process starts here
    for i in range(len(pool_input1)):

        # If there exists a folder with this name, it replaces files in it, if not it creates a new folder and saves
        # the files in that folder.
        if not os.path.exists("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+k[0]):
            os.makedirs("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+k[0]+"/")
        f = open("C:/Users/vamshi/Desktop/DATA_EXTRACTION/bestbuy/"+k[0]+"/"+ str(pool_input1[i][0]).strip() + ".txt",
                 "w+")
        #url1 = "https://www.bestbuy.com/site/reviews/s/" + str(product_id) + "?page=" + str(i) + "&sort=MOST_HELPFUL"
        a = requests.get(pool_input1[i][1], headers=headers)
        soup = BeautifulSoup(a.content, "html.parser")
        table2 = soup.find_all("p", {"class": "pre-white-space"})
        print("process " + str(pool_input1[i][0]) + " done")

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