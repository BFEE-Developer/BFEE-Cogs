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
        self.isnight = False
        self.dayeventshappened = 0
        self.daytotalevents = 0
        self.nighteventshappened = 0
        self.nighttotalevents = 0
        
        # Randomize playerlist
        self.rawplayerlist = random.shuffle(playerlist)
        
        for p in playerlist:
            add_player(p)
        self.total_players_alive = len(playerlist)
        
    def stepDay(self):
        # Check to see if we have a winner.
        if self.total_players_alive is 1:
            self.game_active = False
            for p in self.players.values():
                if p.alive is True:
                    return {'w': p}
        
        # Check to see if everyone is dead..
        if self.total_players_alive is 0:
            self.game_active = False
            return {'ad': True}
            
        messages = []
        for p in self.players_dead_today:
            messages.append("☠️ {0} | District {1}".format(p, p.district))
            
        # Reset players dead count day.
        self.players_dead_today = []
        
        if len(messages) == 0:
            messages.append("Today was a good day for all, nobody died")
                    
        summary = {
            'title': "The sun rises over the horizon as we venture into day {0}".format(self.day),
            'messages': messages,
            'footer': "BFEE champions remaining: {0}/{1}".format(self.total_players_alive, len(self.players))
        }
        
        self.totalevents = randint(1, 5)
        self.eventshappened = 0
        
        return summary
    
    def stepNight():
        summary = {
            'title': "Night",
            'messages': "Night",
            'footer': "BFEE champions remaining: {0}/{1}".format(self.total_players_alive, len(self.players))
        }
        return
        
    def step(self)
        # Check to se if total number of events happened.
        # If total number of events happened, progres Day > Night, Night > Day
        if self.isnight:
            if self.nighteventshappened == self.nighttotalevents:
                return stepDay()
            else:
                # Commit night event.
        else:
            if self.dayeventshappened == self.daytotalevents:
                return stepNight()
            else:
                # Commit day event.


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