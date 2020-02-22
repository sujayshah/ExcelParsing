import openpyxl as pyxl
from openpyxl import formula
from datetime import date, timedelta, datetime
import platform
import colorsys
import pandas as pd

class EXCEL_FUNCS:
	def __init__(self, func_type):
		self.func_type = func_type

	def runFunction(self, st, op_range, cellCache, offset = 0, secondary_range = None): 
		if self.func_type == 'MIN(':
			# print("getMin")
			return self.getMin(st, op_range, cellCache)
		elif self.func_type == 'MAX(':
			return self.getMax(st, op_range, cellCache)
			# print("getMax")
		elif self.func_type == 'WORKDAY(':
			# print("getWorkday")
			return self.getWorkday(st, op_range, cellCache, offset, secondary_range)
		elif op_range:
			# print("getCellValue")
			return self.getCellValue(st, op_range, offset, cellCache)
		else:
			return None

	def getCellValue(self, st, op_range, offset, cellCache):
		cellValue = st[op_range].value
		if not isinstance(cellValue, datetime):
			cellValue = evaluateFormulaToDate(st, cellValue, cellCache)
		return cellValue + timedelta(days = offset)

	def getMin(self, st, op_range, cellCache):
		min = None
		try:
			for row in st[op_range]:
				for cell in row:
					evalCell = cell.value
					if not isinstance(cell.value, datetime):
						evalCell = evaluateFormulaToDate(st, cell.value, cellCache)
					if not min:
						min = evalCell
					elif evalCell < min:
						min = evalCell
		except Exception as e:
			print(e)
		return min

	def getMax(self, st, op_range, cellCache):
		max = None
		try:
			for row in st[op_range]:
				for cell in row:
					evalCell = cell.value
					if not isinstance(cell.value, datetime):
						evalCell = evaluateFormulaToDate(st, cell.value, cellCache)
					if not max:
						max = evalCell
					elif evalCell > max:
						max = evalCell
		except Exception as e:
			print(e)
		return max
	
	def getWorkday(self, st, op_range, cellCache, offset, secondary_range):
		workday = st[op_range].value
		try:
			if not isinstance(workday, datetime):
				workday = evaluateFormulaToDate(st, workday, cellCache)
			if workday.weekday() >= 5:
				workday -= timedelta(days = workday.weekday() - 4)
			for i in range(0, offset):
				if workday.weekday() >= 5:
					workday += timedelta(days = 7 - workday.weekday())
				workday += timedelta(days = 1)
		except Exception as e:
			print(e)
		while workday.weekday() >= 5:
			workday += timedelta(days = 1)
		return workday

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

def evaluateFormulaToDate(st, evalString, cellCache):
	if isinstance(evalString, datetime):
		return evalString
	else:
		tok = formula.Tokenizer(evalString)
		func_type = next((t for t in tok.items if t.type == 'FUNC' and t.subtype == 'OPEN'), None)
		operand_range_iter = (t for t in tok.items if t.type == 'OPERAND' and t.subtype == 'RANGE')
		operand_range = next(operand_range_iter, None)
		secondary_range = next(operand_range_iter, None)
		offset = next((t for t in tok.items if t.type == 'OPERAND' and t.subtype == 'NUMBER'), 0)
		offset_infix = next((t for t in tok.items if t.type == 'OPERATOR-INFIX'), 0)
		# print(func_type, operand_range, secondary_range, offset)
		# print("\n".join("%12s%11s%9s" % (t.value, t.type, t.subtype) for t in tok.items))

		if func_type:
			func_type = func_type.value
		formula_func = EXCEL_FUNCS(func_type)

		if operand_range:
			operand_range = operand_range.value

		if secondary_range:
			secondary_range = secondary_range.value

		if isinstance(offset, pyxl.formula.tokenizer.Token) and isinstance(offset.value, str):
			offset = int(float(offset.value))
			if offset_infix and offset_infix.value == '-':
				offset *= -1

		funcOutput = formula_func.runFunction(st=st, op_range=operand_range, cellCache=cellCache, 
		offset=offset, secondary_range=secondary_range)
		return funcOutput

def parseSchedule(st, userStartDate, userEndDate):
	categories = []
	eventList = []
	cellCache = {}
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

	# tok = formula.Tokenizer(st['C47'].value)
	# func_type = next((t for t in tok.items if t.type == 'FUNC' and t.subtype == 'OPEN'), None)
	# for t in tok.items:
	# print(t.value, t.type, t.subtype)
	output = evaluateFormulaToDate(st, st['C47'].value, cellCache)
	# print(output)

	########################################
	# row = 0
	# for a, b, c, d in zip(st['A'], st['B'], st['C'], st['D']):
	# 	row += 1
	# 	# Title Row
	# 	if row == 1:
	# 		continue
	# 	# Check if Date
	# 	if isinstance(c.value, datetime):
	# 		cellCache[c.coordinate] = c.value
	# 		# c.value.date() < userStartDate or c.value.date() > userEndDate or d.value.date() < userStartDate or d.value.date() > userEndDate:
	# 		# raise ValueError

	# 	# Check if formula
	# 	elif isinstance(c.value, str) and c.value.startswith('='):
	# 		return evaluateFormulaToDate(st, c.value, cellCache)

	# 	# Unknown Type in Column C/D
	# 	else:
	# 		raise TypeError
		##############################
		# if a.value == None:
		# 	eventList.append(Event(b.value, c.value.date(), d.value.date()))
		# if a.value != None:
		# 	eventList[-1].subTasks.append(Task(a.value, b.value, c.value.date(), d.value.date()))
		# 	if a.value not in categories:
		# 		categories.append(a.value)

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
	# try:
	# 	categories, eventData = parseSchedule(st, start, end)
	# except ValueError as ve:
	# 	raise Exception('Invalid Date or Offset')
	# except TypeError as te:
	# 	raise Exception('A cell in column C or D has an invalid date or formula')
	categories, eventData = parseSchedule(st, start, end)
	# print(categories, eventData)
	if "Calendar" not in wb.sheetnames:	
		ws = wb.create_sheet("Calendar")
	# writeExcel(st, wkList, eventData, palette, start)
	wb.save(file_path)
