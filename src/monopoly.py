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
    "CommunityChestTile", "ChanceTile", "EventTile"]

"""
A Type representing buyable tiles
"""
BuyableTileType = Union["Property", "Utility", "Railroad"]


# RGB Values for each property
RGBDICT: Dict[int, Tuple[int, int, int]] = {
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
    """
    A class representing a basic game-tile
    Parameters:
        name: str: The name of the tile
        pos: Tuple[int, int]: A tuple representing the (quadrant, distance
            along the quadrant) on the game board
        image: imagetype: a pathway that specifies the image displayed on the tile
    """

    def __init__(self, name: str, pos: Tuple[int, int], image: imagetype):
        self.name = name
        self.pos = pos
        self.image = image


# Properties


class Property(Tile):
    """
    A class representing a color property tile
    """

    def __init__(self, name: str, pos: Tuple[int, int], image: imagetype,
        propnum: int, cost: int, r0: int, r1: int, r2: int, r3: int, r4: int,
        rh: int, hp: int):

        """
        Parameters:
            name, pos, image: see tile base class

            propnum: int: The property number associated with it in the property
                dictionary created below
            cost: int: the purchase price of the property
            r0 - r4: int: The rent paid on the property with the following number
                referring to the number of houses (eg. r0 is rent with 0 houses,
                r1 is rent with 1 house...)
            rh: int: Rent paid if there is a hotel on the property
            hp: int: House Price, the price to build a house on the property

        Non-Parameter Attributes:
            self.rents: Dict[int, int]: A dictionary to store the associated rents
            self.houses: int: The number of houses on the property
            self.owner: Optional[Player]: The player object that owns the property
            self.mortgage_price: int: The amount the property can be mortgaged for
            self.mortgaged: bool: Whether the property is mortgaged or not
            self.color: Tuple[int, int, int]: The RGB value associated with the
                property's color group
            self.colornum: int: The integer representation of the property's color
                group (eg. Baltic + Med. = group 0, light blues = group 1...)
            self.monop: bool: Whether the owner of the property owns all the others
                of the same color group (None notes the absence of an owner and thus
                the absence of a monopoly)
        """

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
        self.mortgage_price = cost // 2
        self.mortgaged = False
        self.color = RGBDICT[self.propnum]
        self.colornum = propnum // 3
        self.monop: bool = False

    def rent(self) -> int:
        """
        The rent paid if someone lands on this property
        """
        if self.mortgaged:
            return 0
        elif self.monop and self.houses == 0:
            # Rent is 2x if the monopoly is owned but the prop is undeveloped
            return self.rents[self.houses] * 2
        else:
            return self.rents[self.houses]

    def build_house(self) -> None:
        """
        Increases the number of houses by 1
        """
        self.houses += 1

    def remove_house(self) -> None:
        """
        Decreases the number of houses by 1
        """
        self.houses -= 1


### Construction of individual property objects (Thanks chatgpt) ###

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
    """
    A class to represent utility tiles
    """

    def __init__(self, name: str, pos: Tuple[int, int], image: str,
        propnum: int):
        """
        Parameters:
            name, pos, image: see tile base class
            propnum: int: The property number associated with the utility in the
            propdict below
        Non-Parameter Attributes:
            self.price: int: The price of the utility
            self.owner: Player: the player object that owns the utility
            self.both: bool: Whether both utilities are owned by the same player
            self.mortgage_price: int: The money gained when mortgaging the utility
            self.mortgaged: bool: Whether the utility is mortgaged
        """

        super().__init__(name, pos, image)
        self.price = 150
        self.propnum = propnum

        self.owner: Optional["Player"] = None
        self.both = False
        self.mortgage_price = self.price // 2
        self.mortgaged = False

    def rent(self, dieroll: int) -> int:
        """
        Rent charged for landing on the utility
        """
        if self.mortgaged:
            return 0

        elif self.both:
            return dieroll * 10

        else:
            return dieroll * 4


### Construction of individual utility tiles ###

ELECTRIC_COMPANY = Utility("Electric Company", (1,1), "images/Better_Electric.png",
                            23)
WATER_WORKS = Utility("Water Works", (2,7), "images/WATERWORKS.png",
                            24)


# Railroads


class Railroad(Tile):
    """
    A class representing railroad tiles
    """
    def __init__(self, name: str, pos: Tuple[int, int], image: imagetype,
        propnum: int):

        """
        Parameters:
            name, pos, image: see tile base class
            propnum: int: The property number associated with the railroad in the
            propdict below
        Non-Parameter Attributes:
            self.price: int: The price of the railroad
            self.owner: Player: the player object that owns the utility
            self.num_owned: int: The number of total railroads owned by the player
                who owns this railroad
            self.mortgage_price: int: The money gained when mortgaging the railroad
            self.mortgaged: bool: Whether the railroad is mortgaged
            self.rents: Dict[int, int]: A dictionary mapping the number of railroads
                owned to the rent charged
        """

        super().__init__(name, pos, image)

        self.price = 200
        self.propnum = propnum
        self.owner: Optional["Player"] = None

        self.num_owned = 1
        self.mortgage_price = 100
        self.mortgaged = False

        self.rents = {1: 25,
            2: 50,
            3: 100,
            4: 200}

    def rent(self) -> int:
        """
        Rent charged for landing on this property
        """

        if self.mortgaged:
            return 0
        else:
            return self.rents[self.num_owned]


### Construction of individual railroads ###

READING_RAILROAD = Railroad("Reading Railroad", (0, 4), "images/RAILROAD.png",
    25)
PENNSYLVANIA_RAILROAD = Railroad("Pennsylvania Railroad", (1, 4), "images/RAILROAD.png",
    26)
BO_RAILROAD = Railroad("B&O Railroad", (2, 4), "images/RAILROAD.png",
    27)
SHORTLINE_RAILROAD = Railroad("Shortline Railroad", (3, 4), "images/RAILROAD.png",
    28)


# Card Tiles


class CommunityChestTile(Tile):
    """
    Class for representing a community chest tile
    """
    def __init__(self, pos: Tuple[int, int]):
        """
        See Tile base class
        """
        super().__init__("Community Chest", pos, "images/COMMUNITY_CHEST.png" )


class ChanceTile(Tile):
    """
    Class for representing a chance tile
    """

    def __init__(self, pos: Tuple[int, int]):
        """
        See Tile base class
        """

        super().__init__("Chance", pos, "images/CHANCE.png" )


### Construction of community chest/chance tiles ###

COMMUNITY_CHEST_TILE1 = CommunityChestTile((0,1))
COMMUNITY_CHEST_TILE2 = CommunityChestTile((1,6))
COMMUNITY_CHEST_TILE3 = CommunityChestTile((3,2))

CHANCE_TILE1 = ChanceTile((0,6))
CHANCE_TILE2 = ChanceTile((2,1))
CHANCE_TILE3 = ChanceTile((3,5))

# Event Tiles

class EventTile(Tile):
    """
    Class to represent the event_tiles
    """
    def __init__(self, name: str, pos: Tuple[int, int], image: imagetype,
        effect: Callable[["Monopoly"], None]):
        """
        Parameters:
            name, pos, image: see tile base class
            effect: Callable[["Monopoly"], None]: The effect that landing on the tile has on the game
        """
        super().__init__(name, pos, image)
        self.effect = effect

    def apply_tile(self, game: "Monopoly"):
        self.effect(game)

def go_tile(game: "Monopoly"):
    """
    No effect
    """
    pass

def jail_tile(game:"Monopoly"):
    """
    No effect
    """
    pass

def free_parking(game: "Monopoly"):
    """
    Center money goes to landing player
    """
    game.player_turn.money += game.center_money
    game.center_money = 0

def go_to_jail_tile(game: "Monopoly"):
    """
    Sends the landing player to jail
    """
    game.send_jail()

def income_tax(game: "Monopoly"):
    """
    Puts the lesser of 10%/$200 of the player's money in the center
    """
    pct = .1 * game.player_turn.money
    for prop in game.player_turn.proplist:
        if prop.mortgaged:
            continue
        else:
            pct += prop.mortgage_price * .1
    pct = round(pct)

    game.player_turn.money -= min(pct, 200)
    game.center_money += min(pct, 200)

def luxury_tax(game: "Monopoly"):
    """
    Puts 75 of the landing player's money in the center
    """
    game.player_turn.money -= 75
    game.center_money += 200

GO_TILE = EventTile("Go", (3,9), "images/GO_TILE.png", go_tile)
JAIL_TILE = EventTile("Jail", (0,9), "images/JAIL_TILE.png", jail_tile)
FREE_PARKING = EventTile("Free Parking", (1,9), "images/FREE_PARKING.png", free_parking)
GO_TO_JAIL = EventTile("Go to Jail", (2,9), "images/GO_TO_JAIL.png", go_to_jail_tile)
INCOME_TAX = EventTile("Income Tax", (0,3), "images/INCOME_TAX.png", income_tax)
LUXURY_TAX = EventTile("Luxury Tax", (3,7), "images/LUXURY_TAX.png", luxury_tax)

# Game Board
"""
STARTBOARD: List[List[GameTileType]]: A List of Lists with each list representing
    a quadrant, and each item within a quadrant list being a game tile, starting
    with mediterranean at STARTBOARD[0][0] and going all the way to the GO_TILE
    at [3][9]
"""
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

# Property Dictionary
"""
PROPDICT: Dict[int, BuyableTileType]: A dictionary that maps
    property numbers to buyable tile objects
"""
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


class EventCard():
    """
    Base class to represent chance/commchest cards
    """

    def __init__(self, name: str, description: str, image: imagetype,
        effect: Callable[["Monopoly"], None]):
        """
        name: str: Name of the event card
        description: str: Description of it's effect
        image: imagetype: Image associated with the card
            (image should be a 1 x 2 aspect ratio representing the entire card)
        effect: Callable[["Monopoly"], None]): Function that applies an effect
            on the game
        """

        self.name = name
        self.description = description
        self.image = image
        self.effect = effect

    def apply_card(self, game: "Monopoly"):
        """
        Function that applies the effect of the card on the game
        """
        self.effect(game)


class ChanceCard(EventCard):
    """
    Object that represents a chance card
    """
    def __init__(self, name: str, description: str, image: str,
        effect: Callable[["Monopoly"], None]):
        """
        See event card docstring
        """

        super().__init__(name, description, image, effect)


class CommunityChestCard(EventCard):
    """
    Object representing a community chest card
    """
    def __init__(self, name: str, description: str, image: str,
        effect: Callable[["Monopoly"], None]):
        """
        See event card docstring
        """

        super().__init__(name, description, image, effect)

def advance_to_go(game: "Monopoly"):
    """
    Moves the player to go and gives them $200
    """
    game.passgo()
    game.ploc[game.turn] = (3,9)
def go_to_jail(game: "Monopoly"):
    """
    Sends the player to jail
    """
    game.send_jail()
def school_tax(game: "Monopoly"):
    """
    Charges the player $150 school tax
    """
    game.player_turn.money -= 150
    game.center_money += 150



"""
CHANCE_DECK: Dict[int: ChanceCard]: Dictionary mapping integers to ChanceCard
    objects, allowing the creation and shuffling of a chance deck as a list of
    integers
"""

CHANCE_DECK = {
    0: ChanceCard("Advance to Go", "Go to go and collect $200", "images/Advance.png",
        advance_to_go),
    #1: ChanceCard("Go to Jail", "Go Directly to Jail", "jail.png",
     #   go_to_jail),
    #2: ChanceCard("School Tax", "Pay school tax of $150", "school_tax.png",
     #   school_tax)
    }

"""
COMMUNITY_CHEST_DECK: Dict[int: CommunityChestCard]: Dictionary mapping
    integers to CommunityChestCard objects, allowing the creation and
    shuffling of a community chest deck as a list of ntegers
"""

COMMUNITY_CHEST_DECK = {
    0: CommunityChestCard("Advance to Go", "Go to go and collect $200", "images/Advance.png",
        advance_to_go),
    #1: CommunityChestCard("Go to Jail", "Go Directly to Jail", "jail.png",
       # go_to_jail),
   # 2: CommunityChestCard("School Tax", "Pay school tax of $150", "school_tax.png",
       # school_tax)
       }


# Player Class


class Player():
    """
    Class to represent individual players
    """

    def __init__(self, pnum: int, money: int):
        """
        Parameters:
            pnum: int: player number
            money: int: The amount of money the player has
        Non-Parameter Attributes:
            self.proplist: List[BuyableTileType]: A containing all the property
                objects that the player owns
            self.jail: int: An integer representing the number of turns in jail
                + 1, with 0 representing being out of jail, 1 representing the
                turn they were put in jail, 2 representing their 1st turn in
                jail, through 4 representing their 3rd turn in jail
            self.get_out: bool: a boolean tracking whether the player has a
                get out of jail free card
        """

        self.pnum = pnum
        self.money = money
        self.proplist: List[BuyableTileType] = []
        self.jail: int = 0
        self.get_out: bool = False
    def __str__(self) -> str:
        """
        Returns a string of the player in the form "Player player.pnum"
        """
        return f"Player {str(self.pnum)}"
    def sort_prop_list(self) -> None:
        """
        Sorts the player's property list by ordering the properties by property number
        (It is easily optimizable by implementing a binary search algorithm which
        can get done at some point as it would technically be more efficent, but
        is not urgent because the list size never goes over 30)
        """
        tempdict = {}
        for prop in self.proplist:
            tempdict[prop.propnum] = prop
        propnums = list(tempdict.keys())
        propnums.sort()
        self.proplist = []
        for propnum in propnums:
            self.proplist.append(tempdict[propnum])


# Auction Class


class Auction():
    """
    Class to represent and perform the functions of a monopoly auction
    It uses the game to keep track of the auction and saves the things it
    changes in it's attributes:
    Changes:
        game.turn: changes the game's turn, using it to represent the player
            who is currently bidding
        game.active/inactive_players: changes the active and inactive player
            lists to represent the players who have not withdrawn from the
            auction
    """
    def __init__(self, prop: BuyableTileType, game: "Monopoly"):
        """
        Parameters:
            prop: The property being auctioned
            game: The game the auction is being done for
        Non-Parameter Attributes:
            self.save_turn: int: The turn of the game when the auction started
            self.active_players: List[int]: The list of player numbers that were
                active players when the auction was started
            self.inactive_players: List[int]: Same as above but for inactive
                players
            self.current_bid: int: The current highest bid for the auction
        """

        self.saveturn = game.turn
        self.active_players = copy.deepcopy(game.active_players)
        self.inactive_players = copy.deepcopy(game.inactive_players)
        self.game = game
        self.prop = prop
        self.game.isauction = True
        self.current_bid: int = 0

    def bid(self, val: int) -> None:
        """
        Changes the current bid to the inputted value, and modulates the game's
        turn until a player active in the auction is reached

        Inputs:
            val: int: the value being bid
        """

        self.current_bid = val

        self.game.turn = self.game.turn % self.game.num_players + 1

        while self.game.turn not in self.active_players:
            self.game.turn = self.game.turn % self.game.num_players + 1

        self.game.player_turn = self.game.pdict[self.game.turn]

    def quit_auction(self):
        """
        Withdraws the current bidding player from auction contention, and checks
            if that would end the auction (only 1 player left active)
        If 1 active player left:
            Resets the game to the previous state, with the exception of the
            auctioned property being owned by the winning player, and that money
            being paid out of the winning player's funds
        Else:
            Continues the auction by modulating the turn until an active
            player is reached
        """

        self.active_players.remove(self.game.turn)
        self.inactive_players.append(self.game.turn)
        if len(self.active_players) == 1:
            self.game.turn = self.game.turn % self.game.num_players + 1

            while self.game.turn not in self.active_players:
                self.game.turn = self.game.turn % self.game.num_players + 1

            self.game.player_turn = self.game.pdict[self.game.turn]

            self.prop.owner = self.game.player_turn
            self.game.player_turn.money -= self.current_bid
            self.game.player_turn.proplist.append(self.prop)

            self.game.isauction = False
            self.game.auction = None


            self.game.turn = self.saveturn
            self.game.player_turn = self.game.pdict[self.saveturn]
            self.game.poss_bid = 1

        else:
            self.game.turn = self.game.turn % self.game.num_players + 1

            while self.game.turn not in self.active_players:
                self.game.turn = self.game.turn % self.game.num_players + 1

            self.game.player_turn = self.game.pdict[self.game.turn]


# Class to represent a game of Monopoly


class Monopoly():
    """
    Object that represents the game itself, holding all of the neccasary
    attributes and tile objects and functions to play a game of monopoly
    """

    pdict: Dict[int, Player]
    ploc: Dict[int, Tuple[int, int]]
    turn: int
    houses: int
    __d1: int
    __d2: int
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
    chance_deck: Dict[int, ChanceCard]
    community_chest_deck: Dict[int, CommunityChestCard]
    chance_order: List[int]
    community_chest_order: List[int]
    poss_bid: int
    landed: Optional[GameTileType]
    lastchance: Optional[ChanceCard]
    lastcommchest: Optional[CommunityChestCard]

    def __init__(self, num_players: int, startcash: int = 1500):
        """
        Initializes the monopoly object

        Parameters:
            num_players: int: The number of players that should be in the game
            startcash: int: The starting amount of money for each player (
                defaults to $1500)
        Non-Parameter Attributes:
            self.__d1: int: the value of the first die that was rolled
            self.__d2: int: the value of the second die that was rolled
            self.pdict: Dict[int, Player]: A dictionary mapping player numbers
                to player objects
            self.ploc: Dict[int, Tuple[int, int]]: A dictionary mapping
                player number to the player's location
            self.turn: int: The player number of the current player who's turn
                it is
            self.houses: int: the number of houses available for purchase
            self.hotels: int: the number of hotels available for purchase
            self.board: List[List[GameTileType]]: A deepcopy of startboard
                which serves as the list of tiles/property objects for the game
            self.prop_dict: Dict[int, BuyableTileType]: A dictionary that maps
                property numbers to the specific buyable tile objects used in the game
            self.center_money: int: the amount of money that has been confiscated
                through fines and put into the center, the player who lands on
                free parking collects this money
            self.turn_count: The amount of rolls that the current player has done
                since the beginnning of their turn, if it hits 3 (meaning 3 doubles
                in a row), the player is sent to jail and the next player takes
                their turn
            self.active_players: List[int]: A list of the player numbers of
                players who haven't gone bankrupt
            self.inactive_players: List[int]: A list of the player numbers of
                players who have gone bankrupt
            self.done: bool: True if the game is done, False otherwise
            self.turn_taken: bool: Keeps track of whether the player has
                completed all possible rolls this turn
            self.auction: Optional[Auction]: The auction object for the auction
                that is currently underway (None if no auction is currently
                happening)
            self.isauction: bool: True if there is an auction happening
            self.poss_bid: int: The current bid that is being proposed by the
                player who's turn it is
            self.chance_deck: Dict[int, ChanceCard]: The dictionary of chance
                cards for the game
            self.chance_order: List[int]: The list of integers representing the
                order of the chance deck (it gets randomized at the beginning
                and when the entire chance deck is run through)
            self.community_chest_deck: Dict[int, CommunityChestCard]: The
                dictionary of community_chest cards for the game
            self.community_chest_order: List[int]: The list of integers
                representing the order of the community chest deck (it gets
                randomized at the beginning and when the entire deck is run
                through)
            self.landed: Optional[GameTileType]: The last tile that was landed
                on
            self.lastchance: Optional[ChanceCard]: The chance card that was just drawn
            self.lastcommchest: Optional[CommunityChestCard]: The last
                communitychest card that was drawn




        """
        assert num_players >= 2, "Must have at least 2 players"

        self.__d1: int = 1
        self.__d2: int = 1

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
        self.poss_bid = 1

        self.chance_deck = CHANCE_DECK
        self.chance_order = [i for i in range(len(CHANCE_DECK.keys()))]
        self.community_chest_deck = COMMUNITY_CHEST_DECK
        self.community_chest_order = [
            i for i in range(len(COMMUNITY_CHEST_DECK.keys()))]


        self.landed = None
        self.lastchance = None
        self.lastcommchest = None

        random.shuffle(self.chance_order)
        random.shuffle(self.community_chest_order)

        for i in range(1, num_players + 1, 1):
            self.pdict[i] = Player(i, startcash)
            self.ploc[i] = (3, 9)
            self.active_players.append(i)

        self.player_turn = self.pdict[1]

    # Current Gamestate Methods

    def current_tile(self) -> GameTileType:
        """
        Returns the tile currently occupied by the player who's turn it is

        Returns: Tile occupied by player who's turn it is
        """

        player = self.player_turn

        pnum = player.pnum
        cloc = self.ploc[pnum]

        quad, dist = cloc

        return self.board[quad][dist]

    @property
    def d1(self) -> int:
        """
        Returns the current value of the first die
        """
        return self.__d1

    @property
    def d2(self) -> int:
        """
        Returns the current value of the second die
        """
        return self.__d2

    # Auction Methods

    def can_start_auction(self, prop: GameTileType) -> bool:
        """
        Returns a boolean on whether the current player can start an auction on
        the given property
        
        Inputs:
            prop: GameTileType: The property being checked
        Outputs:
            True: If the current player can start an auction for the input prop
            False: Otherwise
        """
        cur_tile = self.current_tile()
        if not isinstance(cur_tile, (Property, Railroad, Utility)):
            return False
        if not cur_tile is prop:
            return False
        if cur_tile.owner is not None:
            return False
        if self.isauction:
            return False

        return True

    def start_auction(self) -> None:
        """
        Starts an auction for the current tile
        Raises:
            AssertionError if it would violate the rules to start an auction on
                the currrent tile (not a buyable tile, tile is owned, or there
                is an auction already ongoing)
        """

        cur_tile = self.current_tile()
        assert isinstance(cur_tile, (Property, Railroad, Utility)), "Not a valid tile to auction"
        assert cur_tile.owner is None, "Can't auction an owned property"
        assert not self.isauction, "The auction is already ongoing"

        self.auction = Auction(cur_tile, self)

    def bid(self) -> None:
        """
        Bids the current "poss_bid" in the auction
        Raises:
            AssertionError if the bid is not legal (no auction going on,
            current player can't afford the bid, the proposed bid is <= the
            current bid)
        """

        assert self.isauction, "There is no auction currently happening"
        assert self.auction is not None
        assert self.player_turn.money >= self.poss_bid, "You do not have enough money"
        assert self.poss_bid > self.auction.current_bid, "You must bid more than the current bid"

        self.auction.bid(self.poss_bid)

    def can_bid(self) -> bool:
        """
        Returns whether the current player can bid the current poss_bid
        """
        return self.isauction and (self.auction is not None) and self.player_turn.money >= self.poss_bid and self.poss_bid > self.auction.current_bid

    def change_poss_bid(self, inc: int) -> None:
        """
        Changes the poss bid by the inputted inc
        Inputs:
            inc: int: The amount to increment the possible bid by
        Raises:
            AssertionError if the change is not legal (There is no auction,
                the player would not be able to pay for that bid, the current
                bid is more than what the incremented possible bid would be)
        """
        assert self.isauction, "There is no auction currently happening"
        assert self.auction is not None
        assert self.player_turn.money >= self.poss_bid + inc, "You do not have enough money"
        assert self.poss_bid + inc > self.auction.current_bid, "You must bid more than the current bid"
        self.poss_bid += inc

    def can_change_poss_bid(self, inc: int) -> bool:
        """
        Returns whether the given value is a legal change to possbid that would
        allow the poss bid to become a legal bid
        Inputs:
            inc: int: The increment to return the legality of
        """
        return (self.isauction
            and self.auction is not None
            and self.player_turn.money >= self.poss_bid + inc
            and self.poss_bid + inc > self.auction.current_bid)

    def withdraw(self) -> None:
        """
        Withdraws the current player from the auction
        Raises:
            AssertionError if there is not auction going on
        """
        assert self.isauction, "There is no auction currently happening"
        assert self.auction is not None, "Cannot withdraw from a nonexistant auction"
        self.auction.quit_auction()

    # Update Player Property List Methods

    def update_monopoly(self, player: Player) -> None:
        """
        Updates the inputted player's Property objects if their monopoly status
            has changed

        Inputs:
            player: Player: The player whose properties need to be checked
        """

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

    def update_railroad(self, player: Player) -> None:
        """
        Updates the inputted player's Railroad objects if the number owned status
            has changed

        Inputs:
            player: Player: The player whose Railroads need to be checked
        """

        count = []
        for prop in player.proplist:
            if isinstance(prop, Railroad):
                count.append(prop)
        for railroad in count:
            railroad.num_owned = len(count)

    def update_utility(self, player: Player) -> None:
        """
        Updates the inputted player's Utility objects if their both owned status
            has changed
        Inputs:
            player: Player: The player whose Utilities need to be checked
        """

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

    # Movement + Landing Methods

    def __roll_dice(self) -> None:
        """
        Simulates rolling dice by setting the d1 and d2 attributes to random 
        integers between 1 and 6
        """
        self.__d1 = random.randint(1,6)
        self.__d2 = random.randint(1,6)

    def __apply_move(self) -> None:
        """
        Applies the move given by the sum of the 2 dice attributes to the 
            current player who's turn it is
        """
        move = self.__d1 + self.__d2

        quadrant, dist = self.ploc[self.turn]


        tot_move = dist + move

        quadmove = tot_move // 10

        new_dist = (tot_move) % 10
        new_quad = (quadrant + quadmove) % 4

        if ((quadrant + quadmove >= 4) or (new_quad == 3
            and new_dist == 9)) and not (quadrant == 3 and dist == 9):

            self.passgo()

        self.ploc[self.turn] = (new_quad, new_dist)

        self.landed = self.current_tile()

        landed = self.landed

        if isinstance(landed, Property) or isinstance(landed, Railroad):
            self.__property_landing(landed)
        elif isinstance(landed, Utility):
            self.__utility_landing(landed)
        elif isinstance(landed, ChanceTile):
            self.__chance_landing()
        elif isinstance(landed, CommunityChestTile):
            self.__community_chest_landing()
        else:
            self.__event_tile_landing(landed)

    def __utility_landing(self, prop: Utility) -> None:
        """
        Resolves the effect of landing on the given utility
        """
        if prop.owner is not None:
            prop.owner.money += prop.rent(self.__d1 + self.__d2)
            self.player_turn.money -= prop.rent(self.__d1 + self.__d2)

    def __property_landing(self, prop: Union[Railroad, Property]) -> None:
        """
        Resolves the effect of landing on the given property/railroad tile
        """

        if prop.owner is not None:

            prop.owner.money += prop.rent()
            self.player_turn.money -= prop.rent()

    def __community_chest_landing(self) -> None:
        """
        Resolves the effect of landing on a community chest tile
        """

        commnum = self.community_chest_order.pop()
        self.community_chest_deck[commnum].apply_card(self)
        self.lastcommchest = self.community_chest_deck[commnum]

        if len(self.community_chest_order) == 0:
            self.community_chest_order = [
            i for i in range(len(COMMUNITY_CHEST_DECK.keys()))]
            random.shuffle(self.community_chest_order)

    def __chance_landing(self) -> None:
        """
        Resolves the effect of landing on a chance tile
        """

        chancenum = self.chance_order.pop()
        self.chance_deck[chancenum].apply_card(self)
        self.lastchance = self.chance_deck[chancenum]

        if len(self.chance_order) == 0:
            self.chance_order = [
            i for i in range(len(CHANCE_DECK.keys()))]
            random.shuffle(self.chance_order)

    def __event_tile_landing(self, tile: EventTile) -> None:
        """
        Resolves the effect of landing on the given event tile
        """

        tile.apply_tile(self)

    def passgo(self) -> None:
        """
        The effect of passing go (landing is technically passing, but moving
        off of go is not passing)
        """
        self.player_turn.money += 200


    # Jail Methods
    
    def send_jail(self) -> None:
        """
        Sends the current player who's turn it is to jail
        """
        self.turn_count = 0
        self.player_turn.jail += 1
        self.ploc[self.turn] = (0,9)
        self.turn_taken = True

    def get_out_free(self) -> None:
        """
        Uses the player's get out of jail free card and frees them from jail

        Raises:
            AssertionError if the player is not in jail or doesnt have a get
                out of jail free card
        """
        assert self.player_turn.jail != 0, "You are not in jail"
        assert self.player_turn.get_out, "You don't have a get out of jail free card"
        self.player_turn.get_out = False
        self.player_turn.jail = 0

    def pay_50_get_out(self) -> None:
        """
        If the current player is in jail, subtracts 50 from their money and
        removes them from jail

        Raises:
            AssertionError if the current player is not in jail
        """
        assert self.player_turn.jail != 0, "You are not in jail"
        self.player_turn.money -= 50
        self.player_turn.jail = 0

    # Turn Methods
    def can_take_turn(self) -> bool:
        """
        Returns whether the current player can take their turn
        
        Outputs:
            bool: True if the player can roll the dice and move, False otherwise
        """
        if self.player_turn.money < 0:
            return False
        if self.isauction:
            return False
        if self.turn_taken:
            return False
        if self.done:
            return False
        cur_tile = self.current_tile()
        if isinstance(cur_tile, (Property, Railroad, Utility)) and cur_tile.owner is None:
            return False
        if self.player_turn.jail == 4:
            return False
        if self.in_debt():
            return False
        return True

    def take_turn(self) -> None:
        """
        Rolls the dice and resolves any landing events that occur

        Raises:
            AssertionError:
                if there is an auction going on
                if the player has already taken their turn
                if the game is over
                if the player has spent 3 turns in jail and has to exit before
                    taking their turn
                if the current tile's owner is None (it either needs to be
                    auctioned or purchased)
                if the player is in debt
        """
        assert not self.isauction, "There is an auction in progress, please either bid or withdraw"
        assert not self.turn_taken, "Turn has already been taken"
        assert not self.done, "Game is Over"
        if self.player_turn.jail == 4:
            raise AssertionError("You have spent 3 turns in jail, either pay or use a get out of jail free card")



        cur_tile = self.current_tile()

        if isinstance(cur_tile, (Property, Railroad, Utility)):
            assert not cur_tile.owner is None, "You must either start an auction or purchase the current property"


        assert not self.in_debt(), "You must mortgage all properties and sell all houses"

        self.__roll_dice()

        if self.__d1 != self.__d2:
            self.turn_count = 0
            self.turn_taken = True



        if self.__d1 == self.__d2:
            if self.player_turn.jail != 0:
                self.player_turn.jail = 0
                self.turn_count = 0
                self.turn_taken = True
            else:
                self.turn_count += 1

                if self.turn_count == 3:
                    self.send_jail()
                    return



        if 1 <= self.player_turn.jail <= 3:
            self.player_turn.jail += 1
            return

        self.__apply_move()

    def can_end_turn(self) -> bool:
        """
        Returns whether the current player can end their turn
        """
        if self.isauction:
            return False
        cur_tile = self.current_tile()
        if isinstance(cur_tile, (Property, Railroad, Utility)) and cur_tile.owner is None:
            return False
        if self.turn_count != 0:
            return False
        if not self.turn_taken:
            return False
        if self.in_debt():
            return False
        return True

    def end_turn(self) -> None:
        """
        Ends the current players turn if possible, otherwise raises an 
        assertionerror detailing why the action cannot be performed
        """
        assert not self.isauction, "There is an auction in progress, please either bid or withdraw"
        cur_tile = self.current_tile()

        if isinstance(cur_tile, (Property, Railroad, Utility)):
            assert not cur_tile.owner is None, "You must either start an auction or purchase the current property"




        assert self.turn_count == 0, "You rolled doubles, you have to take another turn"
        assert self.turn_taken, "Your Turn Hasn't Been Taken"

        assert not self.in_debt(), "You must mortgage all properties and sell all houses to declare bankruptcy"

        self.landed = None
        self.turn = self.turn % self.num_players + 1

        while self.turn not in self.active_players:
            self.turn = self.turn % self.num_players + 1

        self.player_turn = self.pdict[self.turn]

        if len(self.active_players) == 1:
            self.done = True

        self.turn_taken = False

    # Bankruptcy Methods

    def in_debt(self) -> bool:
        """
        Returns whether the current player has less than $0
        """
        return self.player_turn.money < 0

    def is_bankrupt(self) -> bool:
        """
        Returns if the current player has morgaged all properties, sold all
            houses, and is still in debt
        """
        bankrupt = False

        if self.in_debt():
            bankrupt = True

            for prop in self.player_turn.proplist:

                bankrupt = bankrupt and prop.mortgaged

                if isinstance(prop, Property):
                    bankrupt = bankrupt and (prop.houses == 0)

        return bankrupt

    def declare_bankruptcy(self) -> None:
        """
        Goes through the process of bankruptcy, removing the current player form
            the active player list, turning over all of their properties to
                the bank if they went in debt to the bank
                the player who bankrupted them if they couldn't afford rent
        Also moves on to the following player's turn
        """

        cur_tile = self.current_tile()

        if (isinstance(cur_tile, EventTile)
            or isinstance(cur_tile, ChanceTile)
            or isinstance(cur_tile, CommunityChestTile)):

            bankrupter = None
        else:
            bankrupter = cur_tile.owner



        if bankrupter is None:
            for prop in self.player_turn.proplist:
                prop.owner = bankrupter
                prop.mortgaged = False
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

        self.landed = None
        self.turn = self.turn % self.num_players + 1

        while self.turn not in self.active_players:
            self.turn = self.turn % self.num_players + 1

        self.player_turn = self.pdict[self.turn]

        if len(self.active_players) == 1:
            self.done = True

        self.turn_taken = False

    # Buyable Tile Methods

    def can_mortgage(self, prop: GameTileType) -> bool:
        """
        Returns whether the inputted tile can be morgaged by the current 
        player
        """
        if not (isinstance(prop, Railroad) or isinstance(prop, Property) or isinstance(prop, Utility)):
            return False
        return not prop.mortgaged and prop.owner is self.player_turn
    
    def mortgage_property(self, prop: Union[Railroad, Property, Utility]) -> None:
        """
        Morgages the inputted buyable tile

        Raises:
            AssertionError if the property is not owned by the current player,
                already morgaged, or has ouses on it
        """
        assert prop in self.player_turn.proplist, "You don't own this Property"



        assert not prop.mortgaged, "This property is already mortgaged"

        if isinstance(prop, Property):
            assert prop.houses == 0, "You must sell all houses first"

        prop.mortgaged = True
        self.player_turn.money += prop.mortgage_price
    
    def can_unmortgage(self, prop: GameTileType) -> bool:
        """
        Returns whether the inputted tile can be unmorgaged by the current 
        player
        """
        if not (isinstance(prop, Railroad) or isinstance(prop, Property) or isinstance(prop, Utility)):
            return False
        return prop.mortgaged and prop.owner is self.player_turn
    
    def unmortgage_property(self, prop: Union[Railroad, Property, Utility]) -> None:
        """
        Unmorgages the inputted buyable tile

        Raises:
            AssertionError if the property is not owned by the current player,
                not morgaged, or the player doesn't have the money.
        """
        assert prop in self.player_turn.proplist,("You don't own this Property")

        assert prop.mortgaged, "This property is not mortgaged"

        assert self.player_turn.money >= (prop.mortgage_price
            + prop.mortgage_price // 10), "Not enough money"

        prop.mortgaged = False
        self.player_turn.money -= prop.mortgage_price
        self.player_turn.money -= prop.mortgage_price // 10

    def can_build(self, prop: GameTileType) -> bool:
        """
        Returns whether the current player can build on the given tile
        """

        if not isinstance(prop, Property):
            return False
        if self.isauction:
            return False
        if prop not in self.player_turn.proplist:
            return False
        if not prop.monop:
            return False
        if prop.mortgaged:
            return False
        if prop.houses == 5:
            return False

        propnum = prop.propnum

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


        assert isinstance(prop2, Property)
        assert isinstance(prop3, Property)

        if prop.houses - prop2.houses > 0 or prop2.mortgaged:
            return False
        if prop.houses - prop3.houses > 0 or prop3.mortgaged:
            return False

        if self.player_turn.money <= prop.house_price:
            return False

        if prop.houses == 4 and self.hotels < 1:
            return False
        elif self.houses < 1:
            return False

        return True

    def build_house(self, prop: Property):
        """
        Builds a house on the inputted property if possible, otherwise raises 
            AssertionError if the action cannot be performed
        """
        assert not self.isauction, "There is an auction in progress, please either bid or withdraw"

        assert prop in self.player_turn.proplist, ("You don't own this Property")
        assert isinstance(prop, Property), "You can't build on non-color Properties"
        assert prop.monop, "You do not have a monopoly on this property"
        propnum = prop.propnum

        assert not prop.mortgaged, "This property is mortgaged, unmortgage it to build"
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


        assert isinstance(prop2, Property)
        assert isinstance(prop3, Property)

        assert prop.houses - prop2.houses <= 0, f"Not enough houses on {prop2.name}"
        assert prop.houses - prop3.houses <= 0, f"Not enough houses on {prop3.name}"
        assert not prop2.mortgaged, f"{prop2.name} is mortgaged, unmortgage it to build on this property"
        assert not prop3.mortgaged, f"{prop3.name} is mortgaged, unmortgage it to build on this property"
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

    def can_sell(self, prop: GameTileType):
        """
        Returns whether the current player can sell a house on the inputted tile
        """
        if not isinstance(prop, Property):
            return False


        if prop not in self.player_turn.proplist:
            return False
        if prop.houses == 0:
            return False
        if prop.houses == 5:
            if self.houses < 4:
                return False
        propnum = prop.propnum

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


        assert isinstance(prop2, Property)
        assert isinstance(prop3, Property)

        if prop.houses - prop2.houses < 0 or prop.houses - prop3.houses < 0:
            return False

        return True

    def sell_house(self, prop: Property):
        """
        Sells a house on the inputted property if possible, otherwise raises
        an assertionerror detailing the problem
        """
        assert not self.isauction, "There is an auction in progress, please either bid or withdraw"

        assert prop in self.player_turn.proplist, "You don't own this Property"

        assert 1 <= prop.propnum <= 22, "You can't build on non-color properties"

        assert prop.houses >= 1, "There are no houses on this property"


        propnum = prop.propnum

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


        assert isinstance(prop2, Property)
        assert isinstance(prop3, Property)

        assert prop.houses - prop2.houses >= 0, f"Sell houses on {prop2.name} first"
        assert prop.houses - prop3.houses >= 0, f"Sell houses on {prop3.name} first"

        if prop.houses == 5:
            assert self.houses >= 4, "Not enough houses left to sell your hotel"
            self.hotels += 1
            self.houses -= 4
        if prop.houses <= 4:
            self.houses += 1

        prop.remove_house()
        self.player_turn.money += prop.house_price // 2

    def can_buy(self, tile: GameTileType) -> bool:
        """
        Returns whether the current player can buy the inputted tile

        Inputs:
            Tile: GameTileType: The tile in question

        Outputs: bool: True if the tile can be purchased by the current player,
            False otherwise
        """
        
        return (isinstance(tile, (Property, Railroad, Utility))
            and (tile.pos == self.ploc[self.turn])
            and (tile.owner is None)
            and tile.price <= self.player_turn.money
            and not self.isauction)

    def buy_property(self, prop: BuyableTileType) -> None:
        """
        Buys the inputted Buyable Tile if it is a tile that the current player
        is allowed to buy

        Inputs:
            prop: BuyableTileType: The property being bought
        Raises:
            AssertionError if it is not legal to buy the tile inputted
        """

        assert isinstance(prop, (Property, Railroad, Utility)), "This is not a buyable tile"
        assert (prop.pos == self.ploc[self.turn]), "You cannot buy a property you do not occupy"
        assert prop.owner is None, "You cannot buy a property someone already owns"
        assert self.player_turn.money >= prop.price, "You cannot afford this tile, mortgage properties to raise money or put it up for auction"
        assert not self.isauction, "You can't buy a property that is currently being auctioned"

        self.player_turn.money -= prop.price
        self.player_turn.proplist.append(prop)
        prop.owner = self.player_turn



        if isinstance(prop, Utility):
            self.update_utility(self.player_turn)


        elif isinstance(prop, Railroad):
            self.update_railroad(self.player_turn)
        elif isinstance(prop, Property):
            self.update_monopoly(self.player_turn)
