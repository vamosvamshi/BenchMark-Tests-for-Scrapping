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

asin=[]
for line in lines:
    line = line.lower().strip()
    if (re.findall(r'\w+mazon',line)):
        asin = re.split('/|-|\|:|=', line)

print(asin[-1])


#unique for every product, this needs to be changed to get value of each product.
ASIN = asin[-1].strip()

url2 = "http://www.amazon.com/product-reviews/"+ASIN+"/ref" \
       "=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews"

print(url2)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
a = requests.get(url2, headers=headers)

soup = BeautifulSoup(a.content, "lxml")
table1 = soup.find_all("li",{"class":"page-button"})

page=[]
#this is for printing the page numbers
for item in table1:
    page.append(int(item.text))

print("the last page number is "+ str(page[-1]))
page_max = page[-1]
#table = soup.find_all("div","span", { "class":"a-row review-data","class":"a-size-base review-text",\

f = open("E:/Graduate Project/finance data/Amazon Comments.txt", "w+")
for i in range(1,page_max,1):

    url2 = "http://www.amazon.com/product-reviews/"+ASIN+"/ref" \
       "=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i)
    print(url2)
    a = requests.get(url2, headers=headers)
    soup = BeautifulSoup(a.content, "lxml")
    table2 = soup.find_all("span",{"class":"review-text"})

    #this is for printing the commments and writing the lines to the file.
    for item in table2:
        print(item.text+"\n")
        try:
            f.write(item.text+"\n\n")
        except:
            pass

f.close()

