import xlwings as xw
from datetime import date, timedelta
import re
import os
import sys
import pprint
import colorsys
import itertools

yearMatch = re.compile(r'\d{8}')

def generatePalette(N):
	HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
	RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
	return RGB_tuples

def generateCalendar(startDate, endDate):
	startToEnd = []
	curDate = startDate
	while curDate <= endDate:
		startToEnd.append(curDate)
		curDate += timedelta(days = 7)
	return startToEnd

def parseSchedule(st, categories):
	class Event():
		def __init__(self, activity, start, finish): 
			self.machineID = activity[activity.find('(')+1:activity.find(')')]
			self.activityID = activity[:activity.find('(')]
			self.startDate = start
			self.finishDate = finish
			self.subTasks = []
	class Task():
		def __init__(self, category, task, start, finish):
			self.category = category
			self.task = task
			self.startDate = start
			self.finishDate = finish

	eventList = []
	row = 0
	for a, b, c, d in itertools.izip(st.range('A:A'), st.range('B:B'), st.range('C:C'), st.range('D:D')):
		row += 1
		if row == 1:
			continue
		if b.value == None:
			break
		if a.value == None:
			eventList.append(Event(b.value, c.value.date(), d.value.date()))
		if a.value != None:
			eventList[-1].subTasks.append(Task(a.value, b.value, c.value.date(), d.value.date()))
			if a.value not in categories:
				categories.append(a.value)
	# for i in eventList:
	# 	print i.machineID, "  ", i.activityID, "     ", i.startDate, "      ", i.finishDate
	# 	for j in i.subTasks:
	# 		print j.category, "    ", j.startDate, "    ", j.finishDate
	# 	print '\n'
	return eventList

def writeExcel(st2, wkList, eventData, palette):
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

print("Generating calendar...")

#--------------------------------------------------------

wkList = generateCalendar(startDate, endDate)
print("Calendar generated. Exporting to Excel...")

wb = xw.Book('Program Validation Planning Tool.xlsx')
st = wb.sheets[0]

try:
	st2 = wb.sheets['calendar']
	st2.clear()
except Exception as e:
	print type(e)
	sheets = wb.sheets
	sheets.add('calendar', after = st)

try:
	categories = []
	eventData = parseSchedule(st, categories)
	palette = generatePalette(1+len(eventData)+len(categories))
	writeExcel(st2, wkList, eventData, palette)
except Exception as e:
	print e
	sys.exit(1)

sys.exit(0)