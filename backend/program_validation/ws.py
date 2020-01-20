import openpyxl as pyxl
from openpyxl import formula
from datetime import date, timedelta
import platform
import colorsys
import pandas as pd

class EXCEL_FUNCS:
	def __init__(self, func_type):
		self.func_type = func_type

	def runFunction(self, st, range): 
		if self.func_type == 'MIN(':
			return self.getMin(st, range)
		elif self.func_type == 'MAX(':
			return self.getMax(st, range)

	def getMin(self, st, range):
		try:
			for cell in st[range]:
				print(cell.value)
		except Exception as e:
			print(e)
		return range

	def getMax(self, st, range):
		return range

def generatePalette(N):
	HSV_tuples = [(x*1.0/N, 0.5, 0.8) for x in range(N)]
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

def parseSchedule(st, userStartDate, userEndDate):
	categories = []
	eventList = []
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

	# tok = formula.Tokenizer(st['C2'].value)
	# for t in tok.items:
	# 	print(t.value, t.type, t.subtype)
	row = 0
	for a, b, c, d in zip(st['A'], st['B'], st['C'], st['D']):
		row += 1
		if row == 1:
			continue
		tok = formula.Tokenizer(c.value)
		if not tok.items:
			print("Actual Date", c.value)
			if c.value.date() < userStartDate or c.value.date() > userEndDate or d.value.date() < userStartDate or d.value.date() > userEndDate:
				raise ValueError
		else:
			func_type = next(t for t in tok.items if t.type == 'FUNC' and t.subtype == 'OPEN').value
			operand_range = next(t for t in tok.items if t.type == 'OPERAND' and t.subtype == 'RANGE').value
			formula_func = EXCEL_FUNCS(func_type)
			formula_func.runFunction(st, operand_range)
		if a.value == None:
			eventList.append(Event(b.value, c.value.date(), d.value.date()))
		if a.value != None:
			eventList[-1].subTasks.append(Task(a.value, b.value, c.value.date(), d.value.date()))
			if a.value not in categories:
				categories.append(a.value)
	return categories, eventList

def writeExcel(st2, wkList, eventData, palette, categories, startDate):
	st2.range('A1').value = 'Machine S/N'
	st2.range('B1').value = 'Phase'
	st2.range('C1').value = wkList
	st2.range((1,3),(1,2+len(wkList))).color = 0x0095dc
	for i in range(0, len(wkList)/7):
		dateCell = st2.range((1,3+7*i),(1,9+7*i))
		if platform.system() == 'Windows':
			dateCell.api.Merge()
			dateCell.api.HorizontalAlignment = XL_CENTER
			dateCell.api.Borders.Weight = XL_THICK
			# dateCell.api.Borders.Color = 0xFFFFFF
		else:
			dateCell.api.merge()
			dateCell.api.horizontal_alignment.set(XL_CENTER)
			dateCell.api.border_around(color=0xFFFFFF, weight=XL_THICK)
	machineNumRange = st2.range('A:A').options(transpose=True)
	activityNumRange = st2.range('B:B').options(transpose=True)

	dataIter = iter(eventData)
	try:
		for i, j in zip(machineNumRange, activityNumRange):
			addr = int(re.sub('[^0-9]','', i.get_address()))
			if i.get_address() == '$A$1':
				continue
			eventObj = dataIter.next()
			i.value = eventObj.machineID
			j.value = eventObj.activityID
			for subTask in eventObj.subTasks:
				st2.range((addr, 3+(subTask.startDate - startDate).days)).value = subTask.task
				mergedTaskCell = st2.range((addr, 3+(subTask.startDate - startDate).days), (addr, 3+(subTask.finishDate - startDate).days))
				mergedTaskCell.color = (256*palette[categories.index(subTask.category)][2], 256*palette[categories.index(subTask.category)][1], 256*palette[categories.index(subTask.category)][0]) 
				if platform.system() == 'Windows':
					mergedTaskCell.api.Merge()
					mergedTaskCell.autofit()
					mergedTaskCell.api.HorizontalAlignment = XL_CENTER
					mergedTaskCell.api.Borders.Weight = XL_THICK
					# dateCell.api.Borders.Color = 0xFFFFFF
				else:
					mergedTaskCell.api.merge()
					mergedTaskCell.autofit()
					mergedTaskCell.api.horizontal_alignment.set(XL_CENTER)
					mergedTaskCell.api.border_around(color=0xFFFFFF, weight=XL_THICK)
	except StopIteration:
		machineNumRange.autofit()
		activityNumRange.autofit()
		print("Machine and Activity IDs populated...")
	except Exception as e:
		print(e)
	for i in range(1, 2+len(eventData)):
		st2.range((i,1)).api.RowHeight *= 2
		# st2.range((i,1)).autofit()
#--------------------------------------------------------

def program_validation(file_path, palette, start, end):
	wkList = generateCalendar(start, end)
	wb = pyxl.load_workbook(file_path)
	st = wb[wb.sheetnames[0]]
	try:
		categories, eventData = parseSchedule(st, start, end)
	except ValueError as ve:
		raise Exception('Invalid Date Range')
	# print(categories, eventData)
	ws = wb.create_sheet("Calendar")
	# writeExcel(st, wkList, eventData, palette, start)
	wb.save(file_path)
