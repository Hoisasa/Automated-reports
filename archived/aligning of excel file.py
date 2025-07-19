
df = pd.read_excel('Отчет.xlsx')

df = df.iloc[1:, 1:].reset_index(drop=True)
df.to_excel('Отчет(Выровненный).xlsx', index=False)
