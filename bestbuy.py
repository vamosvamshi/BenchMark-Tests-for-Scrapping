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

product_no=[]
for line in lines:
    line = line.lower().strip()
    if (re.findall(r'\w+estbuy',line)):
        product_no = re.split('/|-|\|:|=', line)

print(product_no[-1])

product_id = product_no[-1].strip()

url = "https://www.bestbuy.com/site/reviews/s/"+str(product_id)+"?page=2&sort=MOST_HELPFUL"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
a = requests.get(url, headers=headers)

soup = BeautifulSoup(a.content, "lxml")

page_number=[]
table1 = soup.find_all("span",{"class":"message-text "})
for item in table1:
    page_number.append(item.text)
    print(item.text)


print("items in page_number are ",page_number)
split_message = page_number[0].split(" ")
print("the number of reviews are ",split_message[-3])
last_page=(int(split_message[-3]))
last_page=(last_page/20)+1
print("last page is ",last_page)

f = open("E:/Graduate Project/finance data/BestBuy Comments.txt", "w+")

for i in range(1,int(last_page),1):
    url1="https://www.bestbuy.com/site/reviews/s/"+str(product_id)+"?page="+str(i)+"&sort=MOST_HELPFUL"
    a = requests.get(url1, headers=headers)
    soup = BeautifulSoup(a.content, "lxml")
    table2 = soup.find_all("p",{"class":"pre-white-space"})
    print(url1)
    for item in table2:
        print(item.text)
        try:
            f.write(item.text+"\n\n")
        except:
            pass

f.close()

