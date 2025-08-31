import random

import dearpygui.dearpygui as dpg
import numpy as np
import pandas as pd


def df_table(df, transpose= False):
	df_on_display = df.T if transpose else df
	
	with dpg.theme() as item_theme:
		with dpg.theme_component(dpg.mvAll):
			dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6, category=dpg.mvThemeCat_Core)
			dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 1.5, 1.5, category=dpg.mvThemeCat_Core)
	
	
	with dpg.table(tag='DataframeView', header_row=False, row_background=False,
				   borders_innerH=False, borders_outerH=False,
				   borders_innerV=False, borders_outerV=False) as table_id:
		dpg.bind_item_theme(table_id, item_theme)
		dpg.add_table_column(tag='index', init_width_or_weight=400, width_fixed=True)
		for i, column_label in enumerate(list(df_on_display.columns)):
			dpg.add_table_column(tag=str(column_label), init_width_or_weight=33, width_fixed=True)
		df_on_display.loc['Date', 0:'Total'] = df_on_display.loc['Date', 0:'Total'].map(lambda x: x.day if isinstance(x, pd.Timestamp) else x)

		for i, row_label in enumerate(list(df_on_display.index)):
			with dpg.table_row(tag=str(row_label)):
				dpg.add_text('Дата' if row_label == 'Date' else row_label)
				for j, num in enumerate(list(df_on_display.columns)):
					with dpg.table_cell() as cell:
						cell_value = df_on_display.fillna('').loc[row_label, num]
						if type(cell_value) == float:
							cell_value = int(cell_value)
						input_cell = dpg.add_input_text(default_value=cell_value, width=33, height=16)
						dpg.bind_item_theme(input_cell, item_theme)
						

def table_update(_df):
	for index, row in _df.T.fillna('').iterrows():
		if index.startswith('-'):
			row_children = np.array(dpg.get_item_children(index)[1][1:])
			row_children += 1
			for cell in zip(row_children, row):
				dpg.set_value(cell +1, row)
		


	
						