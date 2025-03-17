import random
import pygame

pygame.init()

WIDTH = 600
HEIGHT = 400
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 155, 255)
GREEN = (0, 255, 0)
FONT = pygame.font.Font(None, 40)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bang Game")


attack_button = pygame.Rect(50, 300, 100, 50)
block_button = pygame.Rect(200, 300, 100, 50)
load_button = pygame.Rect(350, 300, 100, 50)
restart_button = pygame.Rect(450, 300, 120, 50)


def game_screen():
    screen.fill(WHITE)

    player_text = FONT.render(f"You: {player1.health} HP",  True, BLACK)
    cpu_text = FONT.render(f"CPU: {player2.health} HP", True, BLACK)
    screen.blit(player_text, (20, 20))
    screen.blit(cpu_text, (20, 60))

    pygame.draw.rect(screen, RED, attack_button)
    pygame.draw.rect(screen, BLUE, block_button)
    pygame.draw.rect(screen, GREEN, load_button)
    pygame.draw.rect(screen, BLACK, restart_button)

    screen.blit(FONT.render("Attack", True, WHITE), (attack_button.x + 15, attack_button.y + 10))
    screen.blit(FONT.render("Block", True, WHITE), (block_button.x + 15, block_button.y + 10))
    screen.blit(FONT.render("Load", True, WHITE), (load_button.x + 15, load_button.y + 10))
    screen.blit(FONT.render("Restart", True, WHITE), (restart_button.x + 10, restart_button.y + 10))


    if game_over:
        if player1.health <= 0 and player2.health <= 0:
            message = "It's a Tie!"
        elif player2.health <= 0:
            message = "YOU WIN!"
        elif player1.health <= 0:
            message = "YOU LOSE!"

        text_surface = FONT.render(message, True, RED)
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 50))

    pygame.display.flip()



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

def cpu_move_rng(player2):
    move = random.randint(1, 5)

    while True:
        if player2.ammo == 0 and move in [3, 5]:  
            move = random.randint(1, 5) 
        elif player2.ammo >= 3 and move == 4:  
            move = random.randint(1, 5)  
        else:
            break  

    if move in [1, 2]:
        player2.move = "block"
    elif move in [3, 5]:
        player2.move = "attack"
    elif move == 4:
        player2.move = "load"

def replay_ask():
    while True:
        replay = input("Play again? (yes/no): ").strip().lower()
        if replay in ["yes", "no"]:
            return replay
        print("Invalid input. Please enter 'yes' or 'no'.")

player1.name = input("Name: ")

game_over = False
running = True

while running:
    game_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if attack_button.collidepoint(event.pos):
                player1.move = "attack"
                attack(player1, player2)
            elif block_button.collidepoint(event.pos):
                block(player1)
            elif load_button.collidepoint(event.pos):
                load(player1)
            

            cpu_move_rng(player2)
            if player2.move == "attack":
                attack(player2, player1)
            elif player2.move == "block":
                block(player2)
            elif player2.move == "load":
                load(player2)
            

            if player1.health <= 0 or player2.health <= 0:
                game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button.collidepoint(event.pos):
                player1 = Player(player1.name, 100, 0, None)
                player2 = Player("John", 100, 0, None)
                game_over = False

pygame.quit() 