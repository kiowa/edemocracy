#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Alexander Brill on 2008-11-25.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import urllib2
import httplib
import time

from parsers import *

from models import *

class Main:
    page = ""
    cases = []
    BASE_URL = "http://web102881.pbe.oslo.kommune.no/saksinnsyn/postlist.asp"
    startDoc = 1
    hits = 0

    def main(self):
        sys.stdout.write("Scanning for cases: ")
        while (self.startDoc is not -1):
            sys.stdout.write(".")
            sys.stdout.flush()
            self.readPage()
            self.parseSearchResultPage()
            self.nextPage()
            time.sleep(1)
        
        sys.stdout.write("\nFetching data for %s cases: " % len(self.cases))    
        for case in self.cases:
            #sys.stdout.write(".")
            #sys.stdout.flush()
            self.readCasePage(case)
            self.parseCasePage(case)
            time.sleep(1)


    def parseCasePage(self, case):
        p = CaseParser()
        p.parse(self.page)
        c = Case()
        c.caseno = int(case)
        c.address = self.utf8(p.data["Adresse"])
        c.save()
        print c.caseno, c.address
        

    def utf8(self, str):
        return unicode(str, "iso-8859-1").encode("utf-8")

    def readCasePage(self, c):
        req = urllib2.Request("http://web102881.pbe.oslo.kommune.no/saksinnsyn/casedet.asp?mode=all&caseno=%s" % (c))
        req.add_header("Referer", "%s?dateparam=11/06/2008" % (self.BASE_URL))
        f = urllib2.urlopen(req)
        self.page = f.read()        
        f.close()
        
    
    def parseSearchResultPage(self):
        p = SearchResultParser()
        p.cases = []
        p.parse(self.page)
        self.hits = p.hits
        self.cases.extend(p.cases)
        del p
        
    def nextPage(self):
        if (self.hits > (self.startDoc+25)):
            self.startDoc += 25
        else:
            self.startDoc = -1
    
    def readPage(self):
        req = urllib2.Request("%s?startdoc=%s" % (self.BASE_URL, self.startDoc))
        req.add_header("Referer", "%s?dateparam=11/06/2008" % (self.BASE_URL))
        f = urllib2.urlopen(req)
        self.page = f.read()        
        f.close()
    

    
if __name__ == '__main__':
    Main().main()

    #m = Main()
    #m.readCasePage(200813360)
    #m.parseCasePage()
    
