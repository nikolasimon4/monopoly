"""
Monopoly Implementation
"""
from typing import List, Tuple, Optional, Set, Callable, Dict
import random
import copy

"""
A png in the form images/image-name.png, used to pull an image from the images
directory with pygame
"""
imagetype = str

# Tile Base Class
class Tile():
    def __init__(self, name: str, pos: Tuple[int, int], image: imagetype):
        self.name = name
        self.pos = pos
        self.image = image



# Properties 

class Property(Tile):


    def __init__(self, name: str, pos: Tuple[int, int], image: str, 
        propnum: int, cost, r0: int, r1: int, r2: int, r3: int, r4: int, 
        rh: int, hp: int):

        super().__init__(name, pos, image)
        self.propnum = propnum

        self.price = cost
        self.rents = {}
        self.rents[0] = r0
        self.rents[1] = r1
        self.rents[2] = r2
        self.rents[3] = r3
        self.rents[4] = r4
        self.rents[5] = rh
        
        self.house_price = hp

        self.house = 0
        self.owner: Optional("Player") = None
        self.morgage_price = cost // 2
        self.morgaged = False
    
    def rent(self) -> int:
        return self.rents[self.house]
    def build_house(self) -> None:
        self.house += 1
    def remove_house(self) -> None:
        self.house -= 1

# Brown Properties
mediterranean_ave = Property("Mediterranean Avenue", (1, 1), 
                            "mediterranean_ave.png",
                            1, 60, 2, 10, 30, 90, 160, 250, 50)
baltic_ave = Property("Baltic Avenue", (1, 2), "baltic_ave.png",
                    2, 60, 4, 20, 60, 180, 320, 450, 50)

# Light Blue Properties
oriental_ave = Property("Oriental Avenue", (2, 1), "oriental_ave.png",
                        3, 100, 6, 30, 90, 270, 400, 550, 50)
vermont_ave = Property("Vermont Avenue", (2, 2), "vermont_ave.png",
                    4, 100, 6, 30, 90, 270, 400, 550, 50)
connecticut_ave = Property("Connecticut Avenue", (2, 3), 
                        "connecticut_ave.png",
                        5, 120, 8, 40, 100, 300, 450, 600, 50)

# Pink Properties
st_charles_place = Property("St. Charles Place", (3, 1), 
                            "st_charles_place.png",
                            6, 140, 10, 50, 150, 450, 625, 750, 100)
states_ave = Property("States Avenue", (3, 2), "states_ave.png",
                    7, 140, 10, 50, 150, 450, 625, 750, 100)
virginia_ave = Property("Virginia Avenue", (3, 3), "virginia_ave.png",
                        8, 160, 12, 60, 180, 500, 700, 900, 100)

# Orange Properties
st_james_place = Property("St. James Place", (4, 1), 
                        "st_james_place.png",
                        9, 180, 14, 70, 200, 550, 750, 950, 100)
tennessee_ave = Property("Tennessee Avenue", (4, 2), 
                        "tennessee_ave.png",
                        10, 180, 14, 70, 200, 550, 750, 950, 100)
new_york_ave = Property("New York Avenue", (4, 3), 
                        "new_york_ave.png",
                        11, 200, 16, 80, 220, 600, 800, 1000, 100)

# Red Properties
kentucky_ave = Property("Kentucky Avenue", (5, 1), "kentucky_ave.png",
                        12, 220, 18, 90, 250, 700, 875, 1050, 150)
indiana_ave = Property("Indiana Avenue", (5, 2), "indiana_ave.png",
                    13, 220, 18, 90, 250, 700, 875, 1050, 150)
illinois_ave = Property("Illinois Avenue", (5, 3), "illinois_ave.png",
                        14, 240, 20, 100, 300, 750, 925, 1100, 150)

# Yellow Properties
atlantic_ave = Property("Atlantic Avenue", (6, 1), "atlantic_ave.png",
                        15, 260, 22, 110, 330, 800, 975, 1150, 150)
ventnor_ave = Property("Ventnor Avenue", (6, 2), "ventnor_ave.png",
                    16, 260, 22, 110, 330, 800, 975, 1150, 150)
marvin_gardens = Property("Marvin Gardens", (6, 3), 
                        "marvin_gardens.png",
                        17, 280, 24, 120, 360, 850, 1025, 1200, 150)

# Green Properties
pacific_ave = Property("Pacific Avenue", (7, 1), "pacific_ave.png",
                    18, 300, 26, 130, 390, 900, 1100, 1275, 200)
