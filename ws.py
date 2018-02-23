import xlwings as xw
from datetime import date, timedelta
import re

yearMatch = re.compile(r'\d{8}')

palette = [0xFF3333, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0x66AA00, 0xAA6600, 0x0066AA, 0xCC66CC, 0x526556, 0x104827, 0x9d82e1, 0xa41923, 0xb3a678]


def generateCalendar(startDate, endDate):
	startToEnd = []
	wkList = []
	curDate = startDate
	startDayOfWk = startDate.weekday()
	while curDate <= endDate:
		startToEnd.append(curDate)
		curDate += timedelta(days = 1)
	for i in range(0, (endDate-startDate).days+1):
		print i


	

def writeExcel(st, st2, yearList):
	categories = {}
	curCategory = None
	types = []
	job = []
	row = 1
	while st.range('A'+str(row)).value != None or st.range('B'+str(row)).value != None or st.range('C'+str(row)).value != None or st.range('D'+str(row)).value != None:
		if row == 1:
			row += 1
			continue
		if st.range('B'+str(row)).color != None:
			categories[st.range('B'+str(row)).value] = []
			curCategory = st.range('B'+str(row)).value
		elif curCategory != None:
			newEntry = (st.range('A'+str(row)).value, st.range('B'+str(row)).value,  st.range('C'+str(row)).value, st.range('D'+str(row)).value) 
			categories[curCategory].append(newEntry)
		# if st.range('A'+str(row)).value not in types and st.range('A'+str(row)).value != None:
		# 	types.append(st.range('A'+str(row)).value)
		# if row != 1 and st.range('B'+str(row)).color == None:
		# 	job.append((st.range('B'+str(row)).value, st.range('A'+str(row)).value, st.range('C'+str(row)).value, st.range('D'+str(row)).value))
		row += 1

	for i in categories:
		print i
		for j in range(0, len(categories[i])):
			print categories[i][j]
		print "\n\n"

#------------------------------------

	# for i in job:
	# 	print i
	# print len(job)
	# print len(types)

	# partsRange = st2.range('B2')
	# partsRange = partsRange.resize(len(types),1)
	# for i in range(0, len(partsRange)):
	# 	partsRange[i].value = types[i]
	# 	partsRange[i].color = palette[i]
	# partsRange.autofit()
	# st2.range('C1').value = 'Start Date'
	# st2.range('D1').value = 'End Date'

	# dateRange = st2.range('F1')
	# dateRange = dateRange.resize(1,len(yearList))
	# dateRange.value = yearList
	# j = 7
	# while j < len(yearList):
	# 	dateRange[j].color = (0, 0, 0)
	# 	j += 8
	# dateRange.autofit()
	# dateRange.api.ColumnWidth = 1


# startday = raw_input("Enter Starting Weekday (S, M, T, W, Th, F, Sa): ")
# startday = startday.lower()
# wkday = -1
# while wkday < 0:
# 	if startday == 's':
# 		wkday = 6
# 	elif startday == 'm':
# 		wkday = 0
# 	elif startday == 't':
# 		wkday = 1
# 	elif startday == 'w':
# 		wkday = 2
# 	elif startday == 'th':
# 		wkday = 3
# 	elif startday == 'f':
# 		wkday = 4
# 	elif startday == 'sa':
# 		wkday = 5
# 	else:
# 		print "Invalid Input, please try again\n------------------\n"
# 		startday = raw_input("Enter Starting Weekday (S, M, T, W, Th, F, Sa): ")
while True:
	start = raw_input("Enter Start Date in the form MMDDYYYY: ")
	if(re.match(yearMatch, start)):
		try:
			startDate = date(int(start[4:]), int(start[0:2]), int(start[2:4]))
			break
		except:
			print "Invalid Date, please try again"
	else:
		print "Invalid Input, please try again"

while True:
	end = raw_input("Enter End Date in the form MMDDYYYY: ")
	if(re.match(yearMatch, end)):
		try:
			endDate = date(int(end[4:]), int(end[0:2]), int(end[2:4]))
			if endDate <= startDate:
				print "Invalid End Data - Must be a date after the start date"
				continue
			break
		except:
			print "Invalid Date, please try again"
	else:
		print "Invalid Input, please try again"

print("Generating and Exporting Calendar to Excel")

wkList = generateCalendar(startDate, endDate)

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

