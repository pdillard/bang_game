import random

class Player:
    def __init__(self, name:str, health:int, ammo:int):
        self.name = name
        self.health = health
        self.ammo = ammo

    def input_phases(self, command):
        command = input("Your move: ")
        if command.lower().strip() == "attack":
            if self.ammo >= 1:
                pass

player = Player("Steve", 100, 3)
    