north_carolina_ave = Property("North Carolina Avenue", (7, 2), 
                            "north_carolina_ave.png",
                            19, 300, 26, 130, 390, 900, 1100, 1275, 200)
pennsylvania_ave = Property("Pennsylvania Avenue", (7, 3), 
                            "pennsylvania_ave.png",
                            20, 320, 28, 150, 450, 1000, 1200, 1400, 200)

# Blue Properties
park_place = Property("Park Place", (8, 1), "park_place.png",
                    21, 350, 35, 175, 500, 1100, 1300, 1500, 200)
boardwalk = Property("Boardwalk", (8, 2), "boardwalk.png",
                    22, 400, 50, 200, 600, 1400, 1700, 2000, 200)

# Utilities

class Utility(Tile):
    def __init__(self, name: str, pos: Tuple[int, int], image: str,
        propnum: int):
        super().__init__(name, pos, image)
        self.price = 150
        self.propnum = propnum
        
        self.owner: Optional("Player") = None
        self.both = False
        self.morgage_price = 75
        self.morgaged = False

    def rent(self, dieroll: int) -> int:
        
        if self.both:
            return dieroll * 10
        
        else:
            return dieroll * 4

ELECTRIC_COMPANY = Utility("Electric Company", (1,1), "electric_company.png", 
                            23)
WATER_WORKS = Utility("Water Works", (2,7), "water_works.png", 
                            24)


# Railroads 

class Railroad(Tile):
    def __init__(self, name: str, pos: Tuple[int, int], image: imagetype,
        propnum: int):
        super().__init__(name, pos, image)
        self.price = 200
        self.propnum = propnum
        self.owner: Optional("Player") = None

        self.num_owned = 1
        self.morgage_price = 100
        self.morgaged = False

        self.rents = {1: 25,
            2: 50, 
            3: 100,
            4: 200}
        
    def rent(self) -> int:
        return self.rents[self.num_owned]

READING_RAILROAD = Railroad("Reading Railroad", (0, 4), "railroad.png",
    25)
PENNSYLVANIA_RAILROAD = Railroad("Pennsylvania Railroad", (1, 4), "railroad.png",
    26)
BO_RAILROAD = Railroad("B&O Railroad", (2, 4), "railroad.png",
    27)
SHORTLINE_RAILROAD = Railroad("Shortline Railroad", (3, 4), "railroad.png",
    28)

# Card Tiles

class Community_Chest_Tile(Tile):
    def __init__(self, pos: Tuple[int, int]):
        super().__init__("Community Chest", pos, "community.png" )
class Chance_Tile(Tile):
    def __init__(self, pos: Tuple[int, int]):
        super().__init__("Chance", pos, "chance.png" )

COMMUNITY_CHEST_TILE1 = Community_Chest_Tile((0,1))
COMMUNITY_CHEST_TILE2 = Community_Chest_Tile((1,6))
COMMUNITY_CHEST_TILE3 = Community_Chest_Tile((3,2))

CHANCE_TILE1 = Chance_Tile((0,6))
CHANCE_TILE2 = Chance_Tile((2,1))
CHANCE_TILE3 = Chance_Tile((3,5))

# Event Tiles

class Event_Tile(Tile):
    def __init__(self, name: str, pos: Tuple[int, int], image: imagetype, 
        effect: Callable[["Monopoly"], None]):
        super().__init__(name, pos, image)
        self.effect = effect
    def apply_tile(self, game: "Monopoly"):
        self.effect(game)

def go_tile(game: "Monopoly"):
    pass
def jail_tile(game:"Monopoly"):
    pass
def free_parking(game: "Monopoly"):
    game.pdict[game.turn].money += center_money
    game.center_money = 0
def go_to_jail_tile(game: "Monopoly"):
    game.send_jail()
def income_tax(game: "Monopoly"):
    game.pdict[game.turn].money -= 200
    game.center_money += 200
def luxury_tax(game: "Monopoly"):
    game.pdict[game.turn].money -= 75
    game.center_money += 200

GO_TILE = Event_Tile("Go", (3,9), "go.png", go_tile)
JAIL_TILE = Event_Tile("Jail", (0,9), "jail.png", jail_tile)
FREE_PARKING = Event_Tile("Free Parking", (1,9), "free_parking.png", free_parking)
GO_TO_JAIL = Event_Tile("Go to Jail", (2,9), "goto_jail.png", go_to_jail_tile)
INCOME_TAX = Event_Tile("Income Tax", (0,3), "income_tax.png", income_tax)
LUXURY_TAX = Event_Tile("Luxury_Tax", (3,7), "luxury_tax.png", luxury_tax)

