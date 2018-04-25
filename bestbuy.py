from bs4 import BeautifulSoup
import requests
import re
import multiprocessing
import time
from tkinter import *
import glob


t1 = time.time()
def main():
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
    url = "https://www.bestbuy.com/site/reviews/s/" + product_id
    # url = "https://www.bestbuy.com/site/reviews/s/"+str(product_id)+"?page=2&sort=MOST_HELPFUL"
    print(url)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    a = requests.get(url, headers=headers)

    soup = BeautifulSoup(a.content, "html.parser")

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
    for i in range(int(last_page) + 1):
        url_last_page = "https://www.bestbuy.com/site/reviews/s/" + str(product_id) + "?page=" + str(
            i) + "&sort=MOST_HELPFUL"
        pool_input_list.append([[i, url_last_page]])
    pool_input_tuple = tuple(pool_input_list)
    print(pool_input_tuple)

    p = multiprocessing.Pool(processes=4)
    p.map(ParsingPage, pool_input_tuple)
    print("total time taken in multiprocessing pool is " + str(time.time() - t1))
    rd = glob.glob("E:/Graduate Project/finance data/BestBuy Comments*.txt")
    with open("E:/Graduate Project/finance data/BestBuy Comments combined.txt", "wb") as outfile:
        for f in rd:
            with open(f, "rb") as infille:
                outfile.write(infille.read())

    file = open("E:/Graduate Project/finance data/BestBuy Comments combined.txt")
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
        f = open("E:/Graduate Project/finance data/BestBuy Comments" + str(pool_input1[i][0]).strip() + ".txt", "w+")
        #url1 = "https://www.bestbuy.com/site/reviews/s/" + str(product_id) + "?page=" + str(i) + "&sort=MOST_HELPFUL"
        a = requests.get(pool_input1[i][1], headers=headers)
        soup = BeautifulSoup(a.content, "html.parser")
        table2 = soup.find_all("p", {"class": "pre-white-space"})
        print("process " + str(pool_input1[i][0]) + " done")
        for item in table2:
            print(item.text)
            try:
                f.write(item.text + "\n\n")
            except:
                pass
    f.close()

if __name__ == "__main__":
    main()