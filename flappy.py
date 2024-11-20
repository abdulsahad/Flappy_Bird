import pygame
import sys
import random

# Prepare the Pygame components for launching our game
pygame.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
BIRD_HEIGHT = 40
BIRD_WIDTH = 40
BIRD_COLOR = (255, 0, 0)
PIPE_GAP = 200  #contant gap between the upper and the lower pipe
SCREEN_BG = (255, 255, 255)

# Create a game window of size 1500x750 pixels
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the game window as 'Flappy Bird'
pygame.display.set_caption("Flappy Bird")

# Create clock to get the framespersecond of game (60 FPS)
clock = pygame.time.Clock()

# Bird's class to manage it's behavior
class Bird:

    def __init__(self, a, b, width, height):

        # Bird's position and size (a, b, width, height)
        self.x = 200
        self.y = SCREEN_HEIGHT / 2
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT

        # # The bird velocity (origin) is 0 (it starts stopped)
        self.velocity = 0  

        # Gravity's effect pulling the bird down
        self.gravity = 0.5  
        
        # Bird will jump up if the spacebar is pressed
        self.jump_strength = -7  
        
        # Bird's colour
        self.color = (BIRD_COLOR)

    def jump(self):
        
        # Set the bird's velocity to the jump strength when the spacebar is pressed
        self.velocity = self.jump_strength  # Propel upwards

    def draw(self, screen):
        
        # Render the bird as a red rectangle at its current position
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
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


#--------------------------Pipe class starting--------------------------------
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top = self.height
        self.bottom = self.height + PIPE_GAP
        self.velocity = 5
        self.color = (0, 255, 0)  # Green color for pipes

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, 0, 50, self.top))  #upper pipes
        pygame.draw.rect(screen, self.color, (self.x, self.bottom, 50, SCREEN_HEIGHT - self.bottom)) #Bottom pipes

    def movement(self):
        self.x -= self.velocity

    def update(self):
        self.x -= self.velocity

#-------------------pipe class ending------------------------
    


# Position the bird centrally on the screen (vertically)

bird_x = 100  # The bird starts 100 pixels from the left

bird_y = SCREEN_HEIGHT // 2 - BIRD_HEIGHT // 2  # Center the bird vertically

# Instantiate a bird object with the defined position and size
bird = Bird(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)

pipes = [Pipe()] 

# Begin the main game loop
while True:
    
    # Clear the screen with a white background for each frame
    screen.fill((SCREEN_BG))

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


    #This loop is for pipes updation
    for pipe in pipes:
        pipe.update() 
        pipe.draw() #This called function generate the pipes in loop

    #This will appear new pipes on the screen
    if len(pipes) > 0:  #if there is at least one pipe on the screen
        last_pipe = pipes[-1]
        if last_pipe.x < SCREEN_WIDTH - 300:  # Add new pipe when space is available
            pipes.append(Pipe())


    # Refresh the game display to reflect the updated screen
    pygame.display.update()

    # Frame rate to 60fps
    clock.tick(60)
