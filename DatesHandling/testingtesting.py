import pandas as pd
from pandas.tseries import offsets

def era_walk(month_offset = 0):
	month = pd.Timestamp.today().replace(day=1).normalize()
	if month_offset:
		offset = offsets.MonthBegin(month_offset)
		month -= offset
	
	date = month
	allDays = []
	while month.month==date.month:
		allDays.append(date)
		date += offsets.Day()
	return allDays
