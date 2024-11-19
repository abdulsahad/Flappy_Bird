import pygame
import sys

# Prepare the Pygame components for launching our game
pygame.init()

# Create a game window of size 1500x750 pixels
screen = pygame.display.set_mode((1500, 750))

# Set the title of the game window as 'Flappy Bird'
pygame.display.set_caption("Flappy Bird")

# Create clock to get the framespersecond of game (60 FPS)
clock = pygame.time.Clock()

# Bird's class to manage it's behavior
class Bird:

    def __init__(self, a, b, width, height):

        # Bird's position and size (a, b, width, height)
        self.x = a
        self.y = b
        self.width = width
        self.height = height

        # # The bird velocity (origin) is 0 (it starts stopped)
        self.velocity = 0  

        # Gravity's effect pulling the bird down
        self.gravity = 0.5  
        
        # Bird will jump up if the spacebar is pressed
        self.jump_strength = -10  
        
        # Bird's colour
        self.color = (255, 0, 0)  
    
    def update(self):
       
        # Increase the bird's velocity due to gravity
        self.velocity += self.gravity  
        
        # Update the bird's vertical position based on its velocity
        self.y += self.velocity  

        # Enforce boundaries: This prevents the bird from flying above the top
        if self.y <= 0:
            
            self.y = 0  # Keep the bird at the top
            
            self.velocity = 0  # Halt upward movement
        
        # Enforce boundaries: This prevents the bird from falling below the bottom
        elif self.y >= 740 - self.height:
            
            self.y = 740 - self.height  # Limit at the bottom edge
            
            self.velocity = 0  # Halt downward movement

    def jump(self):
        
        # Set the bird's velocity to the jump strength when the spacebar is pressed
        self.velocity = self.jump_strength  # Propel upwards

    def draw(self, screen):
        
        # Render the bird as a red rectangle at its current position
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Define dimensions for the game screen and the bird
screen_width = 800
screen_height = 600
bird_width = 40
bird_height = 40

# Position the bird centrally on the screen (vertically)

bird_x = 100  # The bird starts 100 pixels from the left

bird_y = screen_height // 2 - bird_height // 2  # Center the bird vertically

# Instantiate a bird object with the defined position and size
bird = Bird(bird_x, bird_y, bird_width, bird_height)

# Begin the main game loop
while True:
    
    # Clear the screen with a white background for each frame
    screen.fill((255, 255, 255))

    # Process events (like key presses and closing the window)
    for event in pygame.event.get():
        
        # If the player closes the window
        if event.type == pygame.QUIT:
            
            pygame.quit()  # Terminate Pygame and exit the game
            
            sys.exit()  # Exit the program
        
        # If any key is pressed on the keyboard
        if event.type == pygame.KEYDOWN:
            
            # If the spacebar is pressed, trigger the bird to jump
            if event.key == pygame.K_SPACE:
                
                bird.jump()  # Invoke the bird's jump method 

    # Update the bird's position according to gravity and jumping 
    bird.update()

    # Display the bird on the screen
    bird.draw(screen)

    # Refresh the game display to reflect the updated screen
    pygame.display.update()

    # Frame rate to 60fps
    clock.tick(60)

