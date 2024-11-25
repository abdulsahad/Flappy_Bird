import pygame
import sys
import random

pygame.init()
# This is the window dimensions and constants
WIND_WIDTH = 1500
WIND_HEIGHT = 760
BIRD_HEIGHT = 40
BIRD_WIDTH = 40
BIRD_COLOR = (250, 0, 0)
GAP_BETWEEN_PIPES = 220 # Gap between the top and bottom pipes
SCREEN_BGD = (255, 255, 255) # background color 

# Game window setting up
screen = pygame.display.set_mode((WIND_WIDTH, WIND_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# This is the Bird class (defining bird properties and behavior)
class Bird:
    def __init__(self, a, b, width, height):
        # Bird position, size, and movement
        self.x = a  # Horizontal Position
        self.y = b  # Vertical Position
        self.width = width  # Width of the bird
        self.height = height  # Height of the bird
        self.velocity = 0  # The current vertical velocity
        self.gravity = 0.5  # Pulling the bird down due to gravity force
        self.jump_strength = -7  # The force applied when the bird jumps
        self.c = BIRD_COLOR  # Color of the bird

    def jump(self):
        # Trigger the bird to jump by applying an upward velocity
        self.velocity = self.jump_strength
        
    #This function draws the bird on screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.c, (self.x, self.y, self.width, self.height))

    #This fucntion updates every new changes commited by the user
    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y <= 0:  # Prevent the bird from moving out of bounds
            self.y = 0
            self.velocity = 0
        elif self.y >= WIND_HEIGHT - self.height:  # Keep the bird within the screen
            self.y = WIND_HEIGHT - self.height
            self.velocity = 0

# The Pipe's class
class Pipe:
    def __init__(self):
        self.x = WIND_WIDTH
        self.height = random.randint(100, WIND_HEIGHT - GAP_BETWEEN_PIPES - 100)
        self.top = self.height
        self.bottom = self.height + GAP_BETWEEN_PIPES
        self.velocity = 5
        self.color = (0, 255, 0)
        self.scored = False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, 0, 50, self.top))  # Upper pipe
        pygame.draw.rect(screen, self.color, (self.x, self.bottom, 50, WIND_HEIGHT - self.bottom))  # Bottom pipe

    def update(self):
        self.x -= self.velocity

def game_over_screen(score):
    font = pygame.font.Font(None, 72)
    game_over_surface = font.render("Game Over!", True, (255, 0, 0))
    score_surface = font.render(f"Your Score: {score}", True, (0, 0, 0))
    restart_surface = font.render("Press R to Restart or Q to Quit", True, (0, 0, 0))

    screen.fill(SCREEN_BGD)
    screen.blit(game_over_surface, (WIND_WIDTH // 2 - game_over_surface.get_width() // 2, 200))
    screen.blit(score_surface, (WIND_WIDTH // 2 - score_surface.get_width() // 2, 300))
    screen.blit(restart_surface, (WIND_WIDTH // 2 - restart_surface.get_width() // 2, 400))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Restart game
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    bird = Bird(200, WIND_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
    pipes = [Pipe()]
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        screen.fill(SCREEN_BGD)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Update bird
        bird.update()
        bird.draw(screen)

        # Update and draw pipes
        for pipe in pipes:
            pipe.update()
            pipe.draw()

            # Check for collisions
            if (bird.x + bird.width > pipe.x and bird.x < pipe.x + 50) and \
               (bird.y < pipe.top or bird.y + bird.height > pipe.bottom):
                game_over_screen(score)
                return  # Restart main function

            # Check if bird passes through pipe
            if not pipe.scored and bird.x > pipe.x + 50:
                score += 1
                pipe.scored = True

        # Add new pipes and remove off-screen pipes
        if pipes[-1].x < WIND_WIDTH - 300:
            pipes.append(Pipe())
        pipes = [pipe for pipe in pipes if pipe.x + 50 > 0]

        # Check if bird hits the ground
        if bird.y >= WIND_HEIGHT - bird.height or bird.y <= 0:
            game_over_screen(score)
            return  # Restart main function

        # Display score
        score_surface = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_surface, (10, 10))

        # Update display
        pygame.display.update()
        clock.tick(60)

# Run the game loop
while True:
    main()
