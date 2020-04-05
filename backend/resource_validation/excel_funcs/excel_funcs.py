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
			raise(e)
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
			raise(e)
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
			raise(e)
		while workday.weekday() >= 5:
			workday += timedelta(days = 1)
		return workday