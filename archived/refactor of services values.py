for service in df.iloc[[4, 5, 40, 41], 1]:
	service = '- ' + service
	
	if service.startswith('-'):
		print(True, service[:30])
	else:
		print(False, service[:30])