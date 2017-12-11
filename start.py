import sys
import config as config
from lxml import html
import requests
import json

try:
	#get the result pahe
	print "i am here"
	resultPage = requests.get(config.cseeYear2016['resultUrl'], allow_redirects = False)
	print "and here too"
	#tree contains the whole html
	tree = html.fromstring(resultPage.content)

	#dictionary for json File
	data = {}
	data['schools'] = []

	subjectNameLists = []

	schools = tree.xpath('//table[@cellspacing="2"]//a/text()')
	schoolsUri = tree.xpath('//table[@cellspacing="2"]//a/@href')
	total = len(schools)
	print total
	'''
	for i in range (0, total):
	
		school = schools[i].strip()
		if not (school.startswith('P') or school.startswith('p')):
			myschool = {}
			#Get school name and school code
			school = school.split()
			school_code = school[0]
			myschool["school_code"] = school_code
			del school[0]
			school_name = " ".join(school)
			myschool["school_name"] = school_name
			print school_name
			school_uri = schoolsUri[i].replace("\\","/")

			#Get school specific html content
			schoolResult = requests.get(config.cseeYear2016['schoolPath'] + school_uri)
			schoolTree = html.fromstring(schoolResult.content)
			
			csvFileName = school_code + ".csv"
			csv = open(csvFileName, "w") #create or open csv, "w" to write strings
			colNames = "GENDER, DIVISION\n" #column titles
			csv.write(colNames)
			
		
			schoolResult = schoolTree.xpath('//table[@cellspacing="2"]//td').text_content()
			schoolTdElem = len(schoolResult)
			print len(schoolTdElem)
			
			for z in range (0, shoolTdElem - 5, 5):
				gender = schoolResult[z+1].strip()
				division = schoolResult[z+3].strip()
				csv.write(gender + "," + name + "\n")
			
			result = schoolTree.xpath('//table[@cellspacing="0"]')
			
			if len(result) > 1:
				#Get region and overall gpa of the school
				region = result[1].text_content().split('\n')[1];
				gpa = result[1].text_content().split('\n')[3]
				myschool["region"] = region.strip()
				myschool["school_gpa"] = gpa.strip()
				myschool["subjects"] = []
		
				#check if school has subject wise information
				if len(result) > 5:
					#Get subject gpa and ranking
					mysummary = result[5].text_content().split('\r\n')
					summarytotal = len(mysummary)

					for x in range (11, (summarytotal - 11), 11):
						subject = {}
						subject["subject_code"] = mysummary[x].strip()
						subject["subject_name"] = mysummary[x+1].strip()
						subject["subject_gpa"] = mysummary[x+8].strip() 
						subject["subject_reg_rank"] = mysummary[x+9].strip()
						subject["subject_nat_rank"] = mysummary[x+10].strip()
				
						myschool["subjects"].append(subject)

			data['schools'].append(myschool)
	# Writing JSON data
	with open(config.cseeYear2016['name'] +"Result.json", 'w') as f:
		json.dump(data, f)
		'''

except Exception:
	print "Oppps!"


sys.exit()


			
			



	
	
