"""
Monopoly Implementation
"""
from typing import List, Tuple, Optional, Set, Callable, Dict, Union
import random
import copy

"""
A png in the form images/image-name.png, used to pull an image from the images
directory with pygame
"""
imagetype = str

"""
A Type representing one of the game tiles
"""
GameTileType = Union["Property", "Railroad", "Utility", 
    "Community_Chest_Tile", "Chance_Tile", "Event_Tile"]

# RGB Values for each property
RGBDICT = {
    1: (75, 0, 130),
    2: (75, 0, 130),
    3: (135, 206, 250),
    4: (135, 206, 250),
    5: (135, 206, 250),
    6: (221, 160, 221),
    7: (221, 160, 221),
    8: (221, 160, 221),
    9: (255, 140, 0),
    10: (255, 140, 0),
    11: (255, 140, 0),
    12: (227, 38, 54),
    13: (227, 38, 54),
    14: (227, 38, 54),
    15: (255, 215, 0),
    16: (255, 215, 0),
    17: (255, 215, 0),
    18: (34, 139, 34),
    19: (34, 139, 34),
    20: (34, 139, 34),
    21: (0, 0, 139),
    22: (0, 0, 139)}


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

        self.houses = 0
        self.owner: Optional["Player"] = None
        self.morgage_price = cost // 2
        self.morgaged = False
        self.color = RGBDICT[self.propnum]
        self.colornum = propnum // 3
        self.monop: bool = False
    def rent(self) -> int:
        
        if self.morgaged:
            return 0
        elif self.monop and self.houses == 0:
            return self.rents[self.houses] * 2
        else:
            return self.rents[self.houses]
    def build_house(self) -> None:
        self.houses += 1
    def remove_house(self) -> None:
        self.houses -= 1

# Brown Properties
mediterranean_ave = Property("Mediterranean Avenue", (0, 0), 
                            "images/DARK_PURPLE.png",
                            1, 60, 2, 10, 30, 90, 160, 250, 50)
baltic_ave = Property("Baltic Avenue", (0, 2), "images/DARK_PURPLE.png",
                    2, 60, 4, 20, 60, 180, 320, 450, 50)

# Light Blue Properties
oriental_ave = Property("Oriental Avenue", (0, 5), "images/LIGHT_BLUE.png",
                        3, 100, 6, 30, 90, 270, 400, 550, 50)
vermont_ave = Property("Vermont Avenue", (0, 7), "images/LIGHT_BLUE.png",
                    4, 100, 6, 30, 90, 270, 400, 550, 50)
connecticut_ave = Property("Connecticut Avenue", (0, 8), 
                        "images/LIGHT_BLUE.png",
                        5, 120, 8, 40, 100, 300, 450, 600, 50)

# Pink Properties
st_charles_place = Property("St. Charles Place", (1, 0), 
                            "images/LIGHT_PURPLE.png",
                            6, 140, 10, 50, 150, 450, 625, 750, 100)
states_ave = Property("States Avenue", (1, 2), "images/LIGHT_PURPLE.png",
                    7, 140, 10, 50, 150, 450, 625, 750, 100)
virginia_ave = Property("Virginia Avenue", (1, 3), "images/LIGHT_PURPLE.png",
                        8, 160, 12, 60, 180, 500, 700, 900, 100)

# Orange Properties
st_james_place = Property("St. James Place", (1, 5), 
                        "images/ORANGE.png",
                        9, 180, 14, 70, 200, 550, 750, 950, 100)
tennessee_ave = Property("Tennessee Avenue", (1, 7), 
                        "images/ORANGE.png",
                        10, 180, 14, 70, 200, 550, 750, 950, 100)
new_york_ave = Property("New York Avenue", (1, 8), 
                        "images/ORANGE.png",
                        11, 200, 16, 80, 220, 600, 800, 1000, 100)

# Red Properties
kentucky_ave = Property("Kentucky Avenue", (2, 0), "images/RED.png",
                        12, 220, 18, 90, 250, 700, 875, 1050, 150)
indiana_ave = Property("Indiana Avenue", (2, 2), "images/RED.png",
                    13, 220, 18, 90, 250, 700, 875, 1050, 150)
