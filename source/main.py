from mem_main import get_game_state
import dolphin_memory_engine as DME
from time import sleep


while not DME.is_hooked():
    print("Not hooked..")
    DME.hook()
    sleep(0.5)

while True:
	game_state = get_game_state(False)

	if game_state != None:
		#agent_world_info = game_state[0:3]
		agent_world_info = game_state[3]
		print(agent_world_info)

	sleep(0.02)


# Output example:
# [66.3, -1.8, 14116.451, 3272.538, -75.384, 4.384]
# Speed XZ, Speed Y, X, Y, and Z coords, Race Completion

# We're doing 0:3 for the agent's view because index 4 and 5 are the quaternion and position info.
# Those two things aren't useful for the AI agent to have, but we still need
# them in the output for when we do the raycasting stuff.

# TODO:
# - MT charge %age
# - Race countdown, 3.0 -> 0.0 then -1
# - Normalize RaceCompetition to 0-1?
# - Number of Mushrooms
# - Countdown till wheelie expires? Humans basically have this with the audio cue so it'll be useful.
# - Differentiate between road/offroad/wall when doing angled raycasts/ when character is on an angled slope