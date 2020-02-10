
# Import useful libraries
import pygame
import random


gameboard_size = width, height = 1024, 576
plane_speed = [5, 0] # [vx, vy]
screen = None

# Load the graphics for the game itself
gameboard_background = pygame.image.load('gameboard.png')
plane = pygame.image.load('airplane.png')
plane_location = plane.get_rect()

pygame.init()


# Initialize the game display (this makes a window appear in which the game is played)
pygame.display.init()

screen = pygame.display.set_mode((gameboard_size))

# In game-speak, "blitting" is "drawing"... let's "blit" the game board!
screen.blit(gameboard_background, (0,0))

# Now let's blit the airplane!
screen.blit(plane, plane_location)
pygame.display.flip()

# Now let's run the gameplay.
run_game = True
while run_game:
    # Check if the user wishes to quit...
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            break

    # Advance the plane using its velocity
    plane_location = plane_location.move(plane_speed)
    
    # See if the plane has moved off the game board; loop it back to the left if it has!
    if plane_location.left >= width:
        plane_location.x -= gameboard_size[0] + plane_location.width
        
    # Update the graphics on the game board
    screen.blit(gameboard_background, (0,0))
    screen.blit(plane, plane_location)
    pygame.display.update()
    pygame.time.delay(10)

    
pygame.display.update()
pygame.time.delay(20)


pygame.display.quit()

