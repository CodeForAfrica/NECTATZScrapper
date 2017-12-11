import sys
import json
import os
from os.path import join
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

	output_dir='output'
	os.makedir(output_dir)


	for i in range (0, total):

		school = schools[i].strip()
		if not (school.startswith('P') or school.startswith('p')):
			school = school.split()
			school_code = school[0]
			del school[0]
			school_name = " ".join(school)

			csvFileName = school_code + ".csv"
			csv = open(os.path.join(output_dir, csvFileName), "w") #create or open csv, "w" to write strings
			colNames = "GENDER, DIVISION\n" #column titles
			csv.write(colNames)
			print total
			school_uri = schoolsUri[i].replace("\\","/")

			#Get school specific html content
			schoolResult = requests.get(config.cseeYear2016['schoolPath'] + school_uri, allow_redirects = False)
			schoolTree = html.fromstring(schoolResult.content)

			resultTdElem = schoolTree.xpath('//table[@cellspacing="2"]//td')
			resultTdElemLength = len(resultTdElem)

			if resultTdElemLength > 0:
				for x in range (5, resultTdElemLength-5, 5):
					gender = resultTdElem[x+1]
					division = resultTdElem[x+3]
					csv.write(gender +", "+ division + "\n")


except Exception:
	print "Oops, something went wrong"


sys.exit()
