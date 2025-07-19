import pandas as pd


from DatesHandling.testingtesting import era_walk
from simplefuns.printHandler import display_df, display_df_initial

df = pd.read_excel(r'data\Отчет(Выровненный test4).xlsx')
display_df_initial(df.copy())

df = pd.DataFrame(columns = df['Services'].tolist())
df['Date'] = era_walk()
df = df.explode(column='Date')

display_df(df)

df.to_excel(r'data\Temp.xlsx', index=False)
