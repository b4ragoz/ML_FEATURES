import json


with open('bileti.json', 'r', encoding='windows-1251') as f:
	txt = json.load(f)

print(txt['Задача регрессии'])