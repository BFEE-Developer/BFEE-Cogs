import random
import math

from player import Player


class Game:

    game_active = False
    districts = 0

    def new_game(self, channel_id, owner_id, owner_name, title):
        if game_active:
            return False
        game_active = True
        return True
        
    def start_game(self, channel_id, member_id, prefix, playerlist):
        self.players = {}
        self.players_available_to_act = set()
        self.players_dead_today = []
        self.total_players_alive = 0
        self.day = 1
        # Randomize playerlist
        self.rawplayerlist = random.shuffle(playerlist)
        
        for p in playerlist:
            add_player(p)

    def add_player(self, new_player):
        if new_player.name in self.players:
            return False
        district = _whichDistrict()
        p = Player(new_player.name, district)
        self.players[new_player.name] = p
        return True
        
    def _whichDistrict():
        global districts
        if len(self.players) > (districts * 4):
            districts = districts + 1
        return districts