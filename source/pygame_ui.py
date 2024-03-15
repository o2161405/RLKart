import pygame

pygame.init()

#OFFROAD = (145, 103, 65)
#ROAD = (180, 180, 180)
#WALL = (0, 0, 0)
#PIPE = (0, 255, 0)
#BOOST = (255, 255, 0)
#UNKNOWN = (255, 0, 0)

def draw_grid_with_intersect_locations(intersect_locations, grid_size, cell_size):

    GRID_SIZE = grid_size
    CELL_SIZE = cell_size
    WINDOW_SIZE = (GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE)

    screen = pygame.display.set_mode(WINDOW_SIZE)

    def draw_grid(grid_1d):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Calculate the index in the 1D array
                index = row * GRID_SIZE + col

                # Get the value from the 1D array
                cell_value = grid_1d[index][1]

                # Calculate the cell's coordinates
                x = col * CELL_SIZE
                y = row * CELL_SIZE

                # Set the cell color based on the value
                match round(cell_value, 2):
                    case 0:
                        cell_color = (145, 103, 65)
                    case 10:
                        cell_color = (180, 180, 180)
                    case 11:
                        cell_color = (255, 255, 0)
                    case 12:
                        cell_color = (0, 255, 0)
                    case 13:
                        cell_color = (0, 0, 0)
                    case 17:
                        cell_color = (255, 0, 0)
                    case other:
                        cell_color = (0, 0, 0)

                # Draw the cell with the chosen color
                pygame.draw.rect(screen, cell_color, (x, y, CELL_SIZE, CELL_SIZE))

    """running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False"""

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the grid
    draw_grid(intersect_locations)

    # Update the display
    pygame.display.update()

    #pygame.quit()