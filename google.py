import requests

from bs4 import BeautifulSoup

#"""r = requests.get("https://www.w3schools.com/html/html_classes.asp"""

url = "https://www.yellowpages.com/search?search_terms=coffee&geo_location_terms=Macomb%2C+IL"

r = requests.get(url)

soup = BeautifulSoup(r.content,"html.parser")

links = soup.find_all("div","data-analytics")

#for link in links:
 #   print ("<a href = '%s'> %s </a>", ((link.get("href"), (link.get("text"))))

#g_data = soup.find_all("div",{"class":"info"})

for item in links:
    print (item)
    
    
