import xlwings as xw
from datetime import date, timedelta


labels = 'System,,HYD,ELI,EIC,ENG,COO,STRU,LSTRU,ESI,CAB'
palette = [0xFF3333, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0x66AA00, 0xAA6600, 0x0066AA]

def generateCalendar(wkday, year):
	d = date(year, 1, 1)
	# if weekday == 's':
	# 	off = 6
	# elif:

	if wkday - d.weekday() < 0:
		wkday += 7
	d += timedelta(days = wkday - d.weekday())
	while d.year == year:
		yield d
		d += timedelta(days = 7)

# def parseExcel(wb):


def writeExcel(st, yearList):
	categories = labels.split(',')
	# row = 2
	# for i in categories:
	# 	st.range('B'+str(row)).value = i
	# 	row += 1

	partsRange = st.range('B2')
	partsRange = partsRange.resize(len(categories),1)
	for i in range(0, len(partsRange)):
		partsRange[i].value = categories[i]
		if i >= 2:
			partsRange[i].color = palette[i-2]
	st.range('C1').value = 'Start Date'
	st.range('D1').value = 'End Date'

	dateRange = st.range('F1')
	dateRange = dateRange.resize(1,len(yearList))
	dateRange.value = yearList
	j = 7
	while j < len(yearList):
		dateRange[j].color = (0, 0, 0)
		j += 8
	dateRange.autofit()
	print type(dateRange[0])
	dateRange.api.ColumnWidth = 1


startday = raw_input("Enter Starting Weekday (S, M, T, W, Th, F, Sa): ")
wkday = -1
while wkday < 0:
	if startday == 'S':
		wkday = 6
	elif startday == 'M':
		wkday = 0
	elif startday == 'T':
		wkday = 1
	elif startday == 'W':
		wkday = 2
	elif startday == 'Th':
		wkday = 3
	elif startday == 'F':
		wkday = 4
	elif startday == 'Sa':
		wkday = 5
	else:
		print "Invalid Input, please try again\n------------------\n"
		startday = raw_input("Enter Starting Weekday (S, M, T, W, Th, F, Sa): ")
while True:
	year = raw_input("Enter Year(s) (, for nonconsecutive years, - for consecutive years): ")
	try:
		year = int(year)
		break
	except:
		print "Try again"
wkList = []
for i in range(wkday, wkday+7):
	wkList.append([])
	for d in generateCalendar(i, int(year)):
		# print d
		wkList[i-wkday].append(d)
wb = xw.Book('ws.xlsx')
st = wb.sheets['Sheet1']
st.clear()
yearList = []
for i in range(0,53):
	for j in range(0,7):
		if i < 51:
			yearList.append(wkList[j][i])
		if (len(wkList[j]) > 51 and i == 51) or (len(wkList[j]) == 53 and i == 52):
			yearList.append(wkList[j][i])
	yearList.append('')
print yearList
writeExcel(st, yearList)

# parseExcel(wb)