illinois_ave = Property("Illinois Avenue", (2, 3), "images/RED.png",
                        14, 240, 20, 100, 300, 750, 925, 1100, 150)

# Yellow Properties
atlantic_ave = Property("Atlantic Avenue", (2, 5), "images/YELLOW.png",
                        15, 260, 22, 110, 330, 800, 975, 1150, 150)
ventnor_ave = Property("Ventnor Avenue", (2, 6), "images/YELLOW.png",
                    16, 260, 22, 110, 330, 800, 975, 1150, 150)
marvin_gardens = Property("Marvin Gardens", (2, 8), 
                        "images/YELLOW.png",
                        17, 280, 24, 120, 360, 850, 1025, 1200, 150)

# Green Properties
pacific_ave = Property("Pacific Avenue", (3, 0), "images/GREEN.png",
                    18, 300, 26, 130, 390, 900, 1100, 1275, 200)
north_carolina_ave = Property("North Carolina Avenue", (3, 1), 
                            "images/GREEN.png",
                            19, 300, 26, 130, 390, 900, 1100, 1275, 200)
pennsylvania_ave = Property("Pennsylvania Avenue", (3, 3), 
                            "images/GREEN.png",
                            20, 320, 28, 150, 450, 1000, 1200, 1400, 200)

# Blue Properties
park_place = Property("Park Place", (3, 6), "images/DARK_BLUE.png",
                    21, 350, 35, 175, 500, 1100, 1300, 1500, 200)
boardwalk = Property("Boardwalk", (3, 8), "images/DARK_BLUE.png",
                    22, 400, 50, 200, 600, 1400, 1700, 2000, 200)

# Utilities

class Utility(Tile):
    def __init__(self, name: str, pos: Tuple[int, int], image: str,
        propnum: int):
        super().__init__(name, pos, image)
        self.price = 150
        self.propnum = propnum
        
        self.owner: Optional["Player"] = None
        self.both = False
        self.morgage_price = 75
        self.morgaged = False

    def rent(self, dieroll: int) -> int:
        if self.morgaged:
            return 0

        elif self.both:
            return dieroll * 10
        
        else:
            return dieroll * 4

ELECTRIC_COMPANY = Utility("Electric Company", (1,1), "images/Better_Electric.png", 
                            23)
WATER_WORKS = Utility("Water Works", (2,7), "images/WATERWORKS.png", 
                            24)


# Railroads 

class Railroad(Tile):
    def __init__(self, name: str, pos: Tuple[int, int], image: imagetype,
        propnum: int):
        super().__init__(name, pos, image)
        self.price = 200
        self.propnum = propnum
        self.owner: Optional["Player"] = None

        self.num_owned = 1
        self.morgage_price = 100
        self.morgaged = False

        self.rents = {1: 25,
            2: 50, 
            3: 100,
            4: 200}
        
    def rent(self) -> int:
        if self.morgaged:
            return 0
        else:
            return self.rents[self.num_owned]

READING_RAILROAD = Railroad("Reading Railroad", (0, 4), "images/RAILROAD.png",
    25)
PENNSYLVANIA_RAILROAD = Railroad("Pennsylvania Railroad", (1, 4), "images/RAILROAD.png",
    26)
BO_RAILROAD = Railroad("B&O Railroad", (2, 4), "images/RAILROAD.png",
    27)
SHORTLINE_RAILROAD = Railroad("Shortline Railroad", (3, 4), "images/RAILROAD.png",
    28)

# Card Tiles

class Community_Chest_Tile(Tile):
    def __init__(self, pos: Tuple[int, int]):
        super().__init__("Community Chest", pos, "images/COMMUNITY_CHEST.png" )
class Chance_Tile(Tile):
    def __init__(self, pos: Tuple[int, int]):
        super().__init__("Chance", pos, "images/CHANCE.png" )

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
    game.player_turn.money += game.center_money
    game.center_money = 0
def go_to_jail_tile(game: "Monopoly"):
    game.send_jail()
def income_tax(game: "Monopoly"):
    game.player_turn.money -= 200
    game.center_money += 200
def luxury_tax(game: "Monopoly"):
    game.player_turn.money -= 75
    game.center_money += 200

