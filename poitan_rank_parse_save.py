# coding:utf-8
# get static data from www.poitan.net
# 2014/7/26(Sat) SHINODA Shiori

import sys
import urllib.request
from html.parser import HTMLParser

class myParser(HTMLParser):
        def __init__(self,date):
                HTMLParser.__init__(self)
                self.inSummaryTable = False
                self.inSpan = False
                self.trCount = 20
                self.date = date

        def handle_starttag(self, tag, attrs):
                if tag == "table":
                        for name, value in attrs:
                                if name == "summary" and u"統計情報" in value:
                                        self.inSummaryTable = True
                if self.inSummaryTable == True:
                        if tag == "span":
                                self.inSpan = True
                        if tag == "tr":
                                if self.trCount == 20:
                                        self.trCount = 0
                                else:
                                        self.trCount += 1
                                        print(date,end="\t")

        def handle_endtag(self, tag):
                if self.inSummaryTable == True:
                        if tag == "table":
                                self.inSummaryTable = False
                        if tag == "span":
                                self.inSpan = False
                        if tag == "tr":
                                if self.trCount != 20  or self.trCount != 0:
                                        print()

        def handle_data(self, data):
                if self.inSummaryTable == True:
                        if self.trCount != 0:
                                if self.inSpan == True:
                                        print(data,end="")
                                elif "(" in data:
                                        print(data,end="")
                                else:
                                        print(data,end="\t")


if __name__ == "__main__":

	for year in range(2007,2015):
	        for month in range(1,13):
                        date = str(year)+"年"+str(month)+"月"
                        print(date, file=sys.stderr)
                        url = "http://stats.poitan.net/exchange-" + str(year) + ("0"+str(month))[-2:] +".html"
                        byteshtmldata = urllib.request.urlopen(url)
                        strhtmldata = byteshtmldata.read().strip().decode('euc-jp')
                        parser = myParser(date)
                        
                        parser.feed(strhtmldata)

                        parser.close()
                        byteshtmldata.close()
