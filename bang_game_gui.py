import random
import pygame

pygame.init()


WIDTH = 600
HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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
name_input_box = pygame.Rect(200, 150, 200, 50)


name_input_mode = True
player_name = ""
game_messages = []

sprite_org = pygame.image.load("still_icon.png")
sprite_scale = pygame.transform.scale(sprite_org, (150,150))
sprite_image = pygame.transform.flip(sprite_scale, True, False)


class Player(pygame.sprite.Sprite):
    def __init__(self, name, health, ammo, move):
        self.name = name
        self.health = health
        self.ammo = ammo
        self.move = move
        super().__init__()
        self.image = pygame.image.load("still_icon.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)




player1 = Player("", 100, 0, None)
player2 = Player("John", 100, 0, None)

def draw_text(text, position, color=BLACK):
    text_surface = FONT.render(text, True, color)
    screen.blit(text_surface, position)

def add_message(message):
    """Adds a new message to the game log."""
    game_messages.append(message)
    if len(game_messages) > 5: 
        game_messages.pop(0)

def game_screen():
    screen.fill(WHITE)
    draw_text(f"{player_name}: {player1.health} HP", (20, 20))
    draw_text(f"CPU: {player2.health} HP", (20, 60))

    pygame.draw.rect(screen, RED, attack_button)
    pygame.draw.rect(screen, BLUE, block_button)
    pygame.draw.rect(screen, GREEN, load_button)
    pygame.draw.rect(screen, BLACK, restart_button)

    draw_text("Attack", (attack_button.x + 15, attack_button.y + 10), WHITE)
    draw_text("Block", (block_button.x + 15, block_button.y + 10), WHITE)
    draw_text("Load", (load_button.x + 15, load_button.y + 10), WHITE)
    draw_text("Restart", (restart_button.x + 10, restart_button.y + 10), WHITE)


    y_offset = 20  
    for msg in game_messages:
        draw_text(msg, (WIDTH // 2, y_offset))
        y_offset += 25  

    if game_over:
        message = "It's a Tie!" if player1.health <= 0 and player2.health <= 0 else "YOU WIN!" if player2.health <= 0 else "YOU LOSE!"
        draw_text(message, (WIDTH // 2 - 50, HEIGHT // 2 - 50), RED)

    pygame.display.flip()

def attack(attacker, defender):
    attacker.move = "attack"
    if attacker.ammo >= 1 and defender.move != "block":
        defender.health -= 100
        attacker.ammo -= 1
        add_message(f"{attacker.name} attacks! {defender.name} takes damage!")
    elif attacker.ammo == 0:
        add_message(f"{attacker.name} has no ammo!")
    else:
        attacker.ammo -= 1
        add_message(f"{defender.name} blocks the attack!")

def block(player):
    player.move = "block"
    add_message(f"{player.name} blocks!")

def load(player):
    player.move = "load"
    if player.ammo < 3:
        player.ammo += 1
        add_message(f"{player.name} loads ammo!")
    else:
        add_message(f"{player.name} can't load more ammo!")

def cpu_move():
    moves = ["block", "attack", "load"]
    if player2.ammo == 0:
        moves = ["block", "load"]

    if player2.ammo == 3:
        moves = ["block", "attack"]

    move = random.choice(moves)
    player2.move = move

def menu_screen():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)

        title_text = FONT.render("Bang Game", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        start_button = pygame.Rect(WIDTH // 2 - 75, 150, 150, 50)
        instructions_button = pygame.Rect(WIDTH // 2 - 75, 220, 150, 50)
        quit_button = pygame.Rect(WIDTH // 2 - 75, 290, 150, 50)

        pygame.draw.rect(screen, GREEN, start_button)
        pygame.draw.rect(screen, BLUE, instructions_button)
        pygame.draw.rect(screen, RED, quit_button)

        screen.blit(FONT.render("Start", True, WHITE), (start_button.x + 40, start_button.y + 10))
        screen.blit(FONT.render("Instructions", True, WHITE), (instructions_button.x + 10, instructions_button.y + 10))
        screen.blit(FONT.render("Quit", True, WHITE), (quit_button.x + 40, quit_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    menu_running = False
                elif instructions_button.collidepoint(event.pos):
                    instructions_screen()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def instructions_screen():
    instructions_running = True
    while instructions_running:
        screen.fill(WHITE)
        
        instructions = [
            "How to Play:",
            "Attack: Use bullets to damage the CPU.",
            "Block: Prevents CPU from attacking you.",
            "Load: Gain more bullets for attack.",
            "First to reach 0 HP loses!"
        ]

        for i, text in enumerate(instructions):
            screen.blit(FONT.render(text, True, BLACK), (50, 50 + i * 50))

        back_button = pygame.Rect(WIDTH // 2 - 50, 300, 100, 50)
        pygame.draw.rect(screen, RED, back_button)
        screen.blit(FONT.render("Back", True, WHITE), (back_button.x + 20, back_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                instructions_running = False


menu_screen()

game_over = False
running = True

while running:
    screen.fill(WHITE)

    if name_input_mode:
        draw_text("Enter Your Name:", (200, 100))
        pygame.draw.rect(screen, BLACK, name_input_box, 2)
        draw_text(player_name, (name_input_box.x + 10, name_input_box.y + 10))
    else:
        game_screen()
        screen.blit(sprite_image, (100,150))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if name_input_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name.strip():
                    player1.name = player_name
                    name_input_mode = False
                    add_message(f"Welcome, {player_name}!")
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        elif not game_over:
            
            cpu_move()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if attack_button.collidepoint(event.pos):
                    attack(player1, player2)
                elif block_button.collidepoint(event.pos):
                    block(player1)
                elif load_button.collidepoint(event.pos):
                    load(player1)


                if player2.move == "attack":
                    attack(player2, player1)
                elif player2.move == "block":
                    block(player2)
                elif player2.move == "load":
                    load(player2)

                if player1.health <= 0 or player2.health <= 0:
                    game_over = True
                    add_message("Game Over!")

        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button.collidepoint(event.pos):
                player1 = Player(player1.name, 100, 0, None)
                player2 = Player("John", 100, 0, None)
                game_over = False
                game_messages.clear()
                add_message("Game restarted!")

pygame.quit()