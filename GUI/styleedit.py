import dearpygui.dearpygui as dpg
from EditThemePlugin import EditThemePlugin

dpg.create_context()
dpg.create_viewport(title="some title", width=1000, height=1000)
with dpg.viewport_menu_bar():
	with dpg.menu():
		dpg.add_menu_item(label="Show Metrics", callback=lambda: dpg.show_tool(dpg.mvTool_Metrics))
	EditThemePlugin()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
exit()