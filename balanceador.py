import apirequests

rank_index = {
    "IRON": 0,
    "BRONZE": 5,
    "SILVER": 10,
    "GOLD": 15,
    "PLATINUM": 20,
    "EMERALD": 25,
    "DIAMOND": 30
}

division_index = {
    "IV": 1,
    "III": 2,
    "II": 3,
    "I": 4
}

class Player:
    def __init__(self, name, tag="#BR1"):
        self.name = name
        self.tag = tag
        self.puuid = None
        self.summoner_id = None
        self.flex_rank = None
        self.soloduo_rank = None
        self.KDA = 0.0
        self.winrate = 0.0
        self.player_score = None
        self.populate_attributes()

    def process_match_stats(self):
        match_count = 100
        matches = apirequests.get_matches_for_player(self.puuid)
        
        average_kda = 0
        wins = 0
        for match in matches:
            match_stats = apirequests.get_match_stats(match, self.puuid)
            if match_stats["match_win"]:
                wins += 1
            k = match_stats["kills"]
            d = match_stats["death"]
            a = match_stats["assists"]

            average_kda += (k + a) / d
        
        wins = wins / match_count
        average_kda = average_kda / match_count

        return (average_kda, wins)

    def player_score(self):
        pass
    def populate_attributes(self):
        player_info = apirequests.get_account_info(self.name, self.tag)
        self.puuid = player_info["puuid"]
        self.summoner_id = player_info["id"]

        player_rank = apirequests.get_rank(self.summoner_id)
        
        self.flex_rank = rank_index[player_rank["flex"]["rank"]] + division_index[player_rank["flex"]["division"]]
        self.soloduo_rank = rank_index[player_rank["soloduo"]["rank"]] + division_index[player_rank["soloduo"]["division"]]

        self.KDA, self.winrate = self.process_match_stats()



        