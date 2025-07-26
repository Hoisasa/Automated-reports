from pandas.tseries.offsets import CDay


def mask_cfg(df, weekmask = None):
	
	for
		for item in df.iterrows():
		
	
	if weekmask is not None:
		cday = CDay(weekmask=weekmask)
	else:
		cday = CDay()
	return df.Date.apply(cday.is_on_offset)