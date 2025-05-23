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
sprite_scale = pygame.transform.scale(sprite_org, (150, 150))
sprite_image = pygame.transform.flip(sprite_scale, True, False)

class Player(pygame.sprite.Sprite):
    def __init__(self, name, health, ammo, move):
        super().__init__()
        self.name = name
        self.health = health
        self.ammo = ammo
        self.move = move

        # Load all animation frames
        scale_factor = 1.3  # Adjust this to make sprites bigger

        self.animations = {
            "idle": [
                pygame.transform.scale(pygame.image.load("still_icon.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
            ],
            "attack": [
                pygame.transform.scale(pygame.image.load("still_icon.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
                pygame.transform.scale(pygame.image.load("2you_shoot.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
                pygame.transform.scale(pygame.image.load("3you_shoot.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
            ],
            "load": [
                pygame.transform.scale(pygame.image.load("you_load.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
                pygame.transform.scale(pygame.image.load("2you_load.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
                pygame.transform.scale(pygame.image.load("3you_load.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
            ],
            "block": [
                pygame.transform.scale(pygame.image.load("still_icon.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
                pygame.transform.scale(pygame.image.load("2block.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
                pygame.transform.scale(pygame.image.load("3block.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
            ],
            "dead" : [
                pygame.transform.scale(pygame.image.load("dead.png").convert_alpha(), (150*scale_factor, 150*scale_factor)),
            ]
        }

        # Function to flip images
        def flip_images(images):
            return [pygame.transform.flip(img, True, False) for img in images]

        # Flip player1's images
        if name == "":  # Assuming player1 has an empty name initially
            for key in self.animations:
                self.animations[key] = flip_images(self.animations[key])

        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_speed = 700  # Adjust speed of animation playback
        self.image = self.animations[self.current_animation][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)
        self.animation_counter = 0  # Frame timing control

    def update_animation(self):
        self.animation_counter += 1

        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0  # Reset counter
            self.frame_index += 1  # Move to the next frame

            # Loop animation if needed
            if self.frame_index >= len(self.animations[self.current_animation]):
                self.frame_index = 0
                if self.current_animation != "dead":
                    self.current_animation = "idle"  # Return to idle after animation completes

            self.image = self.animations[self.current_animation][self.frame_index]

    def set_animation(self, action):
        """Change animation when an action is performed."""
        if action in self.animations:
            self.current_animation = action
            self.frame_index = 0
            self.animation_counter = 0


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
        attacker.set_animation("attack")
        defender.health -= 50
        attacker.ammo -= 1
        if defender.health <= 0:
            defender.set_animation("dead")  # Change to dead animation
    elif attacker.ammo == 0:
        attacker.set_animation("idle")
        add_message(f"{attacker.name} has no ammo!")
    else:
        attacker.set_animation("attack")
        attacker.ammo -= 1

def block(player):
    player.set_animation("block")
    player.move = "block"

def load(player):
    player.move = "load"
    if player.ammo < 3:
        player.ammo += 1
        player.set_animation("load")
    else:
        player.set_animation("idle")
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
        screen.blit(FONT.render("Back", True, WHITE), (back_button.x + 30, back_button.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    instructions_running = False

# Main game loop
running = True
game_over = False

menu_screen()

while running:
    screen.fill(WHITE)

    if name_input_mode:
        draw_text("Enter Your Name:", (200, 100))
        pygame.draw.rect(screen, BLACK, name_input_box, 2)
        draw_text(player_name, (name_input_box.x + 10, name_input_box.y + 10))
    else:
        game_screen()

        player1.update_animation()
        player2.update_animation()

        screen.blit(player1.image, player1.rect.topleft)
        screen.blit(player2.image, (400, 100))

    pygame.display.flip()
    print("flip")

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

                if player1.health <= 0:
                    player1.set_animation("dead")
                if player2.health <= 0:
                    player2.set_animation("dead")

        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button.collidepoint(event.pos):
                player1 = Player("", 100, 0, None)
                player2 = Player("John", 100, 0, None)
                name_input_mode = False
                game_over = False
                game_messages.clear()
                add_message("Game restarted!")

pygame.quit()

