import sys
import errno
import json
import os
import config as config
from lxml import html
import requests
import MySQLdb

try:
	page = requests.get(config.cseeYear2016['resultUrl'], allow_redirects = False)
	#tree contains the whole html

	tree = html.fromstring(page.content)
	htmlElem = html.document_fromstring(page.content)
	schools = tree.xpath('//table[@cellspacing="2"]//a/text()')
	schoolsUri = tree.xpath('//table[@cellspacing="2"]//a/@href')
	total = len(schools)

	#connect to db
	dbConnection =MySQLdb.connect(host='localhost',user='root',passwd='khadija',db='careertoolDB')
	dbCursor = dbConnection.cursor()

	#drop if table exists
	dropQuery = "DROP TABLE IF EXISTS " + config.cseeYear2016['name']
	try:
		dbCursor.execute(dropQuery)
		dbConnection.commit()
	except:
		print "Table does not exist"

	query = "CREATE TABLE " + config.cseeYear2016['name'] + " (SchoolCode CHAR(20) NOT NULL, SchoolName CHAR(50) NOT NULL, Region CHAR(30) NOT NULL, StudentNo CHAR(20) NOT NULL, Gender CHAR(5) NOT NULL, Division CHAR(5), Civics CHAR(5), History CHAR(5), English CHAR(5), Kiswahili CHAR(5), Geography CHAR(5), BibleKnowledge CHAR(5), BasicMathematics CHAR(5), AdditionalMathematics CHAR(5), Biology CHAR(5), Physics CHAR(5), Chemistry CHAR(5), BookKeeping CHAR(5), Commerce CHAR(5), AgriculturalSci CHAR(5), ElectricalDraugting CHAR(5), ElectricalInstallation CHAR(5), ElectricalEngnSci CHAR(5), ElimuYaDiniKiislam CHAR(5), FineArt CHAR(5), ArabicLanguage CHAR(5), ArchtecturualDraught CHAR(5), BrickworkMasonary CHAR(5), BuildingConstruction CHAR(5), CarpentryJoinery CHAR(5), EngineeringSci CHAR(5), FittingTurning CHAR(5), FoodNutrition CHAR(5), FrenchLanguage CHAR(5), ComputerStudies CHAR(5), Plumbing CHAR(5), Music CHAR(5), LiteratureEnglish CHAR(5), MechanicalDraughting CHAR(5), MotorVehicleMech CHAR(5), PaintingSignWriting CHAR(5), PhysicalEducation CHAR(5), RadioTvServing CHAR(5), Surveying CHAR(5), TextileDressMaking CHAR(5), TheatreArt CHAR(5), WeldingMetalFabrication CHAR(5), WorkshopTech CHAR(5))"
	
	try:
		dbCursor.execute(query)
		dbConnection.commit()
	except:
		dbConnection.callback()
		print "Unexpected error:", sys.exc_info()

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
			schoolResult = requests.get(config.cseeYear2016['schoolPath'] + school_uri, allow_redirects = False)
			schoolTree = html.fromstring(schoolResult.content)
			result = schoolTree.xpath('//table[@cellspacing="0"]')
			if len(result) > 1:
				region = (result[1].text_content().split('\n')[1]).strip();
			else:
				region = "Not Defined"

			resultTdElem = schoolTree.xpath('//table[@cellspacing="2"]//td')
			resultTdElemLength = len(resultTdElem)

			insertQuery = "INSERT INTO " + config.cseeYear2016['name'] + " (SchoolCode, SchoolName, Region, StudentNo, Gender, Division, Civics, History, English, Kiswahili, Geography, BibleKnowledge, BasicMathematics, AdditionalMathematics, Biology, Physics, Chemistry, BookKeeping, Commerce, AgriculturalSci, ElectricalDraugting, ElectricalInstallation, ElectricalEngnSci, ElimuYaDiniKiislam, FineArt, ArabicLanguage, ArchtecturualDraught, BrickworkMasonary, BuildingConstruction, CarpentryJoinery, EngineeringSci, FittingTurning, FoodNutrition, FrenchLanguage, ComputerStudies, Plumbing, Music, LiteratureEnglish, MechanicalDraughting, MotorVehicleMech, PaintingSignWriting, PhysicalEducation, RadioTvServing, Surveying, TextileDressMaking, TheatreArt, WeldingMetalFabrication, WorkshopTech) VALUES(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			
			valueArray = []

			if resultTdElemLength > 0:
				for x in range (5, resultTdElemLength, 5):
					student_no = resultTdElem[x].text_content().strip()
					gender = resultTdElem[x+1].text_content().strip()
					division = resultTdElem[x+3].text_content().strip()
					subjects = resultTdElem[x+4].text_content().strip()

					Civics = History = English = Kiswahili = Geography = BibleKnowledge = BasicMathematics = AdditionalMathematics = Biology = Physics = Chemistry = BookKeeping = Commerce = AgriculturalSci = ElectricalDraugting = ElectricalInstallation = ElectricalEngnSci = ElimuYaDiniKiislam = FineArt = ArabicLanguage = ArchtecturualDraught = BrickworkMasonary = BuildingConstruction = CarpentryJoinery = EngineeringSci = FittingTurning = FoodNutrition = FrenchLanguage = ComputerStudies = Plumbing = Music = LiteratureEnglish = MechanicalDraughting = MotorVehicleMech = PaintingSignWriting = PhysicalEducation = RadioTvServing = Surveying = TextileDressMaking = TheatreArt = WeldingMetalFabrication = WorkshopTech = "NULL"
					
					if "CIV - '" in subjects:
						index = subjects.find("CIV - '")
						Civics = subjects[index+7]
					if "GEO - '" in subjects:
						index = subjects.find("GEO - '")
						Geography = subjects[index+7] 
					if "B/MATH - '" in subjects:
						index = subjects.find("B/MATH - '")
						BasicMathematics = subjects[index+10]
					if "HIST - '" in subjects:
						index = subjects.find("HIST - '")
						History = subjects[index+8]
					if "ENGL - '" in subjects:
						index = subjects.find("ENGL - '")
						English = subjects[index+8]
					if "KISW - '" in subjects:
						index = subjects.find("KISW - '")
						Kiswahili = subjects[index+8]
					if "E/D/KIISLAMU - '" in subjects:
						index = subjects.find("E/D/KIISLAMU - '")
						ElimuYaDiniKiislam = subjects[index+16]
					if "B/KNOWL - '" in subjects:
						index = subjects.find("B/KNOWL - '")
						BibleKnowledge = subjects[index+11]
					if "PHY - '" in subjects:
						index = subjects.find("PHY - '")
						Physics = subjects[index+7]
					if "CHEM - '" in subjects:
						index = subjects.find("CHEM - '")
						Chemistry = subjects[index+8]
					if "ARABIC LANGUAGE - '" in subjects:
						index = subjects.find("ARABIC LANGUAGE - '")
						ArabicLanguage = subjects[index+19]
					if "BIO'" in subjects:
						index = subjects.find("BIO - '")
						Biology = subjects[index+7]
					if "COMP STUD - '" in subjects:
						index = subjects.find("COMP STUD - '")
						ComputerStudies = subjects[index+13]
					if "B/KEEPING - '" in subjects:
						index = subjects.find("B/KEEPING - '")
						BookKeeping = subjects[index+13]
					if "COMM - '" in subjects:
						index = subjects.find("COMM - '")
						Commerce = subjects[index+8]
					if "AGRI - '" in subjects:
						index = subjects.find("AGRI - '")
						AgriculturalSci = subjects[index+8]
					if "ADD MATH - '" in subjects:
						index = subjects.find("ADD MATH - '")
						AdditionalMathematics = subjects[index+12]
					if "ELECT DRAUGHT - '" in subjects:
						index = subjects.find("ELECT DRAUGHT - '")
						ElectricalDraugting = subjects[index+17]
					if "MECH DRAUGHT - '" in subjects:
						index = subjects.find("MECH DRAUGHT - '")
						MechanicalDraughting = subjects[index+16]
					if "W/SHOP TECH - '" in subjects:
						index = subjects.find("W/SHOP TECH - '")
						WorkshopTech = subjects[index+15]
					if "FITT & TURN - '" in subjects:
						index = subjects.find("FITT & TURN - '")
						FittingTurning = subjects[index+15]
					if "ELECT INST - '" in subjects:
						index = subjects.find("ELECT INST - '")
						ElectricalInstallation = subjects[index+14]
					if "RADIO & TV - '" in subjects:
						index = subjects.find("RADIO & TV - '")
						RadioTvServing = subjects[index+14]
					if "ELECT ENG SC - '" in subjects:
						index = subjects.find("ELECT ENG SC - '")
						ElectricalEngnSci = subjects[index+16]
					if "MOT VEH MECH - '" in subjects:
						index = subjects.find("MOT VEH MECH - '")
						MotorVehicleMech = subjects[index+16]
					if "BLD CONSTR - '" in subjects:
						index = subjects.find("BLD CONSTR - '")
						BuildingConstruction = subjects[index+14]
					if "ARCH DRAUGHT - '" in subjects:
						index = subjects.find("ARCH DRAUGHT - '")
						ArchtecturualDraught = subjects[index+16]
					if "WELD & MET - '" in subjects:
						index = subjects.find("WELD & MET - '")
						WeldingMetalFabrication = subjects[index+14]
					if "PLUMBING - '" in subjects:
						index = subjects.find("PLUMBING - '")
						Plumbing = subjects[index+12]
					if "BRI & MAS - '" in subjects:
						index = subjects.find("BRI & MAS - '")
						BrickworkMasonary = subjects[index+13]
					if "ENG SC - '" in subjects:
						index = subjects.find("ENG SC - '")
						EngineeringSci = subjects[index+10]
					if "CARP & JOIN - '" in subjects:
						index = subjects.find("CARP & JOIN - '")
						CarpentryJoinery = subjects[index+15]
					if "TEXTILE - '" in subjects:
						index = subjects.find("TEXTILE - '")
						TextileDressMaking = subjects[index+11]
					if "PAINT & SIGN - '" in subjects:
						index = subjects.find("PAINT & SIGN - '")
						PaintingSignWriting = subjects[index+16]
					if "PHY EDU - '" in subjects:
						index = subjects.find("PHY EDU - '")
						PhysicalEducatio = subjects[index+11]
					if "FREN - '" in subjects:
						index = subjects.find("FREN - '")
						FrenchLanguage = subjects[index+8]
					if "F.ART - '" in subjects:
						index = subjects.find("F.ART - '")
						FineArt = subjects[index+9]
					if "FOOD - '" in subjects:
						index = subjects.find("FOOD - '")
						FoodNutrition = subjects[index+8]
					if "LIT ENG - '" in subjects:
						index = subjects.find("LIT ENG - '")
						LiteratureEnglish = subjects[index+11]
					if "SURVEYING - '" in subjects:
						index = subjects.find("SURVEYING - '")
						Surveying = subjects[index+13]
					if "MUSIC - '" in subjects:
						index = subjects.find("MUSIC - '")
						Music = subjects[index+9]
					if "THEATRE ART - '" in subjects:
						index = subjects.find("THEATRE ART - '")
						TheatreArt = subjects[index+15]
					valueTuple = (school_code, school_name, region, student_no, gender, division,  Civics,  History ,  English , Kiswahili, Geography, BibleKnowledge, BasicMathematics, AdditionalMathematics, Biology, Physics, Chemistry, BookKeeping, Commerce, AgriculturalSci, ElectricalDraugting, ElectricalInstallation, ElectricalEngnSci, ElimuYaDiniKiislam, FineArt, ArabicLanguage, ArchtecturualDraught, BrickworkMasonary ,  BuildingConstruction , CarpentryJoinery, EngineeringSci, FittingTurning, FoodNutrition, FrenchLanguage, ComputerStudies,  Plumbing, Music, LiteratureEnglish, MechanicalDraughting, MotorVehicleMech, PaintingSignWriting, PhysicalEducation, RadioTvServing, Surveying, TextileDressMaking, TheatreArt, WeldingMetalFabrication, WorkshopTech)
					valueArray.append(valueTuple)
					
			dbCursor.executemany(insertQuery, valueArray)
			dbConnection.commit()
			print "Done Scrapping: School Name " + str(school_name)
            		print "------------------------------------------------------------------------"
	dbConnection.close()



except:
	print "Unexpected error:", sys.exc_info()
	print "Oops, something went wrong"


sys.exit()
