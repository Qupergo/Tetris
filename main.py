import pygame
import pygame.time
import time

pygame.init()
clock = pygame.time.Clock()


board = []
rows = 10
cols = 20
size = 25

for y in range(cols):
    board.append([])
    for x in range(rows):
        board[y].append(0)

print(board)


O = "../.."
I = "...."
L = "./..."
J = "ss./..."
Z = "../s.."
S = "s../.."

def draw_block(block_string, color, pos):
    x, y = 0, 0
    block_grid = []
    for char in block_string:
        if char == ".":
            block_grid.append([x, y])
            x += 1

        elif char == "/":
            y += 1
            x = 0

        elif char == "s":
            x += 1
    total_rect = []
    for grid_pos in block_grid:
        pygame.draw.rect(screen, color, (pos[0] + grid_pos[0]*size, pos[1] + grid_pos[1]*size, size, size))

        # TODO: fix double outline between blocks
        pygame.draw.rect(screen, (0,0,0), (pos[0] + grid_pos[0]*size, pos[1] + grid_pos[1]*size, size, size), 1)
    





# Set up the drawing window
width = 400
height = 750
screen = pygame.display.set_mode([width, height])

# Run until the user asks to quit
running = True
current_pos = {"x":0, "y":0}
frames = 0

slowness_default = 15
slowness = slowness_default

while running:

    frames += 1
    dt = clock.tick(20)
    if frames % slowness == 0:
        current_pos["y"] += size
    
    
    slowness = slowness_default
        

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                if current_pos["x"] < size:
                    current_pos["x"] = 0
                else:
                    current_pos["x"] -= size

            elif event.key == pygame.K_d:
                
                if (current_pos["x"]) >= width - (2 * size):
                    current_pos["x"] = width - (2 * size)
                else:
                    current_pos["x"] += size

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draws the block, TODO: Random block.
    print(draw_block(O, (255, 255, 0), (current_pos["x"], current_pos["y"])))

    pygame.display.flip()

# Done! Time to quit.
pygame.quit()