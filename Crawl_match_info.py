import requests
import pandas as pd
import csv
import time
import argparse

#[1]RGAPI-60bd1475-e03f-43ea-b7f7-2ceaa6ee116f
#[2]RGAPI-3c44417e-8ca0-4471-9b1b-09a1841cb4c8
#[3]RGAPI-5e43b909-75f1-4b04-a456-4988e4ad44a5
#[4]RGAPI-0e4c5546-ecbd-4b9e-8748-06f20c400b38

ap = argparse.ArgumentParser()
ap.add_argument("-k","--key", required=True, help="You shoud insert Riot API Key")
ap.add_argument("-n","--num", required=True, help="You shoud insert the number of partition")
args = vars(ap.parse_args())

print(args)

header = {"X-Riot-Token":f"{args['key']}"}
number = args['num']
default_url = "https://kr.api.riotgames.com"

# response['gameMode'] == "CLASSIC"
# response['participants'] is 10 length list -> response['participants'][n]['teamId'], response['participants'][n]['championId']
# response['teams'][0]['win'] == Win or Fail, response['teams'][0]['teamId'] == 100 or 200

def get_match_info():
	
	path = "/lol/match/v4/matches/"

	fi = open(f"gameId_split_{number}.csv", 'r', encoding='utf-8')
	fi_reader = csv.reader(fi)

	line_count = 0
	result_list = list()
	file_num = 1
	row_count = 0

	for line in fi_reader:
		if line[1]=='gameId':
			continue
		row_count += 1

		total_url = default_url + path + line[1]
		response = requests.get(total_url, headers=header)
			
		while response.status_code == 429:
			print("info_sleep")
			time.sleep(5)
			response = requests.get(total_url, headers=header)

		response_list = response.json()
		a = response_list.get('gameMode')
		if a != "CLASSIC":
			continue
		else:
			win_list = list()
			fail_list = list()
			if response_list['teams'][0]['win'] == 'Win':
				for i in range(0,5):
					win_list.append(response_list['participants'][i]['championId'])
				win_list.append(1)
				for i in range(5,10):
					fail_list.append(response_list['participants'][i]['championId'])
				fail_list.append(0)
			else:
				for i in range(0,5):
					fail_list.append(response_list['participants'][i]['championId'])
				fail_list.append(0)
				for i in range(5,10):
					win_list.append(response_list['participants'][i]['championId'])
				win_list.append(1)

			result_list.append(win_list)
			result_list.append(fail_list)
			line_count+=2

			if line_count == 2000 or row_count==30000:
				print(f"{file_num}th file completed")
				data = pd.DataFrame(result_list)
				data.columns = ['champ1','champ2','champ3','champ4','champ5','win']
				data.to_csv(f'match_info_{file_num}.csv')
				line_count = 0
				file_num+=1

			print(row_count)



if __name__ == "__main__":
	get_match_info()