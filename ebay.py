import bs4 as bs
from bs4 import BeautifulSoup
import pickle
import requests
import urllib
import xlsxwriter
import re
from time import sleep

file = open("E:/Graduate Project/finance data/input.txt")
lines = file.readlines()
file.close()

item_no=[]
for line in lines:
    line = line.lower().strip()
    if (re.findall(r'\w+bay',line)):
        item_no = re.split('/|-|\|:|=', line)

print(item_no[-1])

'''item number of the product, different items have different items numbers in ebay'''
#the end is stripped to make sure no space errors are put in place
item_number = item_no[-1].strip()


url1 ="https://www.ebay.com/urw/product-reviews/"+str(item_number)+"?_itm=1000047616"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
a = requests.get(url1, headers=headers)

soup = BeautifulSoup(a.content, "lxml")

'''to find the page number of the last page, so as to make it possible to loop so many times'''
page_number=[]
try:
    table1 = soup.find_all("a",{"class":" spf-link"})
    for item in table1:
        page_number.append(item.text)
        print(item.text)

    '''last page it the second from the last'''
    print ("last page number is "+page_number[-2])
    last_page = page_number[-2]
except IndexError:
    last_page=1

f = open("E:/Graduate Project/finance data/Ebay Comments.txt", "w+")
'''iterating the loop so many times'''
for i in range(1,int(last_page)+1,1):
    url2 = url1+"&pgn="+str(i).strip()
#url2 ="https://www.ebay.com/urw/product-reviews/2035465231?_itm="+str(item_number)+"&pgn=3"
#url = "https://www.ebay.com/urw/Andis-Slimline-Pro-Li-Cordless-Trimmer/product-reviews/2035465231?_itm=232136660719
# &pgn=3"
#url2="https://www.ebay.com/urw/Andis-Slimline-Pro-Li-Cordless-Trimmer/product-reviews/2035465231?_itm=232136660719
# &pgn=3"
    a = requests.get(url2, headers=headers)
    soup = BeautifulSoup(a.content, "lxml")
    table2 = soup.find_all("p",{"itemprop":"reviewBody"})
    print(url2)
    for item in table2:
        print(item.text)
        try:
            f.write(item.text+"\n\n")
        except:
            pass

f.close()
