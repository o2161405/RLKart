from mem_main import get_game_state
import dolphin_memory_engine as DME
from time import sleep, time
import os
import numpy as np
import math
from mesh import mesh_normalized_ray_lengths

def euler_from_quaternion(x, y, z, w):
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return yaw_z * 57.295779513

# Hook into Dolphin
while not DME.is_hooked():
    print("Not hooked..")
    DME.hook()
    sleep(0.2)

while True:

	t0 = time()

	# Get game state
	game_state = get_game_state()

	# In menus check
	if game_state == None:
		continue

	# Get rotation, since raycasts are always pointing the same direction, the AI agent needs to know where it's looking towards
	x, y, z, w = game_state["Quaternions"]
	# MKW swaps y and z idk
	rotation = euler_from_quaternion(x, z, y, w)

	full_rays, road_rays, offroad_check = mesh_normalized_ray_lengths(game_state["Current_Positions"], 100, rotation, False)

	print((time()-t0)*1000)

	###
	# Print the NORMALIZED information the agent will get
	print(f"""XZ_SPEED: {round(game_state["XZ_Speed"]/120, 6)}
RaceCompletion: {game_state["Race_Completion"]/4}
MT_Charge: {game_state["MT_Charge"]}
Countdown: {game_state["Countdown"]/4}
Shrooms: {game_state["Shrooms"]}
Wheelie_Frames: {round(game_state["Wheelie_Frames"]/181, 6)}
Offroad: {offroad_check}
Track_Rays: {full_rays}
Road_Rays: {road_rays}
""")

	sleep(0.1)

# TODO:
"# - MT charge %age"
"# - Race countdown, 3.0 -> 0.0 then -1"
"# - Number of Mushrooms"
# - Countdown till wheelie expires? Humans basically have this with the audio cue so it'll be useful.
# - Differentiate between road/offroad/wall when doing angled raycasts/ when character is on an angled slope
"# - Raycasts don't change rotation with player (North will always point north no matter what for example)"