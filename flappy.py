import pygame
import sys
import random

# Initializing Pygame to use it's tools
pygame.init()

# Dimensions of the game window  (WIDTH & HEIGHT)
WIND_WIDTH = 1500  # SCREEN'S WIDTH
WIND_HEIGHT = 760  # SCREEN'S HEIGHT

# The dimensions and appearance of the bird
B_WIDTH = 40 # BIRD WIDTH
B_HEIGHT = 40 # BIRD HEIGHT
B_COLOR = (255, 50, 50)  # BIRD COLOR

# PIP'S GAP AND SPEED
PIP_GAP = 220  # Distance BETWEEN THE TOP PIPE AND BOTTOM PIPE
PIP_SPEED = 5  # HOW FAST THE PIPE MOVES 

# Background color for the game
BG_COLOR = (200, 220, 220)  

# Create the game window
screen = pygame.display.set_mode((WIND_WIDTH, WIND_HEIGHT))
pygame.display.set_caption("OUR FLAPPY BIRD")
game_clock = pygame.time.Clock()  # Controls game speed

# Define the Bird class to manage the player's character
class Bird:
    def __init__(self, x, y):
        self.x = x  # Starting horizontal position
        self.y = y  # Starting vertical position
        self.width = B_WIDTH
        self.height = B_HEIGHT
        self.color = B_COLOR
        self.gravity = 0.5  # How strong gravity will pull the bird down
        self.lift = -7  # Upward force applied when the bird jumps up
        self.vertical_speed = 0  # Tracks the bird's up/down speed

    def jump(self):
        """Trigger a jump by applying upward velocity."""
        self.vertical_speed = self.lift

    def update_position(self):
        """Update the bird's location based on physics."""
        self.vertical_speed += self.gravity  # Gravity affects speed
        self.y += self.vertical_speed  # Update position based on speed

        # Prevent the bird from flying off the top or bottom of the screen
        if self.y < 0:
            self.y = 0
        if self.y > WIND_HEIGHT - self.height:
            self.y = WIND_HEIGHT - self.height

    def draw(self):
        """Render the bird on the screen."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Pipe class to create moving obstacles
class Pipe:
    def __init__(self):
        self.x = WIND_WIDTH  # Pipes begin at the far right of the screen
        self.height = random.randint(100, WIND_HEIGHT - PIP_GAP - 100)  # Random gap position
        self.top_height = self.height  # Height of the top pipe
        self.bottom_start = self.height + PIP_GAP  # Start position of the bottom pipe
        self.color = (0, 200, 0)  # PIPE COLOR
        self.width = 50  # Pipe width
        self.scored = False  # Keep track of whether the bird has passed this pipe

    def move(self):
        """Shift the pipe leftward at a constant speed."""
        self.x -= PIP_SPEED

    def draw(self):
        """Render the pipe on the screen."""
        # Draw the top pipe
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.top_height))
        # Draw the bottom pipe
        pygame.draw.rect(screen, self.color, (self.x, self.bottom_start, self.width, WIND_HEIGHT - self.bottom_start))

# Function to show a game-over message
def show_game_over(score):
    """Display a 'Game Over' screen with the player's final score."""
    font = pygame.font.Font(None, 72)
    message = font.render("Game Over!", True, (200, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
    restart_message = font.render("Press R to Restart or Q to Quit", True, (50, 50, 50))

# Start an infinite loop to keep the screen active
    while True:
        # Fill the screen with the background color
        screen.fill(BG_COLOR)
        # Display the main message in the center of the screen
        screen.blit(message, (WIND_WIDTH // 2 - message.get_width() // 2, 200))
        # Display the score text in the center of the screen
        screen.blit(score_text, (WIND_WIDTH // 2 - score_text.get_width() // 2, 300))
        
        # Display the restart message in the center of the screen
        screen.blit(restart_message, (WIND_WIDTH // 2 - restart_message.get_width() // 2, 400))                 
        # Update display to show drawn elements
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If the user shuts the window (pygame.QUIT event) quit the game
                pygame.quit() # Uninitializing Pygame
                sys.exit() # EXIT THE PROGRAM

            # KEY PRESSES EVENTS 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # If the 'R' key is pressed
                    return  # Restart the game

                elif event.key == pygame.K_q: # If the 'Q' key is pressed game closes
                    pygame.quit() # Uninitializing Pygame
                    sys.exit() # PROGRAM EXIT


# To handle the countdown before the game starts
def countdown():
    """Display a countdown to build anticipation."""
    font = pygame.font.Font(None, 72)
    for num in range(3, 0, -1):
        screen.fill(BG_COLOR)
        text = font.render(str(num), True, (200, 0, 0))
        screen.blit(text, (WIND_WIDTH // 2 - text.get_width() // 2, WIND_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(1000)

# GAMES'S MAIN FUNCTION
def game_loop():
    """Run the main game logic."""
    countdown()
    bird = Bird(200, WIND_HEIGHT // 2)
    pipes = [Pipe()]  # GAME Starts with one pipe
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        screen.fill(BG_COLOR)

        # If the user clicks the close button on the game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Update bird position and render it
        bird.update_position()

        # If bird touches the top or bottom
        if bird.y <= 0 or bird.y >= WIND_HEIGHT - bird.height:
            show_game_over(score)
            return

        bird.draw()

        # UPDATING THE POSTION OF THE PIPES
        for pipe in pipes:
            pipe.move()
            pipe.draw()

            # If bird collides with the pipe
            if (pipe.x < bird.x + bird.width < pipe.x + pipe.width) and \
               (bird.y < pipe.top_height or bird.y + bird.height > pipe.bottom_start):
                show_game_over(score)
                return

            # If bird passes the pipe (scoring)
            if not pipe.scored and bird.x > pipe.x + pipe.width:
                score += 1
                pipe.scored = True

        # NEW PIPES ADDED WHEN NEEDED
        if pipes[-1].x < WIND_WIDTH - 300:
            pipes.append(Pipe())

        # PIPE moved off the screen (REMOVED OFF THE SCRREN)
        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        # Score of the game is showing in the corner of the screen
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        game_clock.tick(60)

# Run the game
while True:
    game_loop()
