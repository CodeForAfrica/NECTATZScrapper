import sys
import errno
import json
import os
import config as config
from lxml import html
import requests
import MySQLdb

try:
	page = requests.get(config.cseeYear2015['resultUrl'], allow_redirects = False)
	#tree contains the whole html

	tree = html.fromstring(page.content)
	htmlElem = html.document_fromstring(page.content)
	schools = tree.xpath('//table[@cellspacing="2"]//a/text()')
	schoolsUri = tree.xpath('//table[@cellspacing="2"]//a/@href')
	total = len(schools)

	#connect to db
	dbConnection =MySQLdb.connect(host='localhost',user='root',passwd='khadija',db='careertoolDB')
	dbCursor = dbConnection.cursor();
	query = "CREATE TABLE " + config.cseeYear2016 + " (SchoolCode VARCHAR(20) NOT NULL, SchoolName VARCHAR(50) NOT NULL, Region VARCHAR(30) NOT NULL, StudentNo VARCHAR(20) NOT NULL, Gender CHAR(1) NOT NULL, Division VARCHAR(5), Civics CHAR(1), History CHAR(1), English CHAR(1), Kiswahili CHAR(1), Geography CHAR(1), BibleKnowledge CHAR(1), BasicMathematics CHAR(1), AdditionalMathematics CHAR(1), Biology CHAR(1), Physics CHAR(1), Chemistry CHAR(1), BookKeeping CHAR(1), Commerce CHAR(1), AgriculturalSci CHAR(1), ElectricalDraugting CHAR(1), ElectricalInstallation CHAR(1), ElectricalEngnSci CHAR(1), ElimuYaDiniKiislam CHAR(1), FineArt CHAR(1), ArabicLanguage CHAR(1), ArchtecturualDraught CHAR(1), BrickworkMasonary CHAR(1), BuildingConstruction CHAR(1), CarpentryJoinery CHAR(1), EngineeringSci CHAR(1), FittingTurning CHAR(1), FoodNutrition CHAR(1), FrenchLanguage CHAR(1), ComputerStudies CHAR(1), Plumbing CHAR(1), Music CHAR(1), LiteratureEnglish CHAR(1), MechanicalDraughting CHAR(1), MotorVehicleMech CHAR(1), PaintingSignWriting CHAR(1), PhysicalEducation CHAR(1), RadioTvServing CHAR(1), Surveying CHAR(1), TextileDressMaking CHAR(1), TheatreArt CHAR(1), WeldingMetalFabrication CHAR(1), WorkshopTech CHAR(1))"
	
	try:
		dbCursor.execute(query)
		dbCursor.commit()
	except:
		dbCursor.callback()


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
			
			result = schoolTree.xpath('//table[@cellspacing="0"]')
			if len(result) > 1:
				region = result[1].text_content().split('\n')[1];
			else:
				region = "Not Defined"

			resultTdElem = schoolTree.xpath('//table[@cellspacing="2"]//td')
			resultTdElemLength = len(resultTdElem)

			insertQuery = "INSERT INTO " + config.cseeYear2016 + "(Civics, History, English, Kiswahili, Geography, BibleKnowledge, BasicMathematics, AdditionalMathematics, Biology, Physics, Chemistry, BookKeeping, Commerce, AgriculturalSc, ElectricalDraugt, ElectricalInstal, ElectricalEngnSc, ElimuYaDiniKiislam, FineArt, ArabicLang, ArchtecturualDrought, BrickworkMasonary, BuildingConstruction, CarpentryJoinery, EngineeringSci, FittingTurning, FoodNutrition, FrenchLang, InformComputer, Plumbing, Music, LiteratureEng, MechanicalDrought, MotorVehicleMech, PaintingSignWriting, PhysicalEducation, RadioTvServing, Serving, TextileDressMaking, TheatreArt, WeldingMetalFabrication, WorkshopTech) VALUES"

			if resultTdElemLength > 0:
				for x in range (5, resultTdElemLength, 5):
					student_no = resultTdElem[x].text_content().strip()
					gender = resultTdElem[x+1].text_content().strip()
					division = resultTdElem[x+3].text_content().strip()
					subjects = resultTdElem[x+4].text_content().strip()

					Civics = History = English = Kiswahili = Geography = BibleKnowledge = BasicMathematics = AdditionalMathematics = Biology = Physics = Chemistry = BookKeeping = Commerce = AgriculturalSci = ElectricalDraugting = ElectricalInstallation = ElectricalEngnSci = ElimuYaDiniKiislam = FineArt = ArabicLanguage = ArchtecturualDraught = BrickworkMasonary = BuildingConstruction = CarpentryJoinery = EngineeringSci = FittingTurning = FoodNutrition = FrenchLanguage = ComputerStudies = Plumbing = Music = LiteratureEnglish = MechanicalDraughting = MotorVehicleMech = PaintingSignWriting = PhysicalEducation = RadioTvServing = Surveying = TextileDressMaking = TheatreArt = WeldingMetalFabrication = WorkshopTech = None
					
					if "CIV - '" in subjects:
						index = subjects.find("CIV - '")
						Civics = subjects[index+1]
					elif "GEO - '" in subjects:
						index = subjects.find("GEO - '")
						Geography = subjects[index+1] 
					elif "B/MATH - '" in subjects:
						index = subjects.find("B/MATH - '")
						BasicMathematics = subjects[index+1]
					elif "HIST - '" in subjects:
						index = subjects.find("HIST - '")
						History = subjects[index+1]
					elif "ENGL - '" in subjects:
						index = subjects.find("ENGL - '")
						English = subjects[index+1]
					elif "KISW - '" in subjects:
						index = subjects.find("KISW - '")
						Kiswahili = subjects[index+1]
					elif "E/D/KIISLAMU - '" in subjects:
						index = subjects.find("E/D/KIISLAMU - '")
						ElimuYaDiniKiislam = subjects[index+1]
					elif "B/KNOWL - '" in subjects:
						index = subjects.find("B/KNOWL - '")
						BibleKnowledge = subjects[index+1]
					elif "PHY - '" in subjects:
						index = subjects.find("PHY - '")
						Physics = subjects[index+1]
					elif "CHEM - '" in subjects:
						index = subjects.find("CHEM - '")
						Chemistry = subjects[index+1]
					elif "ARABIC LANGUAGE - '" in subjects:
						index = subjects.find("ARABIC LANGUAGE - '")
						ArabicLanguage = subjects[index+1]
					elif "BIO'" in subjects:
						index = subjects.find("BIO - '")
						Biology = subjects[index+1]
					elif "COMP STUD - '" in subjects:
						index = subjects.find("COMP STUD - '")
						ComputerStudies = subjects[index+1]
					elif "B/KEEPING - '" in subjects:
						index = subjects.find("B/KEEPING - '")
						BookKeeping = subjects[index+1]
					elif "COMM - '" in subjects:
						index = subjects.find("COMM - '")
						Commerce = subjects[index+1]
					elif "AGRI - '" in subjects:
						index = subjects.find("AGRI - '")
						AgriculturalSci = subjects[index+1]
					elif "ADD MATH - '" in subjects:
						index = subjects.find("ADD MATH - '")
						AdditionalMathematics = subjects[index+1]
					elif "ELECT DRAUGHT - '" in subjects:
						index = subjects.find("ELECT DRAUGHT - '")
						ElectricalDraugting = subjects[index+1]
					elif "MECH DRAUGHT - '" in subjects:
						index = subjects.find("MECH DRAUGHT - '")
						MechanicalDraughting = subjects[index+1]
					elif "W/SHOP TECH - '" in subjects:
						index = subjects.find("W/SHOP TECH - '")
						WorkshopTech = subjects[index+1]
					elif "FITT & TURN - '" in subjects:
						index = subjects.find("FITT & TURN - '")
						FittingTurning = subjects[index+1]
					elif "ELECT INST - '" in subjects:
						index = subjects.find("ELECT INST - '")
						ElectricalInstallation = subjects[index+1]
					elif "RADIO & TV - '" in subjects:
						index = subjects.find("RADIO & TV - '")
						RadioTvServing = subjects[index+1]
					elif "ELECT ENG SC - '" in subjects:
						index = subjects.find("ELECT ENG SC - '")
						ElectricalEngnSci = subjects[index+1]
					elif "MOT VEH MECH - '" in subjects:
						index = subjects.find("MOT VEH MECH - '")
						MotorVehicleMech = subjects[index+1]
					elif "BLD CONSTR - '" in subjects:
						index = subjects.find("BLD CONSTR - '")
						BuildingConstruction = subjects[index+1]
					elif "ARCH DRAUGHT - '" in subjects:
						index = subjects.find("ARCH DRAUGHT - '")
						ArchtecturualDraught = subjects[index+1]
					elif "WELD & MET - '" in subjects:
						index = subjects.find("WELD & MET - '")
						WeldingMetalFabrication = subjects[index+1]
					elif "PLUMBING - '" in subjects:
						index = subjects.find("PLUMBING - '")
						Plumbing = subjects[index+1]
					elif "BRI & MAS - '" in subjects:
						index = subjects.find("BRI & MAS - '")
						BrickworkMasonary = subjects[index+1]
					elif "ENG SC - '" in subjects:
						index = subjects.find("ENG SC - '")
						EngineeringSci = subjects[index+1]
					elif "CARP & JOIN - '" in subjects:
						index = subjects.find("CARP & JOIN - '")
						CarpentryJoinery = subjects[index+1]
					elif "TEXTILE - '" in subjects:
						index = subjects.find("TEXTILE - '")
						TextileDressMaking = subjects[index+1]
					elif "PAINT & SIGN - '" in subjects:
						index = subjects.find("PAINT & SIGN - '")
						PaintingSignWriting = subjects[index+1]
					elif "PHY EDU - '" in subjects:
						index = subjects.find("PHY EDU - '")
						PhysicalEducatio = subjects[index+1]
					elif "FREN - '" in subjects:
						index = subjects.find("FREN - '")
						FrenchLanguage = subjects[index+1]
					elif "F.ART - '" in subjects:
						index = subjects.find("F.ART - '")
						FineArt = subjects[index+1]
					elif "FOOD - '" in subjects:
						index = subjects.find("FOOD - '")
						FoodNutrition = subjects[index+1]
					elif "LIT ENG - '" in subjects:
						index = subjects.find("LIT ENG - '")
						LiteratureEnglish = subjects[index+1]
					elif "SURVEYING - '" in subjects:
						index = subjects.find("SURVEYING - '")
						Surveying = subjects[index+1]
					elif "MUSIC - '" in subjects:
						index = subjects.find("MUSIC - '")
						Music = subjects[index+1]
					elif "THEATRE ART - '" in subjects:
						index = subjects.find("THEATRE ART - '")
						TheatreArt = subjects[index+1]
 

					insertQuery += "("+Civics+","+History+","+English+","+Kiswahili+","+Geography+","+BibleKnowledge+","+BasicMathematics+","+AdditionalMathematics+","+Biology+","+Physics+","+Chemistry+","+BookKeeping+","+Commerce+","+AgriculturalSc+","+ElectricalDraugt+","+ElectricalInstal+","+ElectricalEngnSc+","+ElimuYaDiniKiislam+","+FineArt+","+ArabicLang+","+ArchtecturualDrought+","+BrickworkMasonary+","+BuildingConstruction+","+CarpentryJoinery+","+EngineeringSci+","+FittingTurning+","+FoodNutrition+","+FrenchLang+","+InformComputer+","+Plumbing+","+Music+","+LiteratureEng+","+MechanicalDrought+","+MotorVehicleMech+","+PaintingSignWriting+","+PhysicalEducation+","+RadioTvServing+","+Serving+","+TextileDressMaking+","+TheatreArt+","+WeldingMetalFabrication+","+WorkshopTech+")"
					if (x != resultTdElemLength-1):
						insertQuery += ","
					
			dbCursor.execute(insertQuery)
			print "Done Scrapping: School Name " + str(school_name)
            		print "------------------------------------------------------------------------"



except:
	print "Unexpected error:", sys.exc_info()[0]
	print "Oops, something went wrong"


sys.exit()
