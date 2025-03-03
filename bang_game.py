import random
import tkinter

class Player:
    
    def __init__(self, name:str, health:int, ammo:int):
        self.name = name
        self.health = health
        self.ammo = ammo


player1 = Player("Steve", 100, 3)
player2 = Player("John", 100, 3)
    
def input_phase(Player):
    while True:
        command = input("Your move: ")
        if command.lower().strip() == "attack":
            if Player.ammo >= 1:
                player2.health -= 5
                player1.ammo -= 1
                print(f"{player2.name} has {player2.health}")
                if player2.health <= 0:
                    print(f"{player2.name} is dead")
                    break
            else:
                print("no ammo")
        elif command.lower().strip() == "block":
            pass
        elif command.lower().strip() == "load":
            if Player.ammo < 3:
                player1.ammo += 1
                print("loaded")
            else:
                print("no effect")
            

input_phase(player1)