GO_TILE = Event_Tile("Go", (3,9), "images/GO_TILE.png", go_tile)
JAIL_TILE = Event_Tile("Jail", (0,9), "images/JAIL_TILE.png", jail_tile)
FREE_PARKING = Event_Tile("Free Parking", (1,9), "images/FREE_PARKING.png", free_parking)
GO_TO_JAIL = Event_Tile("Go to Jail", (2,9), "images/GO_TO_JAIL.png", go_to_jail_tile)
INCOME_TAX = Event_Tile("Income Tax", (0,3), "images/INCOME_TAX.png", income_tax)
LUXURY_TAX = Event_Tile("Luxury Tax", (3,7), "images/LUXURY_TAX.png", luxury_tax)

# Game Board + Property Dictionary

STARTBOARD: List[List[GameTileType]] = [
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
    28: SHORTLINE_RAILROAD}















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
    game.player_turn.money -= 150
    game.center_money += 150

CHANCE_DECK = {
    0: Event_Card("Advance to Go", "Go to go and collect $200", "advance.png", 
        advance_to_go),
    1: Event_Card("Go to Jail", "Go Directly to Jail", "jail.png",
        go_to_jail),
    2: Event_Card("School Tax", "Pay school tax of $150", "school_tax.png", 
        school_tax)}

COMMUNITY_CHEST_DECK = {
    0: Event_Card("Advance to Go", "Go to go and collect $200", "advance.png", 
        advance_to_go),
    1: Event_Card("Go to Jail", "Go Directly to Jail", "jail.png",
        go_to_jail),
    2: Event_Card("School Tax", "Pay school tax of $150", "school_tax.png",
        school_tax)}



        

class Piece():
    def __init__(self, name: str, image: imagetype):
        self.name = name
        self.image = image


# Class to represent individual players

class Player():
    def __init__(self, pnum: int, money: int):
        self.pnum = pnum
        self.money = money
        self.proplist: List[Union[Property, Utility, Railroad]] = []
        self.jail: int = 0
        self.get_out: bool = False


# Class to represent an auction

class Auction():
    def __init__(self, prop: Property, game: "Monopoly"):
        self.saveturn = copy.deepcopy(game.turn)
        self.active_players = copy.deepcopy(game.active_players)
        self.inactive_players = copy.deepcopy(game.inactive_players)
        self.game = game
        self.prop = prop
        self.game.isauction = True
        self.current_bid: int = 0
    
    def bid(self, val: int):
        assert self.game.auction, "There is no current auction happening"
        assert self.game.player_turn.money >= val, "You do not have enough money"
        assert val > self.current_bid, "You must bid more than the current bid"
        
        self.current_bid = val
        
        self.game.turn = self.game.turn % self.game.num_players + 1 
        
        while self.game.turn not in self.active_players:
            self.game.turn = self.game.turn % self.game.num_players + 1
        
        self.game.player_turn = self.game.pdict[self.game.turn]
 
    
    def quit_auction(self):
        self.active_players.remove(self.game.turn)
        self.inactive_players.append(self.game.turn)
        if len(self.active_players) == 1:
            self.game.turn = self.game.turn % self.game.num_players + 1 
        
            while self.game.turn not in self.active_players:
                self.game.turn = self.turn % self.game.num_players + 1
            
            self.game.player_turn = self.game.pdict[self.game.turn]

            self.prop.owner = self.game.player_turn
            self.game.player_turn.money -= self.current_bid
            self.game.player_turn.proplist.append(self.prop)

            self.game.isauction = False
            self.game.auction = None
            

            self.game.turn = self.saveturn
            self.game.player_turn = self.game.pdict[self.saveturn]

        else:
            self.game.turn = self.game.turn % self.game.num_players + 1 
        
            while self.game.turn not in self.active_players:
                self.game.turn = self.turn % self.game.num_players + 1
            
            self.game.player_turn = self.game.pdict[self.game.turn]

# Class to represent a game of Monopoly

