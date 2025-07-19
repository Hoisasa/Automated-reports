# if item.startswith('-'):
# 	print(True, item)
# else:
# 	print(False, item)

if row in [3, 4, 39, 40]:
	service = item.iloc[1]
	service = '-    ' + service.strip()
	df.iloc[row, 1] = service