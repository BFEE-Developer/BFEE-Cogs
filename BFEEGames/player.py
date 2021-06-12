class Player:
     def __init__(self, name, district):
        self.name = name
        self.district = district
        self.alive = True
        self.kills = 0
        self.cause_of_death = ""