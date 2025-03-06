import random
import tkinter as tk

class Player:
    
    def __init__(self, name:str, health:int, ammo:int, move:str):
        self.name = name
        self.health = health
        self.ammo = ammo
        self.move = move

player1 = Player("You", 100, 0, None)
player2 = Player("John", 100, 0, None)


# def input_phase(Player):
#     while True:
#         p2_move = random.randint(1, 4)
#         print(p2_move)
#         command = input("Your move: ")
#         if command.lower().strip() == "attack":
#             if Player.ammo >= 1 and p2_move not in [1, 2]:
#                 player2.health -= 25
#                 player1.ammo -= 1
#                 print(f"{player2.name} has {player2.health} health")
#                 if player2.health <= 0:
#                     print(f"{player2.name} is dead")
#                     break
#             elif Player.ammo >= 1 and p2_move in [1, 2]:
#                 player1.ammo -= 1
#                 print("John blocked!")
#             else:
#                 print("no ammo")
#         elif command.lower().strip() == "block":
#             pass
#         elif command.lower().strip() == "load":
#             if Player.ammo < 3:
#                 player1.ammo += 1
#                 print("loaded")
#             else:
#                 print("no effect")
#         else: 
#             print("invalid input")

def attack(attacker, defender):
    attacker.move = "attack"
    if attacker.ammo >= 1 and defender.move not in [1, 2, "block"]:
        defender.health -= 50
        attacker.ammo -= 1
        print(f"{attacker.name} attacks")
        return print(f"{defender.name} has {defender.health} health!")
    elif attacker.ammo == 0:
        return print("no ammo")
    else:
        attacker.ammo -= 1
        return print("blocked!")
    
def block(Player):
    Player.move = "block"
    return print(f"{Player.name} blocks")

def load(Player):
    Player.move = "load"
    if Player.ammo < 3:
        Player.ammo += 1
        return print(f"{Player.name} loads")

    else:
        return print("no effect")

def cpu_move_rng(Player):
    move = random.randint(1, 4)
  
    while True:
        if Player.ammo >= 3 and move == 4:
            move = random.randint(1, 4)
        elif Player.ammo == 0 and move == 3:
            move = random.randint(1, 4)
        else:
            break
        
    #print(move)

    if move in [1, 2]:
        Player.move = "block"
    elif move == 3:
        Player.move = "attack"
    elif move == 4:
        Player.move = "load"
    else:
        print("error")
    pass

def replay_ask():
    replay = input("Play again? (yes/no) ")
    if replay.strip().lower() == "yes":
        return "yes"
    if replay.strip().lower() == "no":
        return "no"

player1.name = input("Name: ")

while True:

    print("_________________________________")
    cpu_move_rng(player2)
    # p2_move = random.randint(1, 4)
    # print(p2_move)
    # while True:
    #     if player2.ammo >= 3 and p2_move == 4:
    #         p2_move = random.randint(1, 4)
    #     elif player2.ammo == 0 and p2_move == 3:
    #         p2_move = random.randint(1, 4)
    #     else:
    #         break

    # if p2_move in [1, 2]:
    #     player2.move = "block"
    # elif p2_move == 3:
    #     player2.move = "attack"
    # elif p2_move == 4:
    #     player2.move = "load"
    # else:
    #     print("error")
    
    command = input("Your move: ")
    player1.move = command.strip().lower()
    if player1.move == "attack":
        attack(player1, player2)
    elif player1.move == "block":
        block(player1)
    elif player1.move == "load":
        load(player1)
    else:
        print("invalid input")

    if player2.move == "attack":
        attack(player2, player1)
    elif player2.move == "block":
        block(player2)
    elif player2.move == "load":
        load(player2)
    else:
        print("error")

    if player2.health <= 0 and player1.health <= 0:
        print("TIE!")
        replay = input("Play again? (yes/no) ")
        if replay.strip().lower() == "yes":
            player1 = Player("Steve", 100, 0, None)
            player2 = Player("John", 100, 0, None)
            player1.name = input("Name: ")
            pass
        if replay.strip().lower() == "no":
            break
    elif player2.health <= 0:
        print("YOU WIN!")
        replay = input("Play again? (yes/no) ")
        if replay.strip().lower() == "yes":
            player1 = Player("Steve", 100, 0, None)
            player2 = Player("John", 100, 0, None)
            player1.name = input("Name: ")
            pass
        if replay.strip().lower() == "no":
            break
    elif player1.health <= 0:
        print ("YOU LOSE")
        replay = input("Play again? (yes/no) ")
        if replay.strip().lower() == "yes":
            player1 = Player("Steve", 100, 0, None)
            player2 = Player("John", 100, 0, None)
            player1.name = input("Name: ")
            pass
        if replay.strip().lower() == "no":
            break
    else:
        pass


# root = tk.Tk()
# root.title("Bang Game)
# root.geometry("350x350")

# def on_click():
    # pass

# btn = tk.button(root, text = "")