import discord
import random
import math
from typing import Optional, Union
from .game import Game
from .player import Player

class GameFramework:
    active_games = {}
    cur_summary = {}

    def new_game(self, channel_id, owner_id, owner_name):
        if channel_id in self.active_games:
            this_game = self.active_games[channel_id]
            return {"status": "GAMESTARTED", "owner": this_game.owner_id}
        print("---------------------------")
        self.active_games[channel_id] = Game(owner_name, owner_id)
        return {"status": "GAMESTART", "owner": owner_id}
        #return True

    async def add_player(self, channel_id, imagep, user: discord.User = None):
        if channel_id not in self.active_games:
            return {"status": "NOGAME"}
        this_game = self.active_games[channel_id]

        if this_game.has_started:
            return {"status": "GAMESTARTED"}
        if len(this_game.players) >= 24:
            return {"status": "GAMEFULL"}

        district = math.ceil((len(this_game.players) + 1) / 2)
        
        p = Player(user.name, user.id, district, imagep)
        if not this_game.add_player(p):
            return {"status": "PLAYEREXIST"}
        return "**District {0} | {1}** is selected to be a tribute!".format(p.district, p.name)

    def status(self, channel_id):
        if channel_id not in self.active_games:
            return {"status": "NOGAME"}
        this_game = self.active_games[channel_id]

        player_list = []
        for p in this_game.players_sorted:
            gender_symbol = "♂" if p.is_male else "♀"
            if p.alive:
                player_list.append("District {0} {1} | {2}".format(p.district, gender_symbol, p.name))
            else:
                player_list.append("~~District {0} {1} | {2}~~".format(p.district, gender_symbol, p.name))

        summary = {
            'title': this_game.title,
            'footer': "Players: {0}/24 | Host: {1}"
                      .format(len(this_game.players), this_game.owner_name)
        }

        if len(player_list) == 0:
            summary['description'] = "No players have joined yet"
        else:
            summary['description'] = "The following tributes are currently in the game:\n\n" + "\n".join(player_list)
        return summary

    def start_game(self, channel_id, member_id):
        if channel_id not in self.active_games:
            return {"status": "NOGAME" }
        this_game = self.active_games[channel_id]

        if member_id != this_game.owner_id:
            return {"status": "NOTOWNER" }
        if this_game.has_started:
            return {"status": "GAMEALREADYSTARTED" }
        if len(this_game.players) < 2:
            return {"status": "NOTENOUGHPLAYERS" }

        this_game.start()
        player_list = []
        for p in this_game.players_sorted:
            player_list.append("District {0} | {1}".format(p.district, p.name))

        return {'title': "{0} | The Reaping".format(this_game.title),
                'footer': "Total Players: {0} | Owner {1}".format(len(this_game.players), this_game.owner_name),
                'description': "The Reaping has concluded! Here are the tributes:\n\n{0}\n\n{1}, you may now "
                               "proceed the simulation with `!step`.".format("\n".join(player_list),
                                                                               this_game.owner_name)}

    def end_game(self, channel_id, owner_id):
        if channel_id not in self.active_games:
            return {"status": "NOGAME"}
        this_game = self.active_games[channel_id]
        if owner_id != this_game.owner_id:
            return {"status": "NOTOWNER", "owner": this_game.owner_id}

        return self.active_games.pop(channel_id)

    def step(self, channel_id, member_id):
        # TODO: Let moderators also step
        # TODO: Allow for group skip override
        if channel_id not in self.active_games:
            return {"status": "NOGAME"}
        this_game = self.active_games[channel_id]

        if member_id != this_game.owner_id:
            return {"status": "NOTOWNER", "owner": this_game.owner_id}
        if not this_game.has_started:
            return {"status": "NOGAME"}

        if self.cur_summary.get('messages') is None:
            self.cur_summary["messages"] = []

        if len(self.cur_summary["messages"]) == 0:
            summary = this_game.step()
            self.cur_summary = summary

            if summary.get('winner') is not None:
                self.active_games.pop(channel_id)
                return {
                    'title': "{0} | Winner".format(this_game.title),
                    'color': 0xd0d645,
                    'description': "The winner is {0} from District {1}!".format(summary['winner'], summary['district']),
                    'footer': None
                }
            
            if summary.get('allDead') is not None:
                self.active_games.pop(channel_id)
                return {
                    'title': "{0} | Winner".format(this_game.title),
                    'color': 0xd0d645,
                    'description': "All the contestants have died!",
                    'footer': None
                }
        else:
            summary = self.cur_summary

        if summary['description'] is not None and len(summary['messages']) > 0:
            # Cannon
            formatted_msg = "{0}\n\n> {1}".format(summary['description'], "\n> ".join(summary['messages']))
            avat = None
            summary['messages'] = []
        elif summary['description'] is not None:
            formatted_msg = summary['description']
            avat = None
        else:
            #formatted_msg = "> {0}".format("\n> ".join(summary['messages']))
            #formatted_msg = "{0}".format(summary['messages'])
            f_msg = summary['messages'].pop()
            formatted_msg = "{0}".format(f_msg["message"])
            avat = f_msg["avatars"]
            

        return {
            'day': summary["day"],
            'title': summary['title'],
            'color': summary['color'],
            'description': formatted_msg,
            'avatars': avat,
            'footer': summary['footer']
        }