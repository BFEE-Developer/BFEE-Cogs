import random
import math
import json
from redbot.core.data_manager import cog_data_path, bundled_data_path

class Game:
    def __init__(self, owner_name, owner_id):
        self.owner_name = owner_name
        self.owner_id = owner_id
        self.title = "BFEE Hunger Games"
        self.has_started = False

        # Player data
        self.players = {}
        self.players_available_to_act = set()
        self.players_dead_today = []
        self.total_players_alive = 0

        # Round counting
        self.day = 1
        self.days_since_last_event = 0
        self.consecutive_rounds_without_deaths = 0

        # Round order control
        self.bloodbath_passed = False
        self.day_passed = False
        self.fallen_passed = False
        self.night_passed = False
        
        #See if there is a custom events json file.
        print("Path 1: {0}".format(cog_data_path(None,"BFEEGames")))
        print("Path 2: {0}".format(bundled_data_path(self)))
        if not (cog_data_path(None,"BFEEGames") / "events.json").is_file():
            print("No custom event file")
            self.eventsfile = bundled_data_path(self) / "default_events.json"
        else:
            self.eventsfile = cog_data_path(None,"BFEEGames") / "events.json"
            print("Got custom event file")
            
        with self.eventsfile.open() as json_data:
            self.events = json.load(json_data)
        
    def add_player(self, new_player):
        if new_player.name in self.players:
            return False
        self.players[new_player.name] = new_player
        return True
    
    def start(self):
        self.total_players_alive = len(self.players)
        self.has_started = True
        
    def step(self):
        if self.total_players_alive is 1:
            self.has_started = False
            for p in self.players.values():
                if p.alive is True:
                    return {'winner': p.name, 'district': p.district}
                
        if self.total_players_alive is 0:
            self.has_started = False
            return {'allDead': True}

        if self.night_passed:
            self.day += 1
            self.days_since_last_event += 1
            self.day_passed = False
            self.fallen_passed = False
            self.night_passed = False

        fatality_factor = random.randint(2, 4) + self.consecutive_rounds_without_deaths
        
        self.players_available_to_act = {p for p in self.players.values() if p.alive is True}

        if self.day is 1 and not self.bloodbath_passed:
            step_type = "bloodbath"
            fatality_factor += 2
            self.bloodbath_passed = True
        elif not self.day_passed:
            step_type = "day"
            self.day_passed = True
        elif self.day_passed and not self.fallen_passed:
            step_type = "fallen"
            self.fallen_passed = True
        else:
            step_type = "night"
            self.night_passed = True

        

        event = None
        if step_type is "fallen":
            messages = []
            for p in self.players_dead_today:
                messages.append("☠️ {0} | District {1}".format(p, p.district))
        else:
            messages = []
            event = self.events[step_type]
            dead_players_now = len(self.players) - self.total_players_alive
            #messages.append(self.__generate_messages(fatality_factor, event))
            messages = self.__generate_messages(fatality_factor, event)
            if len(self.players) - self.total_players_alive == dead_players_now:
                self.consecutive_rounds_without_deaths += 1
            else:
                self.consecutive_rounds_without_deaths = 0

        summary = {
            'day': self.day,
            'roundType': step_type,
            'messages': messages,
            'footer': "Tributes Remaining: {0}/{1} | Host: {2}"
                      .format(self.total_players_alive, len(self.players), self.owner_name)
        }

        if step_type is "fallen":
            summary['title'] = "{0} | {1}".format(self.title, "Fallen Tributes {0}".format(self.day))
            if len(self.players_dead_today) > 1:
                summary['description'] = "{0} cannon shots can be heard in the distance.".format(
                    len(self.players_dead_today))
                self.players_dead_today.clear()
            elif len(self.players_dead_today) is 1:
                summary['description'] = "1 cannon shot can be heard in the distance."
                self.players_dead_today.clear()
            else:
                summary['description'] = "No cannon shots are heard."
            summary['color'] = 0xaaaaaa
        else:
            summary['title'] = "{0} | {1}".format("BFEE Hunger Games", "{0} {1}".format(step_type, self.day))
            summary['description'] = None #event['description']
            summary['color'] = 0xf9eb0f #event['color']

        return summary
        
    def __generate_messages(self, fatality_factor, event):
        messages = []##
        while len(self.players_available_to_act) > 0:
            msg = ""
            isChosen = False
            while not isChosen:
                tributes = random.randint(1, len(self.players_available_to_act))
                f = random.randint(0, 10)
                ev_type = None
                if f < fatality_factor and self.total_players_alive > 1:
                    ev_type = "death"
                else:
                    ev_type = "fun"
                
                try:
                    action = event[ev_type][str(tributes)]
                except KeyError:
                    continue
                if len(action) > 0:
                    isChosen = True
                
            action = random.choice(action)

            players_acted = 0
            active_players = []
            avatars = []
            
            while players_acted < tributes:
                p = random.choice(tuple(self.players_available_to_act))
                self.players_available_to_act.remove(p)
                active_players.append(p)
                players_acted += 1
                avatars.append(p.avatar)
                
            if ev_type is "death":
                #print("{0} - {1} | {2}".format(ev_type, action["msg"], len(active_players)))
                msg = action['msg'].format(*["|>>>|{0}".format(str(i).replace(" ","|--|--|--|")) for i in active_players])
                if action.get('killed') is not None:
                    if action.get('killer') is not None:
                        for kr in action['killer']:
                            active_players[kr].kills += len(action['killed'])
                    for kd in action['killed']:
                        active_players[kd].alive = False
                        self.players_dead_today.append(active_players[kd])
                        self.total_players_alive -= 1
                        active_players[kd].cause_of_death = msg
            else:
                msg = action.format(*["|>>>|{0}".format(str(i).replace(" ","|--|--|--|")) for i in active_players])
                
            ret = {"message": msg, "avatars": avatars}
            messages.append(ret)##
        return messages##
        return ret
        
    def __generate_messagesBACKUP(self, fatality_factor, event):
        messages = []
        while len(self.players_available_to_act) > 0:
            isChosen = False
            while not isChosen:
                tributes = random.randint(1, len(self.players_available_to_act))
                f = random.randint(0, 10)
                ev_type = None
                if f < fatality_factor and self.total_players_alive > 1:
                    ev_type = "death"
                else:
                    ev_type = "fun"
                
                try:
                    action = event[ev_type][tributes]
                except KeyError:
                    continue
                    
                isChosen = True
            action = random.choice(action)

            players_acted = 0
            active_players = []
            
            while players_acted < tributes:
                p = random.choice(tuple(self.players_available_to_act))
                self.players_available_to_act.remove(p)
                active_players.append(p)
                players_acted += 1

            if ev_type is "death":
                msg = action['msg'].format(*active_players)
                if action.get('killed') is not None:
                    if action.get('killer') is not None:
                        for kr in action['killer']:
                            active_players[kr].kills += len(action['killed'])
                    for kd in action['killed']:
                        active_players[kd].alive = False
                        self.players_dead_today.append(active_players[kd])
                        self.total_players_alive -= 1
                        active_players[kd].cause_of_death = msg
            else:
                msg = action.format(*active_players)
 
            messages.append(msg)
        return messages
        
    @property
    def players_sorted(self):
        l = list(self.players.values())
        l.sort()
        return l