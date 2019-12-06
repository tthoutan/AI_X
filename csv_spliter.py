import csv
import pandas as pd

fi = open(f"All_gameId.csv", 'r', encoding='utf-8')
fi_reader = csv.reader(fi)

line_count = 0
number = 1
temp_list = list()
for line in fi_reader:
	
	if line[1] == "gameId":
		continue

	temp_list.append(line[1])
	line_count+=1

	if line_count == 30000:
		line_count = 0
		data = pd.DataFrame(temp_list)
		data.columns = ['gameId']
		data.to_csv(f"gameId_split_{number}.csv")
		number+=1
		temp_list = list()

