import requests
import json


api_key = ""


def get_account_info(name, tag="BR1"):
    headers = {
        "X-Riot-Token": api_key
    }
    request = requests.get(f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}", headers=headers)

    if request.status_code == 200:
        response = request.json()
        summoner_request = requests.get(f"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{response['puuid']}", headers=headers)

        if summoner_request.status_code == 200:
            summoner_request_dict = summoner_request.json()

            for key in summoner_request_dict.keys():
                if key not in response:
                    response[key] = summoner_request_dict[key]

            return response
        else:
            return summoner_request.json()
        
    else:
        request.json()



def get_rank(summoner_id):
    headers = {
        "X-Riot-Token": api_key
    }
    request = requests.get(f"https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}", headers=headers)

    if request.status_code == 200:
        response = request.json()

        player_ranks = {
            "flex": {
                "rank": response[0]["tier"],
                "division": response[0]["rank"]
            },
            "soloduo": {
                "rank": response[1]["tier"],
                "division": response[0]["rank"]
            }
        }

        return player_ranks
    else:
        return None

def get_matches_for_player(puuid, amount=50):

    headers = {
        "X-Riot-Token": api_key
    }

    matches = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={amount}", headers=headers)

    if matches.status_code == 200:
        return matches.json()
    else:
        return None
    
def get_match_stats(match_id, puuid):
    headers = {
        "X-Riot-Token": api_key
    }

    match = requests.get(f"https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}", headers=headers)

    if match.status_code == 200:
        participants = match["metadata"]["participants"]
        player_match_index = participants.index(puuid)

        player_stats = match["info"]["participants"][player_match_index]

        kills = player_stats["kills"]
        deaths = player_stats["deaths"]
        assists = player_stats["assists"]
        kda = (kills + assists) / deaths
        won_match = True if player_stats["win"] == "true" else False

        player_stats_dict = {
            "match_win": won_match,
            "kills": kills,
            "deaths": deaths,
            "assists": assists
        }

        return player_stats_dict
    else:
        return None


    

res = get_matches_for_player("mijodebosta", "HOFF")

print(res) if res is not None else print(-1)
    

    

    