# cat color = ffc000
import xlwings as xw
from datetime import date, timedelta
import re
import os
import sys

yearMatch = re.compile(r'\d{8}')

palette = [0xFF3333, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0x66AA00, 0xAA6600, 0x0066AA, 0xCC66CC, 0x526556, 0x104827, 0x9d82e1, 0xa41923, 0xb3a678, 0xD43A12]


def generateCalendar(startDate, endDate):
	startToEnd = []
	wkList = []
	curDate = startDate
	startDayOfWk = startDate.weekday()
	while curDate <= endDate:
		if curDate != startDate and curDate.weekday() == startDayOfWk:
			startToEnd.append('--------')
		startToEnd.append(curDate)
		curDate += timedelta(days = 1)
	for i in range(0, len(startToEnd)/7):
		wkList.append(startToEnd[i:i+7])

	wkList.append(startToEnd[(len(startToEnd)/7)*7:len(startToEnd)])

	return startToEnd

def writeExcel(st, st2, numDays, start, end, wkList):
	objectiveType = []
	categories = {}
	curCategory = None
	colors = []
	row = 1
	while st.range('A'+str(row)).value != None or st.range('B'+str(row)).value != None or st.range('C'+str(row)).value != None or st.range('D'+str(row)).value != None:
		if row == 1:
			row += 1
			continue
		if st.range('B'+str(row)).color != None:
			colors.append(st.range('B'+str(row)).color)
			categories[st.range('B'+str(row)).value] = []
			curCategory = st.range('B'+str(row)).value
		elif curCategory != None:
			newEntry = (st.range('A'+str(row)).value, st.range('B'+str(row)).value, st.range('C'+str(row)).value, st.range('D'+str(row)).value) 
			categories[curCategory].append(newEntry)
			if st.range('A'+str(row)).value not in objectiveType:
				objectiveType.append(st.range('A'+str(row)).value)
		row += 1

	colorIdx = 0
	row = 2
	for i in categories:
		st2.range('B'+str(row)).options(transpose = True).value = i
		st2.range('B'+str(row)).options(transpose = True).color = colors[colorIdx]
		row += 1
		for j in categories[i]:
			st2.range('C'+str(row)).options(transpose = True).value = j[0]
			st2.range('D'+str(row)).options(transpose = True).value = j[1]
			print j[2], start, row, (j[2].date()-start).days
			# st2.cells(row, 6+(j[2].date()-start).days).value = 'Start'
			# st2.cells(row, 6+(j[3].date()-start).days).value = 'End'
			st2.cells(row, 6+(wkList.index(j[2].date()))).value = 'Start'
			st2.cells(row, 6+(wkList.index(j[3].date()))).value = 'End'
			st2.range((row, 6+(wkList.index(j[2].date()))), (row, 6+(wkList.index(j[3].date())))).color = palette[objectiveType.index(j[0])]
			row += 1
	
		row += 1
		colorIdx += 1

	st2.range((1,1),(row,5)).columns.autofit()
	# st2.range("A1:E1").column_width = 2
	print len(objectiveType)
#--------------------------------

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

print("Generating and Exporting Calendar to Excel...\nGeneration done in Calendar Tab")

wkList = generateCalendar(startDate, endDate)

wb = xw.Book('966GC sample.xlsx')
st = wb.sheets['Sheet1']

st2 = wb.sheets['calendar']
st2.clear()
st2.range('F2').options(transpose = False).value = wkList
weekday = []
for i in wkList:
	if type(i) == date:
		day = ['M','T','W','Th','F','Sa','Su']
		weekday.append(day[i.weekday()])
	else:
		weekday.append(None)
st2.range('F1').options(transpose = False).value = weekday

try:
	writeExcel(st, st2, len(wkList), startDate, endDate, wkList)
except:
	print "Warning: Date range specified does not cover some events. Please restart program and indicate a date range that matches all project events.\n" 