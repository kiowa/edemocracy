#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Alexander Brill on 2008-11-25.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sgmllib
import re

class CaseParser(sgmllib.SGMLParser):
	data = {}
	tableNo = 0
	inDetailHeading = False
	inDetailCell = False
	inDetailB = False
	curKey = curValue = ""
	
	def parse(self, s):
		self.feed(s)
		self.close()
		
	def headerTable(self):
		if (self.tableNo == 1):
			return True
		return False
		
	def start_table(self, attributes):
		self.tableNo += 1
		
	def end_table(self):
		pass
		
	def start_tr(self, attributes):
		pass
		
	def end_tr(self):
		if (self.curKey != ""):
			self.data[self.curKey[:-1]] = self.curValue
		self.curKey = ""
		self.curValue = ""
		
		
	def start_td(self, attributes):
		if (self.headerTable()):
			for name, value in attributes:
				if name == "class":
					if value == "detailHeading":
						self.inDetailHeading = True
					if value == "detailCell":
						self.inDetailCell = True
	
	def end_td(self):
		if (self.headerTable()):
			self.inDetailHeading = False
			self.inDetailCell = False
		
	def start_b(self, attributes):
		if self.inDetailCell:			
			self.inDetailB = True

	def end_b(self):
		self.inDetailB = False
	
	def handle_data(self, data):
		if self.inDetailB:
			self.curValue = data.strip()
			
		elif self.inDetailHeading:
			self.curKey = data.strip()
			
		elif self.inDetailCell:
			self.curValue = self.curValue + data.strip()
			
	
			

class SearchResultParser(sgmllib.SGMLParser):
	cases = []
	hits = 0
	
	inSearchTable = False
	columnNo = 0
	inSearchResult = False
	inDocColumn = False
	inSakColumn = False
	inResultInfo = False
	inResultInfoAnchor = False
	

	def parse(self, s):
		self.feed(s)
		self.close()
		
	def start_table(self, attributes):
		for name, value in attributes:
			if (name == "class"):
				if (value == "searchtable"):
					self.inSearchTable = True
	
	def end_table(self):
		if self.inSearchTable:
			self.inSearchTable = False
	
	def start_tr(self, attributes):
		if self.inSearchTable:
			self.columnNo = 0
			
	def end_tr(self):
		pass
	
	def start_td(self, attributes):
		pass
	
	def end_td(self):
		if self.inSearchTable:
			self.columnNo +=1
			
	def start_a(self, attributes):
		if self.columnNo == 4:
			self.inSakColumn = True
			for name, value in attributes:
				if (name == "href"):
					self.cases.append(value.strip()[19:28])
		
		if (self.inResultInfo):
			for name, value in attributes:
				if (name == "href"):
					self.inResultInfoAnchor = True
			
	def end_a(self):
		if self.inDocColumn:
			self.inDocColumn = False
		if self.inSakColumn:
			self.inSakColumn = False
			
	def start_div(self, attributes):
		for name, value in attributes:
			if (name == "class"):
				if (value == "resultInfoDiv"):
					self.inResultInfo = True
					
	def end_div(self):
		if self.inResultInfo:
			self.inResultInfo = False
	
	def handle_data(self, data):
		if (data == "Sak"):
			self.inSakColumn = True
		if (data == "Dok"):
			self.inDocColumn = True
		if (self.inResultInfo):
			line = data.strip()
			c = re.compile("Viser dokument [0-9]+ til [0-9]+ av totalt ([0-9]+)")
			m = c.match(line)
			if (m):
				self.hits = int(m.group(1))
