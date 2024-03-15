from time import sleep, time_ns
from mem_tools import Get_Quaternion_Values, Get_Pos_Values, Get_Race_Completion, Get_Countdown, Get_MT_Charge
import dolphin_memory_engine as DME
import math

def get_game_state():

    # In Menus check, could be done better
    if Get_Quaternion_Values() == "":
        return None

    Quaternions = Get_Quaternion_Values()
    Previous_Positions = Get_Pos_Values()[0]
    Current_Positions = Get_Pos_Values()[1]

    Race_Completion = round(Get_Race_Completion(), 3)
    XZ_Speed = round(math.sqrt(((Current_Positions[0] - Previous_Positions[0])**2) +
                                                   ((Current_Positions[2] - Previous_Positions[2])**2)), 1)

    #First_Oil_Distance_X = Current_Positions[0] - 3200
    #First_Oil_Distance_Z = Current_Positions[2] - 10930
    #Player_Hit_First_Oil = math.sqrt(abs(First_Oil_Distance_X)**2 + abs(First_Oil_Distance_Z)**2) < 300

    #Second_Oil_Distance_X = Current_Positions[0] - 14700
    #Second_Oil_Distance_Z = Current_Positions[2] + 17370
    #Player_Hit_Second_Oil = math.sqrt(abs(Second_Oil_Distance_X)**2 + abs(Second_Oil_Distance_Z)**2) < 300
    
    #Boost_Pad_Distance_X = Current_Positions[0] + 13750
    #Boost_Pad_Distance_Z = Current_Positions[2] - 9792

    Countdown = int(Get_Countdown().hex(), 16)
    Countdown = round((240 - Countdown) / 60, 2)

    MT_Charge = Get_MT_Charge()

    if Countdown < 0:
        Countdown = -1

    # Detect if we're in the restart black screen when all values are nulled but it isn't technically the menu
    if Current_Positions == [0.0, 0.0, 0.0]:
        return None

    return {"Quaternions": Quaternions,
            "Previous_Positions": Previous_Positions,
            "Current_Positions": Current_Positions,
            "Race_Completion": Race_Completion,
            "XZ_Speed": XZ_Speed,
            #"First_Oil_Distance_X": First_Oil_Distance_X,
            #"First_Oil_Distance_Z": First_Oil_Distance_Z,
            #"Player_Hit_First_Oil": Player_Hit_First_Oil,
            #"Second_Oil_Distance_X": Second_Oil_Distance_X,
            #"Second_Oil_Distance_Z": Second_Oil_Distance_Z,
            #"Player_Hit_Second_Oil": Player_Hit_Second_Oil,
            #"Boost_Pad_Distance_X": Boost_Pad_Distance_X,
            #"Boost_Pad_Distance_Z": Boost_Pad_Distance_Z,
            "Countdown": Countdown,
            "MT_Charge": MT_Charge}

if __name__ == "__main__":
    get_game_state()