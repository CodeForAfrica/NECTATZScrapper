#=IMPORTXML("http://www.necta.go.tz/results/2014/acsee/index.htm", "//a/@href")


from lxml import html
import requests

page = requests.get('http://www.necta.go.tz/results/2014/acsee/index.htm', allow_redirects = False)

#tree contains the whole html
tree = html.fromstring(page.content)
htmlElem = html.document_fromstring(page.content)


#list of schools and uri

schools = tree.xpath('//a/text()')
schoolsUri = tree.xpath('//a/@href')
resultTable = tree.xpath('//tr/td')
resultTable2 = tree.xpath('//td')[0].text_content().strip()
data = list()
#for row in resultTable:
 #   data.append([c.text for c in row.getchildren()])


#print schoolsUri
#print schools
print schools
print len(schoolsUri)

#loop through the school names to createfile
for school in schools:
	schoolCode = school.split(' ')[0]
	#print schoolCode
	csvFileName = schoolCode + ".csv"
	csv = open(csvFileName, "w") #create or open csv, "w" to write strings
	colNames = "CNO, SEX, AGGT, DIV, DETAILED SUBJECTS\n" #column titles
	#csv.write(colNames)





