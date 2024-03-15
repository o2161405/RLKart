import trimesh
import numpy as np
import time
import pygame

mesh = trimesh.load('../model/a_final.obj', force='mesh')

#X, Y, Z = [-12203.0, 1060.51611328125, -2954.655029296875]
X, Y, Z = [-12203, 1061, -2955]
X, Y, Z = X/100, Y/100, Z/100

inbetween_gap = 3
definition = 65 # 15x15 grid

ray_origins = np.array([[0, 0, 0]]) # We need at least 1 element in here
ray_offset = (((definition * inbetween_gap) / 2) - (inbetween_gap / 2))

t0 = time.time()

rays = []
for i in range(1, definition + 1):
	for j in range(1, definition + 1):
		new_ray = np.array([
			(X + (i * inbetween_gap) - inbetween_gap) - ray_offset,
			Y + 10,
			(Z + (j * inbetween_gap) - inbetween_gap) - ray_offset,
			])
		rays.append(new_ray)
ray_origins = np.vstack((ray_origins, rays))

"""locations, index_ray, index_tri = mesh.ray.intersects_location(
        ray_origins=ray_origins,
        ray_directions=ray_directions)"""

ray_origins = ray_origins[1:]
ray_directions = np.tile(np.array([0, -1, 0]), (ray_origins.shape[0], 1))

intersect_locations = mesh.ray.intersects_id(
        ray_origins=ray_origins,
        ray_directions=ray_directions,
        multiple_hits=False,	
        max_hits=1,
        return_locations=True)[2]

t1 = time.time()

#ray_visualize = trimesh.load_path(np.hstack((ray_origins,
                                             #ray_origins + ray_directions*20.0)).reshape(len(ray_origins), 2, 3))
#for i in intersect_locations:
	#print(i)
#print(len(intersect_locations))
print((t1-t0)*1000)

#mesh.unmerge_vertices()
#mesh.visual.face_colors = [255,255,255,255]
#scene = trimesh.Scene([mesh, ray_visualize])
#scene.show()

pygame.init()

OFFROAD = (145, 103, 65)
ROAD = (180, 180, 180)
WALL = (0, 0, 0)
UNKNOWN = (255, 255, 255)

GRID_SIZE = definition
CELL_SIZE = 10

WINDOW_SIZE = (GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption(f"{definition}x{definition} Grid")

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
                	cell_color = OFFROAD
                case 10:
                	cell_color = ROAD
                case 13:
                	cell_color = WALL
                case other:
                	cell_color = UNKNOWN

            # Draw the cell with the chosen color
            pygame.draw.rect(screen, cell_color, (x, y, CELL_SIZE, CELL_SIZE))

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the grid
    draw_grid(intersect_locations)

    # Update the display
    pygame.display.flip()

pygame.quit()