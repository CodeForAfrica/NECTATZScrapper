import sys
import errno
import json
import os
import config as config
from lxml import html
import requests

try:
	page = requests.get(config.cseeYear2015['resultUrl'], allow_redirects = False)
	#tree contains the whole html
	
	tree = html.fromstring(page.content)
	htmlElem = html.document_fromstring(page.content)
	schools = tree.xpath('//table[@cellspacing="2"]//a/text()')
	schoolsUri = tree.xpath('//table[@cellspacing="2"]//a/@href')
	total = len(schools)
	
	#csv files gender performance
	csvFileName = config.cseeYear2015['name']+"GenderPerformance.csv"
	csv = open(csvFileName, "w")
	colName = "SCHOOL CODE, SCHOOL NAME, GENDER, GENDER TOTAL, DIV I, DIV II, DIV III, DIV IV, DIV 0, ABS/WITHHELD\n"
	csv.write(colName)

	for i in range (0, total):
		school = schools[i].strip()
		if not (school.startswith('P') or school.startswith('p')):
			school = school.split()
			school_code = school[0]
			del school[0]
			school_name = " ".join(school)
			print "------------------------------------------------------------------------"
			print "Scrapping School named " + str(school_name)

			#School Url
			school_uri = schoolsUri[i].replace("\\","/")
			#Get school specific html content
			schoolResult = requests.get(config.cseeYear2015['schoolPath'] + school_uri, allow_redirects = False)
			schoolTree = html.fromstring(schoolResult.content)
			resultTdElem = schoolTree.xpath('//table[@cellspacing="2"]//td')
			#resultTdElements = resultTdElem[0].text_content().split("\r\n\r\n")
			resultTdElemLength = len(resultTdElem)
			#'''
			totalCount = 0
			femaleCount = 0
			maleCount = 0
			div1Count = 0
			div2Count = 0
			div3Count = 0
			div4Count = 0
			div0Count = 0
			absFCount = 0
			absMCount = 0
			absCount = 0
			div1FCount = 0
			div2FCount = 0
			div3FCount = 0
			div4FCount = 0
			div0FCount = 0
			div1MCount = 0
			div2MCount = 0
			div3MCount = 0
			div4MCount = 0
			div0MCount = 0
			if resultTdElemLength > 0:
				for x in range (5, resultTdElemLength, 5):
					gender = resultTdElem[x+1].text_content().strip()
					totalCount += 1
					division = resultTdElem[x+3].text_content().strip()
					if gender == "F":
						femaleCount += 1
						if division == "I":
							div1FCount += 1
							div1Count += 1
						elif division == "II":
							div2FCount += 1
							div2Count += 1
						elif division == "III":
							div3FCount += 1
							div3Count += 1
						elif division == "IV":
							div4FCount += 1
							div4Count += 1
						elif division == "0":
							div0FCount += 1
							div0Count += 1
						else:
							absFCount +=1
							absCount += 1
					else:
						maleCount += 1
						if division == "I":
		                                        div1MCount += 1
							div1Count += 1
		                                elif division == "II":
		                                        div2MCount += 1
							div2Count += 1
		                                elif division == "III":
		                                        div3MCount += 1
							div3Count += 1
		                                elif division == "IV":
		                                        div4MCount += 1
							div4Count += 1
		                                elif division == "0":
		                                        div0MCount += 1
							div0Count += 1
						else:
							absMCount +=1
							absCount += 1
 
			csv.write(school_code +", "+ school_name + ", F, "+ str(femaleCount) +", " + str(div1FCount) +", " + str(div2FCount) +", "+ str(div3FCount) +", " + str(div4FCount) +", "+ str(div0FCount) + ", " + str(absFCount) + "\n")
			csv.write(school_code +", "+ school_name + ", M, "+ str(maleCount) +", " + str(div1MCount) +", " + str(div2MCount) +", "+ str(div3MCount) +", " + str(div4MCount) +", "+ str(div0MCount)+ ", " + str(absMCount) +"\n")
			csv.write(school_code +", "+ school_name + ", All, "+ str(totalCount) +", " + str(div1Count) +", " + str(div2Count) +", "+ str(div3Count) +", " + str(div4Count) +", "+ str(div0Count) + ", " + str(absCount) +"\n")
			print "Done Scrapping: School Name " + str(school_name)
                        print "------------------------------------------------------------------------"
			#'''


except:
	print "Unexpected error:", sys.exc_info()[0]
	print "Oops, something went wrong"


sys.exit()
