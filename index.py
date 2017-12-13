import sys
import errno
import json
import os
import config as config
from lxml import html
import requests

try:

	page = requests.get(config.cseeYear2016['resultUrl'], allow_redirects = False)
	#tree contains the whole html
	tree = html.fromstring(page.content)
	htmlElem = html.document_fromstring(page.content)
	schools = tree.xpath('//table[@cellspacing="2"]//a/text()')
	schoolsUri = tree.xpath('//table[@cellspacing="2"]//a/@href')
	total = len(schools)

	for i in range (0, total):
		school = schools[i].strip()
		if not (school.startswith('P') or school.startswith('p')):
			school = school.split()
			school_code = school[0]
			del school[0]
			school_name = " ".join(school)

			csvFileName = school_code + ".csv"
			csv = open(csvFileName, "w") #create or open csv, "w" to write strings
			colNames = "GENDER, DIVISION\n" #column titles
			csv.write(colNames)
			school_uri = schoolsUri[i].replace("\\","/")

			#Get school specific html content
			schoolResult = requests.get(config.cseeYear2016['schoolPath'] + school_uri, allow_redirects = False)
			schoolTree = html.fromstring(schoolResult.content)

			resultTdElem = schoolTree.xpath('//table[@cellspacing="2"]//td')
			#resultTdElements = resultTdElem[0].text_content().split("\r\n\r\n")
			resultTdElemLength = len(resultTdElem)
			print resultTdElemLength
			print resultTdElem[6].text_content()
			#print resultTdElements[2].strip()
			#'''
			if resultTdElemLength > 0:
				for x in range (5, resultTdElemLength-5, 5):
					gender = resultTdElem[x+1].text_content().strip()
					division = resultTdElem[x+3].text_content().strip()
					print gender
					csv.write(gender +", "+ division + "\n")
			#'''


except Exception:
	print "Oops, something went wrong"


sys.exit()
