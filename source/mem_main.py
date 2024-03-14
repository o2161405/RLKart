from time import sleep, time_ns
from mem_tools import Get_Quaternion_Values, Get_Pos_Values, Get_Race_Completion
import dolphin_memory_engine as DME
import math

def get_game_state():

    # In Menus check, could be done better
    if Get_Quaternion_Values() == "":
        return None

    Quat_X, Quat_Y, Quat_Z, Quat_W = Get_Quaternion_Values()
    Prev_Pos_X, Prev_Pos_Y, Prev_Pos_Z, Current_Pos_X, Current_Pos_Y, Current_Pos_Z = Get_Pos_Values()
    Race_Completion = Get_Race_Completion()

    oil_distance_1_X = round(Current_Pos_X - 3200)
    oil_distance_1_Z = round(Current_Pos_Z - 10930)
    hit_oil_1 = round(math.sqrt(abs(oil_distance_1_X)**2 + abs(oil_distance_1_Z)**2)) < 300

    oil_distance_2_X = round(Current_Pos_X - 14700)
    oil_distance_2_Z = round(Current_Pos_Z + 17370)
    hit_oil_2 = round(math.sqrt(abs(oil_distance_2_X)**2 + abs(oil_distance_2_Z)**2)) < 300

    boost_pad_distance_X = round(Current_Pos_X + 13750)
    boost_pad_distance_Z = round(Current_Pos_Z - 9792)
    # Because it's a rectangle hitbox for the boost pad so we can't do
    # a proximity detection for when you're on it like with the oil

    if [round(Current_Pos_X, 3), round(Current_Pos_Y, 3), round(Current_Pos_Z, 3)] == [0.0, 0.0, 0.0]:
        return None

    return [
            [[oil_distance_1_X, oil_distance_1_Z, hit_oil_1],
            [oil_distance_2_X, oil_distance_2_Z, hit_oil_2],
            [boost_pad_distance_X, boost_pad_distance_Z]],
            round(math.sqrt(((Current_Pos_X - Prev_Pos_X)**2) + ((Current_Pos_Z - Prev_Pos_Z)**2)), 1), #XZ Speed
            round(Race_Completion, 3), # Race Completion
           #round(Current_Pos_Y  - Prev_Pos_Y, 1), # Y Speed
           [Quat_X, Quat_Y, Quat_Z, Quat_W], # Quaternions (The agent doesn't need to know it's direction if it has rays and Race_Completion)
                                           # On second thought, we need this. If we had a model rotating and a ray ALWAYS had to be to
                                           # the right of it, we need the rotation and then add 90 degrees Eular to it.
           [round(Current_Pos_X, 3), round(Current_Pos_Y, 3), round(Current_Pos_Z, 3)], # Position
           ]

if __name__ == "__main__":
    get_game_state()