class Monopoly():
    pdict: Dict[int, Player]
    ploc: Dict[int, Tuple[int, int]]
    turn: int
    houses: int
    d1: int
    d2: int
    hotels: int
    board: List[List[GameTileType]]
    prop_dict: Dict[int, Union[Property, Railroad, Utility]]
    center_money: int
    active_players: List[int]
    inactive_players: List[int]
    done: bool
    turn_taken: bool
    auction: Optional[Auction]
    isauction: bool
    chance_deck: Dict[int, Event_Card]
    community_chest_deck: Dict[int, Event_Card]
    chance_order: List[int]
    community_chest_order: List[int]



    def __init__(self, num_players: int, startcash: int = 1500):
        
        assert num_players >= 2, "Must have at least 2 players"

        self.d1: int = 0
        self.d2: int = 0

        self.pdict = {}
        self.ploc = {}
        self.turn = 1
        self.num_players = num_players
        self.houses = 32
        self.hotels = 12
        self.board = copy.deepcopy(STARTBOARD)

        
        self.prop_dict = {}
        for quadrant in self.board:
            for tile in quadrant:
                if (isinstance(tile, Property) 
                    or isinstance(tile, Railroad) 
                    or isinstance(tile, Utility)):

                    self.prop_dict[tile.propnum] = tile

        self.center_money = 0
        self.turn_count = 0    
        self.active_players = []
        self.inactive_players = []
        self.done = False    
        self.turn_taken = False
        
        
        self.auction = None
        self.isauction = False

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
        
        self.player_turn = self.pdict[1]

    def make_auction(self, prop: Property):
        self.auction = Auction(prop, self)
    
    def bid(self, bid: int):
        assert self.isauction, "There is no auction currently happening"
        assert self.auction is not None
        self.auction.bid(bid)
    def withdraw(self):
        assert self.isauction, "There is no auction currently happening"
        self.auction.quit_auction()
    def start_auction(self):
        cur_tile = self.current_tile()
        assert (isinstance(cur_tile, Property) 
            or isinstance(cur_tile, Railroad) 
            or isinstance(cur_tile, Utility)), "Not a valid tile to auction"

        self.make_auction(self.current_tile())


    def can_buy(self, tile: GameTileType) -> bool:
        return ((isinstance(tile, Property) or isinstance(tile, Utility) or 
            isinstance(tile, Railroad)) and (tile.pos == self.ploc[self.turn]) 
            and (tile.owner is None))


    def current_tile(self) -> GameTileType:
        

        player = self.player_turn
        
        pnum = player.pnum
        cloc = self.ploc[pnum]

        quad, dist = cloc
       
        return self.board[quad][dist]

    def update_monopoly(self, player: Player):
        count = {}
        
        for prop in player.proplist:
            if isinstance(prop, Property):
                if prop.colornum not in count:
                    count[prop.colornum] = [prop]
                else:
                    count[prop.colornum].append(prop)
        for colornum, colorlist in count.items():
            if colornum == 0 or colornum == 7:
                if len(colorlist) == 2:
                    for prop in colorlist:
                        prop.monop = True
                else:
                    for prop in colorlist:
                        prop.monop = False
            else:
                if len(colorlist) == 3:
                    for prop in colorlist:
                        prop.monop = True
                else:
                    for prop in colorlist:
                        prop.monop = False
    def update_railroad(self, player: Player):
        count = []
        for prop in player.proplist:
            if isinstance(prop, Railroad):
                count.append(prop)
        for railroad in count:
            railroad.num_owned = len(count)

    def update_utility(self, player: Player):
        count = 0
        for prop in player.proplist:
            if isinstance(prop, Utility):
                count += 1
        if count == 2:
            self.prop_dict[23].both = True # type: ignore
            self.prop_dict[24].both = True # type: ignore
        else:
            self.prop_dict[23].both = False # type: ignore
            self.prop_dict[24].both = False # type: ignore
    def buy_property(self, prop: Union[Property, Utility, Railroad]):
        
        assert self.can_buy(prop), "You cannot buy this property"
        
        propnum = prop.propnum
        
        self.player_turn.money -= prop.price
        self.player_turn.proplist.append(prop)
        prop.owner = self.player_turn



        if isinstance(prop, Utility):
            self.update_utility(self.player_turn)
            

        elif isinstance(prop, Railroad):
            self.update_railroad(self.player_turn)
        elif isinstance(prop, Property):
            self.update_monopoly(self.player_turn)
            


    def buy_current(self) -> None:
        cur_tile = self.current_tile()

        assert isinstance(cur_tile, Property) or isinstance(cur_tile, Utility) or isinstance(cur_tile, Railroad)
        
        self.buy_property(cur_tile)
        
    def utility_landing(self, prop: Utility):
        if prop.owner is not None:
            prop.owner.money += prop.rent(self.d1 + self.d2)
            self.player_turn.money -= prop.rent(self.d1 + self.d2)
    
    def property_landing(self, prop: Union[Railroad, Property]):
        if prop.owner is not None:

            prop.owner.money += prop.rent()
            self.player_turn.money -= prop.rent() 

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

        landed = self.current_tile()

        if isinstance(landed, Property) or isinstance(landed, Railroad):
            self.property_landing(landed)
        elif isinstance(landed, Utility):
            self.utility_landing(landed)
        elif isinstance(landed, Chance_Tile):
            self.chance_landing()
        elif isinstance(landed, Community_Chest_Tile):
            self.community_chest_landing()
        else:
            self.event_tile_landing(landed)
    
    def passgo(self):
        self.player_turn.money += 200
    
    def send_jail(self):
        self.turn_count = 0
        self.player_turn.jail += 1
        self.ploc[self.turn] = (1,9)
        self.turn_taken = True

    def exit_jail(self):
        if self.player_turn.get_out:
            self.player_turn.get_out = False
            return
        else:
            self.player_turn.money -= 50 
            self.center_money += 50

    def take_turn(self) -> None:
        assert not self.isauction, "There is an auction in progress, please either bid or withdraw"
        assert not self.turn_taken, "Turn has already been taken"        
        assert not self.done, "Game is Over"
        

        
        cur_tile = self.current_tile()
        
        if (isinstance(cur_tile, Property) 
            or isinstance(cur_tile, Utility) 
            or isinstance(cur_tile, Railroad)):
            assert not cur_tile.owner is None, "You must either start an auction or purchase the current property"

        self.roll_dice()
        
        if self.d1 != self.d2:
            self.turn_count = 0
            self.turn_taken = True
            

        
        if self.d1 == self.d2:
            if self.player_turn.jail != 0:
                self.player_turn.jail = 0
                self.turn_count = 0
                self.turn_taken = True
            else:
                self.turn_count += 1  
                
                if self.turn_count == 3:
                    self.send_jail()
                    return
            


        if 1 <= self.player_turn.jail <= 2:
            self.turn_taken = True
            return

        
        
        if self.player_turn.jail == 3:
            self.exit_jail()
        

        
       
        self.apply_move()

    def in_debt(self) -> bool:
        return self.player_turn.money < 0 
    
    def bankruptcy(self) -> None:
        
        
        cur_tile = self.current_tile()
            
        if (isinstance(cur_tile, Event_Tile)
            or isinstance(cur_tile, Chance_Tile) 
            or isinstance(cur_tile, Community_Chest_Tile)):
            
            bankrupter = None 
        else:
            bankrupter = cur_tile.owner



        if bankrupter is None:
            for prop in self.player_turn.proplist:
                prop.owner = bankrupter
                prop.morgaged = False
                if isinstance(prop, Property):
                    prop.monop = False
                if isinstance(prop, Railroad):
                    prop.num_owned = 1
                if isinstance(prop, Utility):
                    prop.both = False

        else: 
            for prop in self.player_turn.proplist:
                prop.owner = bankrupter
                bankrupter.proplist.append(prop)
            self.update_monopoly(bankrupter)
            self.update_railroad(bankrupter)
            self.update_utility(bankrupter)                    

       
            bankrupter.money += self.player_turn.money

        self.active_players.remove(self.turn)
        self.inactive_players.append(self.turn)

        
    def morgage_property(self, prop: Property):
        
        assert prop in self.player_turn.proplist, "You don't own this Property"
        
        
        
        assert not prop.morgaged, "This property is already morgaged"
        
        if isinstance(prop, Property):
            assert prop.houses == 0, "You must sell all houses first"

        prop.morgaged = True
        self.player_turn.money += prop.morgage_price
    
    def unmorgage_property(self, prop: Property):
        assert prop in self.player_turn.proplist,("You don't own this Property")
        
        assert prop.morgaged, "This property is not morgaged"
        
        assert self.player_turn.money >= (prop.morgage_price 
            + prop.morgage_price // 10), "Not enough money"

        prop.morgaged = False
        self.player_turn.money -= prop.morgage_price 
        self.player_turn.money -= prop.morgage_price // 10
    
    def build_house(self, prop: Property):
        
        assert not self.isauction, "There is an auction in progress, please either bid or withdraw"

        assert prop in self.player_turn.proplist, ("You don't own this Property")
        propnum = prop.propnum
        assert 1 <= propnum <= 22, "You can't build on non-color properties"
        
        assert not prop.morgaged, "This property is already morgaged"
        assert prop.houses <= 4, "There is already a hotel here"

        if 1 <= propnum <= 2:
            propnum2 = 1
            propnum3 = 2
        elif 3 <= propnum <= 20:
            if propnum % 3 == 0:

                propnum2 = propnum + 1
                propnum3 = propnum + 2
            elif propnum % 3 == 1:
                propnum2 = propnum + 1
                propnum3 = propnum - 1
            elif propnum % 3 == 2:
                propnum2 = propnum - 1
                propnum3 = propnum - 2
        elif 21 <= propnum <= 22:
            propnum2 = 21
            propnum3 = 22
        

        prop2 = self.prop_dict[propnum2]
        prop3 = self.prop_dict[propnum3]

        assert prop2 in self.player_turn.proplist, (f"{prop2.name} is not owned")
        assert prop3 in self.player_turn.proplist, (f"{prop3.name} is not owned")
        
        assert isinstance(prop2, Property)
        assert isinstance(prop3, Property)
        
        assert prop.houses - prop2.houses <= 0, f"Not enough houses on {prop2.name}"
        assert prop.houses - prop3.houses <= 0, f"Not enough houses on {prop3.name}"

        assert self.player_turn.money >= prop.house_price, "Not enough money"
        
        if prop.houses == 4:
            assert self.hotels >= 1, "Not enough hotels"
            self.houses += 4
            self.hotels -= 1
        else:
            assert self.houses >= 1, "Not enough houses"
            self.houses -= 1 
        
        
        prop.build_house()
        self.player_turn.money -= prop.house_price
    
    def sell_house(self, prop: Property):
        
        assert not self.isauction, "There is an auction in progress, please either bid or withdraw"

        assert prop in self.player_turn.proplist, "You don't own this Property"
        
        assert 1 <= prop.propnum <= 22, "You can't build on non-color properties"
        
        assert prop.houses >= 1, "There are no houses on this property"
        
        if prop.houses == 5:
            assert self.houses >= 4, "Not enough houses left to sell your hotel"
            self.hotels += 1
            self.houses -= 4
        if prop.houses <= 4:
            self.houses += 1
        
        self.player_turn.money += prop.house_price // 2


            
        
        
            

    def end_turn(self) -> None:





        assert not self.isauction, "There is an auction in progress, please either bid or withdraw"
        cur_tile = self.current_tile()
        
        if (isinstance(cur_tile, Property) 
            or isinstance(cur_tile, Utility) 
            or isinstance(cur_tile, Railroad)):
            assert not cur_tile.owner is None, "You must either start an auction or purchase the current property"
                



        assert self.turn_count == 0, "You rolled doubles, you have to take another turn"
        assert self.turn_taken, "Your Turn Hasn't Been Taken"
        
        if self.in_debt():
            bankrupt = True
            
            for prop in self.player_turn.proplist:

                bankrupt = bankrupt and prop.morgaged

                if isinstance(prop, Property):
                    bankrupt = bankrupt and (prop.houses == 0)
                
                if not bankrupt:
                    raise NegativeMoneyError(
                    f"{self.player_turn.pnum} is in debt, morgage properties " +
                    "and sell houses (or trade for money), until your balance" +
                    " is positive or all of your properties are morgaged and" +
                        " houses are sold")
            
            self.bankruptcy()
        
        self.turn = self.turn % self.num_players + 1 
        
        while self.turn not in self.active_players:
            self.turn = self.turn % self.num_players + 1
        
        self.player_turn = self.pdict[self.turn]

        if len(self.active_players) == 1:
            self.done = True

        self.turn_taken = False

class NegativeMoneyError(Exception):
    pass

    
        



