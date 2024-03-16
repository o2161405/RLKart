from mem_main import get_game_state
import dolphin_memory_engine as DME
import time
from time import sleep
import os
from mesh_test import calculate_intersect_locations
from pygame_ui import draw_grid_with_intersect_locations
import numpy as np
import math

# TODO: only calculate Z and return that, faster.
def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x * 57.295779513, pitch_y * 57.295779513, yaw_z * 57.295779513 # in radians

# Hook into Dolphin
while not DME.is_hooked():
    print("Not hooked..")
    DME.hook()
    sleep(0.2)

while True:

	t0 = time.time()

	# Get game state
	game_state = get_game_state()

	# In menus check
	if game_state == None:
		continue

	# 𝑥 by 𝑥 grid output from raycasting
	definition = 75
	# Gap inbetween each ray, measured in meters. Higher value = Less zoom (and less quality)
	inbetween_gap = 1.5

	# Raycast, and then remove unnecessary X and Z component from ray output
	# (Since rays are always looking down, we don't need X and Z)
	intersect_locations = calculate_intersect_locations(positions=game_state["Current_Positions"], inbetween_gap=inbetween_gap, definition=definition)
	intersect_filtered = [round(i[1]) for i in intersect_locations]
	intersect_filtered = np.array(intersect_filtered).reshape(definition, definition)

	""" # Code for adding new things to the overlay:
	numbers = {0}
	for i in intersect_locations:
		numbers.add(round(i[1], 2))
	print(numbers)
	exit()"""

	# Get rotation, since raycasts are always pointing the same direction, the AI agent needs to know where it's looking towards
	x, y, z, w = game_state["Quaternions"]
	# MKW swaps y and z idk
	rotation = round(euler_from_quaternion(x, z, y, w)[2])

	# Pygame Overlay
	draw_grid_with_intersect_locations(intersect_locations=intersect_locations, grid_size=definition, cell_size=10, rotation=rotation)

	print((time.time() - t0)*1000)

	sleep(0.1)


# IGNORE THIS FOR NOW
# We're doing 0:3 for the agent's view because index 4 and 5 are the quaternion and position info.
# Those two things aren't useful for the AI agent to have, but we still need
# them in the output for when we do the raycasting stuff.

# TODO:
"# - MT charge %age"
"# - Race countdown, 3.0 -> 0.0 then -1"
# - Number of Mushrooms
# - Countdown till wheelie expires? Humans basically have this with the audio cue so it'll be useful.
# - Differentiate between road/offroad/wall when doing angled raycasts/ when character is on an angled slope
"# - Raycasts don't change rotation with player (North will always point north no matter what for example)"