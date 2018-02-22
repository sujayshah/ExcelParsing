import xlwings as xw
from datetime import date, timedelta
import re

re.compile(r'\d{1,2}-\d{1,2}-\d{1,2}')

palette = [0xFF3333, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0x66AA00, 0xAA6600, 0x0066AA, 0xCC66CC, 0x526556, 0x104827, 0x9d82e1, 0xa41923, 0xb3a678]

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

def writeExcel(st, st2, yearList):
	categories = []
	job = []
	row = 1
	while st.range('A'+str(row)).value != None or st.range('B'+str(row)).value != None or st.range('C'+str(row)).value != None or st.range('D'+str(row)).value != None:
		row += 1
		# print "row: ", row, " ", st.range('A'+str(row)).value
		if st.range('A'+str(row)).value not in categories and st.range('A'+str(row)).value != None:
			categories.append(st.range('A'+str(row)).value)
		if row != 1 and st.range('B'+str(row)).color == None:
			job.append((st.range('B'+str(row)).value, st.range('A'+str(row)).value, st.range('C'+str(row)).value, st.range('D'+str(row)).value))
		# if st.range('B'+str(row)).color != 0xFFFFFF:

	for i in job:
		print i
	print len(job)
	print len(categories)

	partsRange = st2.range('B2')
	partsRange = partsRange.resize(len(categories),1)
	for i in range(0, len(partsRange)):
		partsRange[i].value = categories[i]
		partsRange[i].color = palette[i]
	partsRange.autofit()
	st2.range('C1').value = 'Start Date'
	st2.range('D1').value = 'End Date'

	dateRange = st2.range('F1')
	dateRange = dateRange.resize(1,len(yearList))
	dateRange.value = yearList
	j = 7
	while j < len(yearList):
		dateRange[j].color = (0, 0, 0)
		j += 8
	dateRange.autofit()
	# print type(dateRange[0])
	dateRange.api.ColumnWidth = 1


startday = raw_input("Enter Starting Weekday (S, M, T, W, Th, F, Sa): ")
startday = startday.lower()
wkday = -1
while wkday < 0:
	if startday == 's':
		wkday = 6
	elif startday == 'm':
		wkday = 0
	elif startday == 't':
		wkday = 1
	elif startday == 'w':
		wkday = 2
	elif startday == 'th':
		wkday = 3
	elif startday == 'f':
		wkday = 4
	elif startday == 'sa':
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
wb = xw.Book('966GC sample.xlsx')
st = wb.sheets['Sheet1']
yearList = []
for i in range(0,53):
	for j in range(0,7):
		if i < 51:
			yearList.append(wkList[j][i])
		if (len(wkList[j]) > 51 and i == 51) or (len(wkList[j]) == 53 and i == 52):
			yearList.append(wkList[j][i])
	yearList.append('')
# print yearList


st2 = wb.sheets['calendar']
st2.clear()
writeExcel(st, st2, yearList)

