"""
Monopoly Implementation
"""
import typing


class Property():


    def __init__(self, color: Tuple[int, int, int], name: str, 
        pos: Tuple[int, int], cost, r0: int, r1: int, r2: int, r3: int, r4: int, 
        rh: int, hp: int):
        
        self.color = color
        self.name = name
        self.pos = pos

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
    
    def rent(self) -> int:
        return self.rents[self.house]
    def build_house(self) -> None:
        self.house += 1
    

class Piece():
    raise NotImplementedError

class Player():
    def __init__(self, pnum: int, money: int, piece: Piece):
        self.pnum = pnum
        self.money = money
        self.piece = piece


class Monopoly():



class Chance():
    


class Community_Chest():



