import xlwings as xw
from datetime import date, timedelta
import re
import os
import sys
import pprint
import colorsys
import itertools

XL_CENTER = -4108

yearMatch = re.compile(r'\d{8}')

def generatePalette(N):
	HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
	RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
	return RGB_tuples

def generateCalendar(startDate, endDate):
	startToEnd = []
	curDate = startDate
	dayOfWk = startDate.weekday()
	while curDate <= endDate:
		if curDate.weekday() == dayOfWk:
			startToEnd.append(curDate)
		else:
			startToEnd.append(None)
		curDate += timedelta(days = 1)
	while curDate.weekday() != dayOfWk:
		startToEnd.append(None)
		curDate += timedelta(days = 1)
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
	st2.range('A1').value = 'Machine S/N'
	st2.range('B1').value = 'Phase'
	st2.range('C1').value = wkList
	st2.range((1,3),(1,2+len(wkList))).color = 0xFF8732
	for i in range(0, len(wkList)/7):
		dateCell = st2.range((1,3+7*i),(1,9+7*i))
		dateCell.api.merge()
		dateCell.api.horizontal_alignment.set(XL_CENTER)
	machineNumRange = st2.range('A:A').options(transpose=True)
	activityNumRange = st2.range('B:B').options(transpose=True)

	dataIter = iter(eventData)
	try:
		for i, j in itertools.izip(machineNumRange, activityNumRange):
			if i.get_address() == '$A$1':
				continue
			eventObj = dataIter.next()
			i.value = eventObj.machineID
			j.value = eventObj.activityID
	except StopIteration:
		print "Machine and Activity IDs populated..."

#--------------------------------------------------------

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
except Exception as e:
	print e
	sys.exit(1)

writeExcel(st2, wkList, eventData, palette)

sys.exit(0)