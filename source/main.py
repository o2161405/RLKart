from mem_main import get_game_state
import dolphin_memory_engine as DME
from time import sleep
from mesh import get_raycasts


while not DME.is_hooked():
    print("Not hooked..")
    DME.hook()
    sleep(0.5)

while True:
	game_state = get_game_state(False)

	if game_state != None:
		positions = game_state[4]
		print(get_raycasts(positions[0], positions[1], positions[2]))

	sleep(0.02)

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
# - Raycasts don't change rotation with player (North will always point north no matter what for example)