import random
import tkinter

class Player:
    
    def __init__(self, name:str, health:int, ammo:int, move:str):
        self.name = name
        self.health = health
        self.ammo = ammo
        self.move = move

player1 = Player("Steve", 100, 3, None)
player2 = Player("John", 100, 3, None)


def input_phase(Player):
    while True:
        p2_move = random.randint(1, 4)
        print(p2_move)
        command = input("Your move: ")
        if command.lower().strip() == "attack":
            if Player.ammo >= 1 and p2_move not in [1, 2]:
                player2.health -= 25
                player1.ammo -= 1
                print(f"{player2.name} has {player2.health} health")
                if player2.health <= 0:
                    print(f"{player2.name} is dead")
                    break
            elif Player.ammo >= 1 and p2_move in [1, 2]:
                player1.ammo -= 1
                print("John blocked!")
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
        else: 
            print("invalid input")

def attack(attacker, defender):
    if attacker.ammo >= 1 and defender.move not in [1, 2, "block"]:
        defender.health -= 25
        attacker.ammo -= 1
        print(f"")


input_phase(player1)