# Game Board + Property Dictionary

STARTBOARD = [
    # Quadrant 0
    [mediterranean_ave, COMMUNITY_CHEST_TILE1, baltic_ave, INCOME_TAX, 
        READING_RAILROAD, oriental_ave, CHANCE_TILE1, vermont_ave, connecticut_ave, 
        JAIL_TILE], 
    # Quadrant 1
    [st_charles_place, ELECTRIC_COMPANY, states_ave, virginia_ave, 
        PENNSYLVANIA_RAILROAD, st_james_place, COMMUNITY_CHEST_TILE2, 
        tennessee_ave, new_york_ave, FREE_PARKING],
    # Quadrant 2 
    [kentucky_ave, CHANCE_TILE2, indiana_ave, illinois_ave, 
        BO_RAILROAD, atlantic_ave, ventnor_ave, WATER_WORKS, 
        marvin_gardens, GO_TO_JAIL],
    # Quadrant 3
    [pacific_ave, north_carolina_ave, COMMUNITY_CHEST_TILE3, pennsylvania_ave, 
        SHORTLINE_RAILROAD, CHANCE_TILE3, park_place, LUXURY_TAX, 
        boardwalk, GO_TILE]
        ]
PROPDICT = {
    1: mediterranean_ave,
    2: baltic_ave,
    3: oriental_ave,
    4: vermont_ave,
    5: connecticut_ave,
    6: st_charles_place,
    7: states_ave,
    8: virginia_ave,
    9: st_james_place,
    10: tennessee_ave,
    11: new_york_ave,
    12: kentucky_ave,
    13: indiana_ave,
    14: illinois_ave,
    15: atlantic_ave,
    16: ventnor_ave,
    17: marvin_gardens,
    18: pacific_ave,
    19: north_carolina_ave,
    20: pennsylvania_ave,
    21: park_place,
    22: boardwalk,
    23: ELECTRIC_COMPANY,
    24: WATER_WORKS,
    25: READING_RAILROAD,
    26: PENNSYLVANIA_RAILROAD,
    27: BO_RAILROAD,
    28: SHORTLINE_RAILROAD,
}





# Chance + Commmunity Chest Decks


class Event_Card():
    def __init__(self, name: str, description: str, image: str, 
        effect: Callable[["Monopoly"], None]):
        
        self.name = name
        self.description = description
        self.image = image
        self.effect = effect
    
    def apply_card(self, game: "Monopoly"):
        self.effect(game)



def advance_to_go(game: "Monopoly"):
    game.passgo()
    game.ploc[game.turn] = (3,9)
def go_to_jail(game: "Monopoly"):
    game.send_jail()
def school_tax(game: "Monopoly"):
    game.pdict[game.turn].money -= 150
    game.center_money += 150

CHANCE_DECK = {
    0: Event_Card("Advance to Go", "Go to go and collect $200", "advance.png", 
        advance_to_go),
    1: Event_Card("Go to Jail", "Go Directly to Jail", "jail.png",
        go_to_jail),
    2: Event_Card("School Tax", "Pay school tax of $150", "school_tax.png", 
        school_tax),
}

COMMUNITY_CHEST_DECK = {
    0: Event_Card("Advance to Go", "Go to go and collect $200", "advance.png", 
        advance_to_go),
    1: Event_Card("Go to Jail", "Go Directly to Jail", "jail.png",
        go_to_jail),
    2: Event_Card("School Tax", "Pay school tax of $150", "school_tax.png",
        school_tax),
}



        

class Piece():
    def __init__(self, name: str, image: imagetype):
        self.name = name
        self.image = image


# Class to represent individual players

class Player():
    def __init__(self, pnum: int, money: int):
        self.pnum = pnum
        self.money = money
        self.proplist: List[int] = []
        self.jail = -1
        self.get_out = False



# Class to represent a game of Monopoly

