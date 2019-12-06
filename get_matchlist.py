import time
import requests
import pandas as pd

header = {"X-Riot-Token":"RGAPI-60bd1475-e03f-43ea-b7f7-2ceaa6ee116f"}
default_url = "https://kr.api.riotgames.com"
QUEUE = "RANKED_SOLO_5x5"
TIER = "SILVER"
DIVISON_LIST = ["IV"]
start_time = "1574203380000" # 11월 20일 오전 07:43 pre_season 9.23 패치 적용 후 점검완료 시간


# 전달받은 summoner_id에 대응하는 encrypted_accountid를 리턴해줌

def get_aid(summoner_id):
    
    path = "/lol/summoner/v4/summoners/"

    # encoded_url = default_url + parse.quote(path)

    total_url = default_url + path + summoner_id

    response = requests.get(total_url, headers=header)

    while response.status_code == 429:
    	print("aid sleep")
    	time.sleep(5)
    	response = requests.get(total_url, headers=header)
    
    return response.json()['accountId']


# 각 페이지 마다 소환사의 AccountId 리스트 리턴, 만약 페이지의 끝일 경우 None 리턴

def get_summoner_list(queue_type, tier, division, page_number):

	path = f"/lol/league/v4/entries/{queue_type}/{tier}/{division}/?page={page_number}"

	summoner_aid_list = list()

	total_url = default_url + path

	response = requests.get(total_url, headers=header)

	while response.status_code == 429:
		print("summoner sleep")
		time.sleep(5)
		response = requests.get(total_url, headers=header)

	response_list = response.json()

	if len(response_list) == 0:
		return None

	for a in response_list:
		summoner_aid_list.append(get_aid(a['summonerId']))

	return summoner_aid_list

def get_match_list():

	path = "/lol/match/v4/matchlists/by-account/"

	match_list = list()

	for division in DIVISON_LIST:
		page_num = 1
		while True:
			print(page_num)
			aid_list = get_summoner_list(QUEUE, TIER, division, page_num)
			print("get_summoner_list pass")
			if aid_list is None:
				break

			for aid in aid_list:
				begin_idx = 0
				print(begin_idx)
				while True:
					total_url = default_url + path + aid + "?beginTime=" + start_time + "&beginIndex=" + str(begin_idx)

					response = requests.get(total_url, headers=header)

					while response.status_code == 429:
						print("match list sleep")
						time.sleep(5)
						response = requests.get(total_url, headers=header)

					response_list = response.json()
					matches = response_list.get('matches', list())

					if len(matches) == 0:
						break

					for match in matches:
						match_list.append(match['gameId'])

					begin_idx = response_list['endIndex']

			

			match_list = list(set(match_list))

			data = pd.DataFrame(match_list)
			data.columns = ['gameId']
			data.to_csv(f'{TIER}_{division}_{page_num}_gameId.csv')

			page_num+=1
			if page_num > 20:
				break
			match_list=list()

	


if __name__ == '__main__':
	get_match_list()


