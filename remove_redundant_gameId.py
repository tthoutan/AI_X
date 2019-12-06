import csv
import pandas as pd

DIVISION_LIST = ["I","II","III","IV"]

gameId_list = list()

for division in DIVISION_LIST:
	
	page_num = 1

	while True:

		try:

			file_name = f"SILVER_{division}_{page_num}_gameId.csv"
			fi = open(file_name, 'r', encoding='utf-8')
			fi_reader = csv.reader(fi)

		except FileNotFoundError:
			break

		temp_list = list()

		for line in fi_reader:
			temp_list.append(line[1])

		fi.close()

		gameId_list.extend(temp_list)

		page_num+=1

gameId_list = list(set(gameId_list))
print(len(gameId_list))

data = pd.DataFrame(gameId_list)
data.columns = ['gameId']
data.to_csv(f'All_gameId.csv')


		

fi.close()
