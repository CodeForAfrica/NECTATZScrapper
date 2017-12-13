import sys
import json
import config as config
from lxml import html
import requests


try:

	#get the result pahe
	resultPage = requests.get(config.acseeYear2017['resultUrl'], allow_redirects = False)

	#tree contains the whole html
	tree = html.fromstring(resultPage.content)


	#csv File
	csvFileName = config.acseeYear2017['name'] +"Result.csv"
	csv = open(csvFileName, "w")
	colNames = "SCHOOL CODE, SCHOOL NAME, REGION, GPA, SUBJECT_CODE, SUBJECT_NAME, SUBJECT_GPA, SUBJECT_REG_RANK, SUBJECT_NAT_RANK \n"
	csv.write(colNames)

	#a dictionary to dump in json -->uncomment below line (2 lines) for json output
	#data = {}
	#data["schools"] = []

	schools = tree.xpath('//table[@cellspacing="2"]//a/text()')
	schoolsUri = tree.xpath('//table[@cellspacing="2"]//a/@href')
	total = len(schools)


	for i in range (0, total):

		school = schools[i].strip()
		if not (school.startswith('P') or school.startswith('p')):
			#thisSchool = {}		-->a dictionary to populate school attributes /uncomment for json output
			#Get school name and school code
			school = school.split()
			school_code = school[0]
			del school[0]
			school_name = " ".join(school)

			#uncomment below lines to populate the dictionary
			#thisSchool["school_code"] = school_code
			#thisSchool["school_name"] = school_name

			school_uri = schoolsUri[i].replace("\\","/")

			#Get school specific html content
			schoolResult = requests.get(config.acseeYear2017['schoolPath'] + school_uri, allow_redirects = False)
			schoolTree = html.fromstring(schoolResult.content)

			result = schoolTree.xpath('//table[@cellspacing="0"]')
			if len(result) > 1:
				#region = schoolTree.xpath('//table[@cellspacing="0"]//td')[2].text_content()
				#gpa = schoolTree.xpath('//table[@cellspacing="0"]//td')[6].text_content()
				region = result[1].text_content().split('\n')[1];
				gpa = result[1].text_content().split('\n')[3]

				#uncomment below lines to populate the dictionary
				#thisSchool["region"] = region.strip()
				#thisSchool["gpa"] = gpa.strip()
				#thisSchool["subjects"] = []

				if len(result) > 5:
					subSummary = result[5].text_content().split('\n')
					sumLen = len(subSummary)

					for x in range(11, (sumLen-11), 11):
						#subject = {}
						subject_code = subSummary[x].strip()
						subject_name = subSummary[x+1].strip()
						subject_gpa = subSummary[x+8].strip()
						subject_reg_rank = subSummary[x+9].split("/")[0]
						subject_nat_rank = subSummary[x+10].split("/")[0]

						#subject["subject_code"] = subSummary[x].strip()
						#subject["subject_name"] = subSummary[x+1].strip()
						#subject["subject_gpa"] = subSummary[x+8].strip()
						#subject["subject_reg_rank"] = subSummary[x+9].split("/")[0]
						#subject["subject_nat_rank"] = subSummary[x+10].split("/")[0]
						##thisSchool["subjects"].append(subject)
						csv.write(school_code +", "+ school_name +", "+ region.strip() +", "+ gpa.strip() +", "+ subject_code +", "+ subject_name +", "+ subject_gpa +", "+ subject_reg_rank +","+ subject_nat_rank + "\n")

					print school_name
			#data["schools"].append(thisSchool)

except Exception:
	print "Oops, something went wrong"


sys.exit()
