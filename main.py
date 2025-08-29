# import pandas as pd
# import dearpygui.dearpygui as dpg
#
#
# from DatesHandling.testingtesting import era_walk
# from simplefuns.printHandler import display_df, display_df_initial
#
#
# df = pd.read_excel(r'data\Отчет(Выровненный test4).xlsx')
# display_df_initial(df.copy())
#
# df = pd.DataFrame(columns = df['Services'].tolist())
# df['Date'] = era_walk()
# df = df.explode(column='Date')
#
# display_df(df)
#
#
#
# df.to_excel(r'data\Temp.xlsx', index=False)

import dearpygui.dearpygui as dpg
import numpy as np
import pandas as pd

from configparser import ConfigParser

from dearpygui.dearpygui import configure_item
from pandas.tseries.offsets import BDay

from GUI.customWidgets.input_table import df_table
from fonts.font_setup import font_setup
from pipe import select, Pipe, tee





@Pipe
def organised_child_data(config_column):
	target_column = dpg.get_alias_id(config_column)
	table_children = dpg.get_item_children('ConfigView')
	table_col_children, table_row_children = list(table_children.values())[:2]
	try:
		idx = table_col_children.index(target_column)
	except ValueError:
		print(f"Critical error: target column {target_column} of config not found!")
		import sys
		sys.exit(1)  # exit the app with error code
	return table_row_children, idx


@Pipe
def checkbox_states(children_data):
	shift_to_columns = np.array(children_data[0], dtype=object)
	shift_to_columns += children_data[1] + 1
	column_items = list(shift_to_columns)
	checkbox_values = dpg.get_values(column_items)
	return checkbox_values


@Pipe
def mask_notempty(checkbox_values, df):
	mask_active = df.columns.str.startswith('-')
	checkbox_iterator = iter(checkbox_values)
	for i, status in enumerate(mask_active):
		if status:
			mask_active[i] = next(checkbox_iterator)
	return mask_active


@Pipe
def time_val_matrix(list_of_services):
	pass

def set_active_columns():
	for day in weekday_colors.keys():
		_id = current_client["value"]
		dpg.configure_item(day, enabled=config.getboolean(f"Weekdays:{_id}", day))
		pass

def is_active(id):
	return config.getboolean(f"Client:{id}", "active")

def get_name(id):
	return config.get(f"Client:{id}", "name")

def update_WDcb(id: int):
	checkboxes = dpg.get_item_children("workDaysRow")
	for day in checkboxes[1]:
		# check parsed children for key in their tag
		# the key is WDcb short for Weekdays checkbox
		name_check = dpg.get_item_alias(day)
		if "WDcb" not in name_check:
			raise Exception("failed to parse ids from row")
		correct_name = name_check[:3]
		new_cb_state = config.getboolean(f"Weekdays:{id}", correct_name)
		dpg.set_value(day, new_cb_state)

def combo_client_callback(sender, app_data, user_data):
	_id = ids_dict[app_data]
	user_data["value"] = _id
	update_WDcb(_id)
	set_active_columns()
	pass

def WDcb_callback(sender, app_data, user_data):
	build_string = f"Weekdays:{user_data["value"]}"
	config[build_string][sender[:3]] = str(app_data)
	with open("configs/clientsbase.ini", "w", encoding="utf-8") as f:
		config.write(f)
	set_active_columns()
	pass

def step_one(sender, app_data, user_data):
	mask_columns = 'Active' | organised_child_data() | checkbox_states() | mask_notempty(user_data)
	updated_user_data = mask_columns | time_val_matrix(user_data)
	user_data.loc[:, mask_columns] = pd.DataFrame(matrix, columns=user_data.columns.loc[mask_columns])
	update_table(user_data)

# for index, service in enumerate(list_of_services):
#
#
#
# 	return temp_df
#
#
#
# def update_table():
# 	pass

dpg.create_context()

config = ConfigParser()
config.read("configs/clientsbase.ini", encoding="utf-8")

max_id = int(config.sections()[-1].split(sep=":")[1]) + 1
clients_dict = {id: get_name(id) for id in range(1, max_id)}
ids_dict = {get_name(id): id for id in range(1, max_id)}
current_client = {"value": 1}


df = pd.read_excel('data/Temp.xlsx')
for i, col in enumerate(df.columns):
	if ' та інші послуги' in col and len(col) == 26:
		df = df.rename(columns={df.columns[i]: '- та інші послуги2'})
df.columns = df.columns.str.replace('\u00A0', '')
df.columns = df.columns.str.replace(r'(-) {1,}', '-    ', regex=True)

rows_count = df.columns.size
font_size = ((1020 - 40 - 3 * rows_count) / rows_count) * 0.75
font_size = min(24, font_size)
mask_services = df.columns.str.startswith('-')
df_services = df.loc[:, mask_services]
bday = BDay()
isBday = bday.is_on_offset

font_setup(font_size)

