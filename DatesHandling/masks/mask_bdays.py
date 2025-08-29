from pandas.tseries.offsets import CDay


def mask_bdays(df, weekmask = None):
	if weekmask is not None:
		cday = CDay(weekmask=weekmask)
	else:
		cday = CDay()
	return df.Date.apply(cday.is_on_offset)