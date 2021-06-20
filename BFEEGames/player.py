class Player:
    def __init__(self, name, id, district, ava):
        self.name = name
        self.id = id
        self.district = district
        self.avatar = ava
        self.alive = True
        self.kills = 0
        self.cause_of_death = ""
        
    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name and self.district == other.district
        return False

    def __ne__(self, other):
        return self.name != other.name or self.district != other.district

    def __lt__(self, other):
        return (self.district, self.name) < (other.district, other.name)

    def __le__(self, other):
        return (self.district, self.name) <= (other.district, other.name)

    def __gt__(self, other):
        return (self.district, self.name) > (other.district, other.name)

    def __ge__(self, other):
        return (self.district, self.name) >= (other.district, other.name)

    def __hash__(self):
        return hash((self.district, self.name))