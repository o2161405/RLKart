from mem_main import get_game_state
import dolphin_memory_engine as DME
import time
from time import sleep
#from mesh import get_raycasts
import os
from mesh_test import calculate_intersect_locations
from pygame_ui import draw_grid_with_intersect_locations
import numpy as np

while not DME.is_hooked():
    print("Not hooked..")
    DME.hook()
    sleep(0.5)

while True:

	t0 = time.time()

	game_state = get_game_state()

	if game_state == None:
		continue

	intersect_locations = calculate_intersect_locations(positions=game_state["Current_Positions"], inbetween_gap=3, definition=65)

	""" Code for adding new things to the overlay:
	numbers = {0}
	for i in intersect_locations:
		numbers.add(round(i[1], 2))
	print(numbers)
	exit()"""


	#print(intersect_locations)
	#print(len(intersect_locations))

	# Pygame Overlay
	#draw_grid_with_intersect_locations(intersect_locations=intersect_locations, grid_size=65, cell_size=10)

	print((time.time() - t0)*1000)

	sleep(0.1)
	#os.system('cls')

# We're doing 0:3 for the agent's view because index 4 and 5 are the quaternion and position info.
# Those two things aren't useful for the AI agent to have, but we still need
# them in the output for when we do the raycasting stuff.

# TODO:
"# - MT charge %age"
"# - Race countdown, 3.0 -> 0.0 then -1"
# - Number of Mushrooms
# - Countdown till wheelie expires? Humans basically have this with the audio cue so it'll be useful.
# - Differentiate between road/offroad/wall when doing angled raycasts/ when character is on an angled slope
# - Raycasts don't change rotation with player (North will always point north no matter what for example)