weekday_colors = {"Mon": (225, 200, 235, 255),
				  "Fri": (255, 200, 200, 255),
				  "Thu": (255, 220, 200, 255),
				  "Wed": (240, 240, 200, 255),
				  "Tue": (200, 245, 210, 255),
				  }
weekday_themes = []
for key, value in weekday_colors.items():
	with dpg.theme() as theme:
		with dpg.theme_component(dpg.mvInputText):
			dpg.add_theme_color(dpg.mvThemeCol_FrameBg, value, category=dpg.mvThemeCat_Core)
			dpg.add_theme_color(dpg.mvThemeCol_Text, (20, 20, 20, 255), category=dpg.mvThemeCat_Core)
	weekday_themes.append(theme)

with dpg.window(label='GeneratorConfig', tag='GeneratorConfig', width=1500, show=False, popup=True) as conf:
	with dpg.table(tag='ConfigView', header_row=True,
				   row_background=False, borders_innerH=False,
				   borders_outerH=False, borders_innerV=False,
				   borders_outerV=False) as cfg_table:
		
		dpg.add_table_column(label='Сервис', tag='param name', init_width_or_weight=800, width_fixed=True)
		dpg.add_table_column(label='ВКЛ', tag='Active', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Все', tag='Wee', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Пн', tag='Mon', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Вт', tag='Tue', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Ср', tag='Wed', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Чт', tag='Thu', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Пт', tag='Fri', init_width_or_weight=33, width_fixed=True)
		

		
		for cfg in list(df_services.columns):
			with dpg.table_row(label=cfg + 'cfg'):
				dpg.add_text(cfg, label=cfg + 'name')
				dpg.add_checkbox(tag=f'{cfg}Active', default_value=True)
				dpg.add_checkbox(tag=f'{cfg}Wee')
				dpg.add_checkbox(tag=f'{cfg}Mon')
				dpg.add_checkbox(tag=f'{cfg}Tue')
				dpg.add_checkbox(tag=f'{cfg}Wed')
				dpg.add_checkbox(tag=f'{cfg}Thu')
				dpg.add_checkbox(tag=f'{cfg}Fri')
	
	set_active_columns()

with dpg.window(label='Options', tag='Options', width=600, show=True, popup=True) as conf:
	dpg.add_combo(list(clients_dict.values()),
				  label="Список клиентов", tag="combo_clients",
				  default_value=list(clients_dict.values())[0],
				  callback=combo_client_callback,
				  user_data=current_client,
				  )
	
	with dpg.table(tag='Weekdays', header_row=True,
				   row_background=False, borders_innerH=False,
				   borders_outerH=False, borders_innerV=False,
				   borders_outerV=False) as cfg_table:
		dpg.add_table_column(label='Пн', tag='MonWD', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Вт', tag='TueWD', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Ср', tag='WedWD', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Чт', tag='ThuWD', init_width_or_weight=33, width_fixed=True)
		dpg.add_table_column(label='Пт', tag='FriWD', init_width_or_weight=33, width_fixed=True)
		
		with dpg.table_row(tag= "workDaysRow"):
			dpg.add_checkbox(tag=f'MonWDcb', callback=WDcb_callback, user_data=current_client)
			dpg.add_checkbox(tag=f'TueWDcb', callback=WDcb_callback, user_data=current_client)
			dpg.add_checkbox(tag=f'WedWDcb', callback=WDcb_callback, user_data=current_client)
			dpg.add_checkbox(tag=f'ThuWDcb', callback=WDcb_callback, user_data=current_client)
			dpg.add_checkbox(tag=f'FriWDcb', callback=WDcb_callback, user_data=current_client)
	
	update_WDcb(current_client["value"])
		
	pass

# dpg.add_button(label='Apply', callback=printPos, user_data = df)

with dpg.handler_registry():
	dpg.add_key_down_handler(key=dpg.mvKey_F1, callback=lambda: dpg.configure_item("GeneratorConfig", show=True))
	dpg.add_key_down_handler(key=dpg.mvKey_F2, callback=lambda: dpg.configure_item("Options", show=True))
	dpg.add_key_down_handler(key=dpg.mvKey_Escape, callback=lambda: dpg.configure_item("GeneratorConfig", show=False))
	dpg.add_key_down_handler(key=dpg.mvKey_Escape, callback=lambda: dpg.configure_item("Options", show=False))

with dpg.window(label='Row Example', tag='Primary Window') as window:
	df_table(df, True)
	dpg.add_button(label="Open Window", callback=lambda: dpg.configure_item("GeneratorConfig", show=True))
	
	for index, day in df.Date.items():
		if isBday(day):
			dpg.bind_item_theme(str(index), weekday_themes[day.weekday()])
		else:
			dpg.configure_item(str(index), enabled=False, show=False)

# dpg.show_item_registry()
dpg.create_viewport(x_pos=480, y_pos=300, width=960, height=540)
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window", True)
dpg.show_viewport()
# dpg.maximize_viewport()
#
# result = "Active" | organised_child_data() | checkbox_states() | mask_notempty(df)
# print(result)

dpg.start_dearpygui()
dpg.destroy_context()
