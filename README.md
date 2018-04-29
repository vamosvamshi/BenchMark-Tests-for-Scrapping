Process and steps followed in BenchMark Test for Scrapping:

1.	The following tests are the Bench Mark Tests to mine data product data from amazon, best buy, eBay, yahoo finance and google finance. 
2.	 The general process is that it has every product in these online e – commerce sites has a unique ID. We use this to parse data and scrape from each of the pages generated. There is a common methodology.
3.	For the finance data similar approach if followed I.e. the parameters are parsed from an input file and are used in the url. Then different pages are generated, and data is scraped.
4.	Many different libraries were used in testing like 
o	BeautifulSoup to filter and parse page content.
o	 OS commands to combine many text files into one, setting the no of processes, glob function etc., directories creation and to give permissions.
o	Multiprocessing to create multiple processes to make us of all processors and then combining the output, mapping functions.
o	Requests to spoof headers and get the html of the required page.
o	Re library to filter the content in the patterns that is required.
o	Time functions to calculate and measure performance.
o	Date time functions to calculate the timestamp outputs required in the html.
o	Xlsxwriter to write the data into excel sheets.
o	Pyexcel to perform operations on multiple excel sheets.
o	Tkinter to create GUI to display the output.
o	Math library to make page calculations.
5.	Then the data that is scrapped from different pages in written into individual files like .txt and .xlsx respectively. And the OS commands are used to combine all the individual files and create a single file (combined data for all single files) for that product or data requested.
6.	If there does not exist a folder already for the requested product, a new folder is created by that name and data is written into it. If there exists a folder already for the product, it updates the data and deletes the old files. 