class Monopoly():
    pdict: Dict[int, Player]
    ploc: Dict[int, Tuple[int, int]]

    def __init__(self, num_players, startcash = 1500):
        
        assert num_players >= 2, "Must have at least 2 players"

        self.d1 = None
        self.d2 = None

        self.pdict = {}
        self.ploc = {}
        self.turn = 1
        self.num_players = num_players
        self.houses = 32
        self.hotels = 12
        self.board = copy.deepcopy(STARTBOARD)
        self.prop_dict = copy.deepcopy(PROPDICT)
        self.center_money = 0
        self.turn_count = 0    
        self.active_players = []
        self.inactive_players = []
        self.done = False    
        self.turn_taken = False
        

        self.chance_deck = CHANCE_DECK
        self.chance_order = [i for i in range(len(CHANCE_DECK.keys()))]
        self.community_chest_deck = COMMUNITY_CHEST_DECK
        self.community_chest_order = [
            i for i in range(len(COMMUNITY_CHEST_DECK.keys()))]

        
        random.shuffle(self.chance_order) 
        random.shuffle(self.community_chest_order) 

        for i in range(1, num_players + 1, 1):
            self.pdict[i] = Player(i, startcash)
            self.ploc[i] = (3, 9)
            self.active_players.append(i)
    
    def buy_property(self, player, propnum):
        prop = self.prop_dict[propnum]
        player.money -= prop.price

        if 23 <= propnum <= 24:
            for i in [23, 24]:
                if i in player.proplist:
                    self.prop_dict[i].both = True
                    self.prop_dict[propnum].both = True

        elif 25 <= propnum <= 28:
            for i in [25,26,27,28]:
                if i in player.proplist:
                    self.prop_dict[i].num_owned += 1
                    prop.num_owned += 1

        prop.owner = player
        player.proplist.append(propnum)

    def property_landing(self, prop):
        if prop.owner is None:
            
            buy = True
            
            if buy:
                self.buy_property(self.pdict[self.turn], prop.propnum)
        
        else:
            landing_player.money -= prop.rent 

    def community_chest_landing(self):
        cnum = self.community_chest_order.pop(0)
        self.community_chest_order.append(cnum)
        self.community_chest_deck[cnum].apply_card(self)
    
    def chance_landing(self):
        cnum = self.chance_order.pop(0)
        self.chance_order.append(cnum)
        self.chance_deck[cnum].apply_card(self)
    
    def event_tile_landing(self, tile):
        tile.apply_tile(self)
        
    def roll_dice(self):
        
        self.d1 = random.randint(1,6)
        self.d2 = random.randint(1,6)
    
    def apply_move(self):
        
        move = self.d1 + self.d2
        
        quadrant, dist = self.ploc[self.turn]
 
        
        tot_move = dist + move
        
        quadmove = tot_move // 10
            
        new_dist = (tot_move) % 10
        new_quad = (quadrant + quadmove) % 4
        
        if ((quadrant + quadmove >= 4) or (new_quad == 3 
            and new_dist == 9)) and not (quadrant == 3 and dist == 9):
            
            self.passgo()
        
        self.ploc[self.turn] = (new_quad, new_dist)

        landed = self.board[new_quad][new_dist]

        if isinstance(landed, Property) or isinstance(landed, Utility) or isinstance(landed, Railroad):
            self.property_landing(landed)
        elif isinstance(landed, Chance_Tile):
            self.chance_landing()
        elif isinstance(landed, Community_Chest_Tile):
            self.community_chest_landing()
        else:
            self.event_tile_landing(landed)
    
    def passgo(self):
        self.pdict[self.turn].money += 200
    
    def send_jail(self):
        player = self.pdict[self.turn]
        player.jail += 1
        self.ploc[self.turn] = (1,9)
        self.turn_taken = True

    def exit_jail(self):
        player = self.pdict[self.turn]
        if player.get_out:
            player.get_out = False
            return
        else:
            player.money -= 50 
            self.center_money += 50

    def take_turn(self) -> None:
        
        if self.turn_taken:
            return
        
        player = self.pdict[self.turn]
        
        
        
        self.roll_dice()
        
        if self.d1 != self.d2:
            self.turn_count = 0
        
        if self.d1 == self.d2:
            if player.jail != -1:
                player.jail = -1
                self.turn_count = 0
            else:
                self.turn_count += 1  
                
                if self.turn_count == 3:
                    self.send_jail()
                    self.turn_count = 0
                    return        

        
        if 0 <= player.jail <= 1:
            self.turn_taken = True
            return
        
        if player.jail == 3:
            self.exit_jail()
        

        
       
        self.apply_move()

        if self.turn_count == 0:
            self.turn_taken = True

        

    
        



