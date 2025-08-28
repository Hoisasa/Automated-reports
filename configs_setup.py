from configparser import ConfigParser


def default_weekdays(num: int, group: str):
	config[f"Weekdays:{num}"] = {}
	if group == "IV:low":
		config[f"Weekdays:{num}"]["Mon"] = "False"
		config[f"Weekdays:{num}"]["Tue"] = "True"
		config[f"Weekdays:{num}"]["Wed"] = "False"
		config[f"Weekdays:{num}"]["Thu"] = "True"
		config[f"Weekdays:{num}"]["Fri"] = "False"
	elif group == "IV:high":
		config[f"Weekdays:{num}"]["Mon"] = "True"
		config[f"Weekdays:{num}"]["Tue"] = "False"
		config[f"Weekdays:{num}"]["Wed"] = "True"
		config[f"Weekdays:{num}"]["Thu"] = "False"
		config[f"Weekdays:{num}"]["Fri"] = "True"
	elif group == "V:high":
		config[f"Weekdays:{num}"]["Mon"] = "True"
		config[f"Weekdays:{num}"]["Tue"] = "True"
		config[f"Weekdays:{num}"]["Wed"] = "True"
		config[f"Weekdays:{num}"]["Thu"] = "True"
		config[f"Weekdays:{num}"]["Fri"] = "True"
		
config = ConfigParser()

clientsBase = {
	"Андрущенко" : "IV:high",
	"Далінчук" : "V:high",
	"Жельніо" : "IV:low",
	"Карпенко" : "IV:high",
	"Лемешко Е" : "IV:low",
	"Лемешко Л" : "IV:low",
	"Мозгова Н" : "IV:low",
	"Мозговий М" : "IV:low",
	"Сотнікова" : "IV:high",
	"Тиха" : "IV:high",
}
for num, (client, group) in enumerate(clientsBase.items()):
	config[f"Client:{num}"] = {}
	config[f"Client:{num}"]["Name"] = client
	config[f"Client:{num}"]["Group"] = group
	
	default_weekdays(num, group)
	

		
with open("configs/clientsbase.ini", "w", encoding="utf-8") as f:
	config.write(f)
