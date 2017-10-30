import ebay
import bestbuy
import amazon
import google
import yahoo
import re

file = open("E:/Graduate Project/finance data/input.txt")
lines = file.readlines()
file.close()

option=[]
for line in lines:
    line = line.lower().strip()
    if (re.findall(r'\w+un',line)):
        option_no = re.split('/|-|\|:|=', line)

print(option_no[-1])

option = option_no[-1].strip()

print("option is \"%s\"" %option)

#ebay.main()


if option == "yahoo":
    yahoo.main()
elif option == "google":
    google.main()
elif option == "bestbuy":
    bestbuy.main()
elif option == "ebay":
    ebay.main()
elif option == "amazon":
    amazon.main()
