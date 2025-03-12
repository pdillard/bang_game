import random
import pygame

WIDTH = 600
HEIGHT = 400
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (0, 0, 255)
BLUE = (0, 155, 255)
GREEN = (0, 255, 0)

# screen = pygame.display.set_mode(WIDTH, HEIGHT)
# pygame.display.set_caption("Bang Game")

# font = pygame.font.Font(None, 40)

# attack_button = pygame.Rect(50, 300, 100, 50)
# block_button = pygame.Rect(200, 300, 100, 50)
# load_button = pygame.Rect(350, 300, 100, 50)
# restart_button = pygame.Rect(450, 300, 120, 50)



class Player:
    
    def __init__(self, name:str, health:int, ammo:int, move:str):
        self.name = name
        self.health = health
        self.ammo = ammo
        self.move = move

player1 = Player("You", 100, 0, None)
player2 = Player("John", 100, 0, None)

def attack(attacker, defender):
    attacker.move = "attack"
    if attacker.ammo >= 1 and defender.move not in [1, 2, "block"]:
        defender.health -= 100
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
    
    move = random.randint(1, 5)

    while True:

        if Player.ammo >= 3 and move == 4:
            move = random.randint(1, 5)
        elif Player.ammo == 0 and move == 3:
            move = random.randint(1, 5)
        else:
            break

    if move in [1, 2]:
        Player.move = "block"
    elif move in [3, 5]:
        Player.move = "attack"
    elif move == 4:
        Player.move = "load"

def replay_ask():
    while True:
        replay = input("Play again? (yes/no): ").strip().lower()
        if replay in ["yes", "no"]:
            return replay
        print("Invalid input. Please enter 'yes' or 'no'.")

player1.name = input("Name: ")

while True:

    print("_________________________________")
    if player1.ammo == 0 and player2.ammo < 2:
        player2.move = "load"
    else:
        cpu_move_rng(player2)

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
    elif player2.move == None:
        print("did not generate")
    else:
        print("cpu error")

    # if player2.health <= 0 and player1.health <= 0:
    #     print("TIE!")
    #     replay = input("Play again? (yes/no) ")
    #     if replay.strip().lower() == "yes":
    #         player1 = Player("Steve", 100, 0, None)
    #         player2 = Player("John", 100, 0, None)
    #         player1.name = input("Name: ")
    #         pass
    #     if replay.strip().lower() == "no":
    #         break
    # elif player2.health <= 0:
    #     print("YOU WIN!")
    #     replay = input("Play again? (yes/no) ")
    #     if replay.strip().lower() == "yes":
    #         player1 = Player("Steve", 100, 0, None)
    #         player2 = Player("John", 100, 0, None)
    #         player1.name = input("Name: ")
    #         pass
    #     if replay.strip().lower() == "no":
    #         break
    # elif player1.health <= 0:
    #     print ("YOU LOSE")
    #     replay = input("Play again? (yes/no) ")
    #     if replay.strip().lower() == "yes":
    #         player1 = Player("Steve", 100, 0, None)
    #         player2 = Player("John", 100, 0, None)
    #         player1.name = input("Name: ")
    #         pass
    #     if replay.strip().lower() == "no":
    #         break
    # else:
    #     pass
    if player1.health <= 0 and player2.health <= 0:
        print("It's a tie!")
    elif player2.health <= 0:
        print("YOU WIN!")
    elif player1.health <= 0:
        print("YOU LOSE!")

    if player1.health <= 0 or player2.health <= 0:
        if replay_ask() == "no":
            break
        player1, player2 = Player(input("Enter your name: ")), Player("John")