# AI_X tech blog
***

# Project Title : naïve bayes classifier를 이용하여 게임 ‘리그 오브 레전드’의 아군 챔피언(캐릭터) 선택에 따른 챔피언 추천 

***

## Members
* 박철우, 정보시스템학과
* 이윤지, 수학과
* 이동한, 수학과
* 이제환, 수학과

***

## Table of Contents
* [1.Introduction](#chapter-1)
* [2.DataSets](#chapter-2)
* [3.Methodology](#chapter-3)
* [4.Evaluate & Analysis](#chapter-4)
* [5.Related Work](#chapter-5)
* [6.Conclusion](#chapter-6)

***

<a id="chapter-1"></a>
### 1.Introduction
‘리그 오브 레전드’는 미국의 라이엇 게임즈가 개발 및 서비스 중인 MOBA(Multiplayer Online Battle Arena)장르의 게임으로, 현재 전세계적으로 가장 인기 있는 PC 온라인 게임 중 하나이다. ‘리그 오브 레전드’ 에서는 비슷한 점수대의 유저들이 선호 포지션에 따른 Random으로 선택된 10명의 유저들이 5vs5로 대전하는 게임이며, 각각의 유저들은 게임에서 사용할 챔피언(캐릭터)를 선택한다. 선택할 수 있는 챔피언은 총 145개가 존재하며 각각의 챔피언은 모두 서로 다른 능력치와 스킬을 가지기 때문에 어떤 챔피언을 고르는 지에 따라 게임의 승패에 큰 영향을 미치게 된다. 또한 챔피언들은 같은 팀으로 선택되었을 때 서로가 가진 특징에 따라 상승효과를 불러 일으키는 경우가 많기 때문에 챔피언을 고를 때에는 아군 혹은 적군이 어떤 챔피언을 고르는지도 챔피언 선택의 중요한 근거가 될 수 있다. 우리는 naïve bayes classifier를 이용하여 다른 아군 4명이 챔피언을 골랐을 때 어떤 챔피언을 고르는 것이 승률이 높을 것인지를 근거로 선택할 챔피언을 추천하고자 한다.

***
<a id="chapter-2"></a>
### 2.DataSets
‘리그 오브 레전드’에서는 자체 API를 통해 게임 플레이 데이터를 제공하고 있다. https://developer.riotgames.com/ 사이트를 통해 API 사용 신청하여 승인을 받았고, 이를 통해 naïve bayes classifier (혹은 다른 알고리즘)를 수행하는 데 충분한 데이터를 얻을 수 있다.

데이터 수집 방법 : ‘리그 오브 레전드’에서는 자체 API를 통해 게임 플레이 데이터를 제공하고 있다. https://developer.riotgames.com/ 사이트를 통해 API 사용 신청하여 승인을 받았고, 이를 통해 naïve bayes classifier (혹은 다른 알고리즘)를 수행하는 데 충분한 데이터를 얻을 수 있다.

데이터를 수집하는 자세한 방법에 대해서 설명하겠다.

1. 먼저 데이터 수집을 원하는 기간에 해당하는 게임의 데이터를 수집하기 위해 각 게임의 gameId를 수집할 필요가 있다.
다음의 파이썬 스크립트는 SOLO RANK SILVER 티어에서의 4개의 각 DIVISON에 대해 9.23 패치가 적용되고 나서부터의 gameId를 RIOT API로 받아와서 라이엇에서 자체적으로 분류한 page 단위에 따라 csv 파일로 저장하는 스크립트이다.

```python

import time
import requests
import pandas as pd

header = {"X-Riot-Token":"Your API Token Key"} # Riot Developers Page에서 Development API Key를 발급 받을 수 있다.
default_url = "https://kr.api.riotgames.com"
QUEUE = "RANKED_SOLO_5x5"
TIER = "SILVER"
DIVISON_LIST = ["I","II","III","IV"]
start_time = "1574203380000" # 11월 20일 오전 07:43 pre_season 9.23 패치 적용 후 점검완료 시간

# 각 Player의 Match List를 조회하기 위해서는, SummonerId가 아닌 AccountId가 필요한데, SummonerId를 통해 AccountId를 알 수 있다.
# 그리고 이 get_aid 함수는 summoner_id를 인자로 받아 AccountId를 return 해주는 함수이다.

def get_aid(summoner_id):
    
    path = "/lol/summoner/v4/summoners/"

    total_url = default_url + path + summoner_id

    response = requests.get(total_url, headers=header)

    while response.status_code == 429:
    	print("aid sleep")
    	time.sleep(5)
    	response = requests.get(total_url, headers=header)
    
    return response.json()['accountId']


# queue_type(여기서는 RANKED_SOLO_5x5)과 tier(여기서는 SILVER), division(각 티어마다 I,II,III,IV가 존재함), page number를 인자로 받는다.
# 주어진 인자의 조건에 알맞는 Player 들의 정보를 조회하는 API를 이용해 정보를 조회한 뒤, 그곳에서 SummonerId 값을 뽑아 get_aid 함수를 호출해
# 최종적으로 Player 들의 AccountId로 이루어진 List를 만들어서 반환한다.

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


# get_summoner_list 함수 호출을 통해 반환받은 AccountId List를 이용해 각 Player의 Match List를 조회하고 각 Match의 gameId를 뽑아 List를 만든다. 그 뒤 각 page number 마다의 List를 csv 파일로 저장한다.

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
			
			# 만들어진 해당 페이지의 gameId 리스트를 csv로 export 하는 부분.
			data = pd.DataFrame(match_list)
			data.columns = ['gameId']
			data.to_csv(f'{TIER}_{division}_{page_num}_gameId.csv')

			# page의 수가 너무 많아서 적당한 수준의 데이터의 양을 각 디비전마다 가져오기 위해 page의 개수를 20개로 제한했다.
			page_num+=1
			if page_num > 20:
				break
			match_list=list()
```

2. 다음으로는 각 Player들의 gameId를 수집한 것이고 '리그 오브 레전드'는 5vs5 팀게임이기 때문에, 수집된 gameId의 리스트에 중복되는 값이 많이 있을 가능성이 
존재한다. 따라서 



***
<a id="chapter-3"></a>
### 3.Methodology

naïve bayes classifier 소개 : naïve bayes classifier는 조건부 확률에 대한 bayes theorem에 기반한 것으로 조건부 확률 P(C_i│x_1,⋯x_p )를 계산하게 되며 C_i는 해당 레코드가 속하게 되는 클래스,즉 이 문제에서는 승리 혹은 패배가 되며, 범주형 예측 변수인 x_1,⋯x_p는 아군 5명 각각이 선택한 챔피언이 된다.

***
<a id="chapter-4"></a>
### 4.Evaluation & Analysis

...준비중...

***
<a id="chapter-5"></a>
### 5.Related Work

...준비중...

***
<a id="chapter-6"></a>
### 6. Conclusion

...준비중...
