import pandas as pd

def display_df(df):
	df = df.T
	df.index = df.index.map(lambda x: str(x)[:30])
	df.loc['Date', 0:'Total'] = df.loc['Date', 0:'Total'].map(lambda x: x.day if isinstance(x, pd.Timestamp) else x)
	
	print(df.fillna('').to_string())
	
def display_df_initial(df):
	df.loc[:, 'Services'] = df.loc[:, 'Services'].map(lambda x: str(x)[:30])
	print(df.fillna('').to_string())
	