from time import sleep, time_ns
import os
from mem_tools import *
import dolphin_memory_engine as DME
import math

if __name__ == "__main__":

    Print_Text = True
    max_runtime = 0

    while not DME.is_hooked():
        print("Not hooked..")
        DME.hook()
        sleep(0.5)
        os.system('cls')

    while True:

        t0 = time_ns() / (10 ** 9)

        # In Menus check, could be done better
        if Get_Quaternion_Values() == "":
            os.system('cls')
            if Print_Text:
                print("In Menus")
            sleep(0.1)
            continue

        Quat_X, Quat_Y, Quat_Z, Quat_W = Get_Quaternion_Values()
        Prev_Pos_X, Prev_Pos_Y, Prev_Pos_Z, Current_Pos_X, Current_Pos_Y, Current_Pos_Z = Get_Pos_Values()

        if Print_Text:
            print(f"""Speed
X:  {Current_Pos_X - Prev_Pos_X}
Y:  {Current_Pos_Y - Prev_Pos_Y}
Z:  {Current_Pos_Z - Prev_Pos_Z}
XZ: {math.sqrt(((Current_Pos_X - Prev_Pos_X)**2) + ((Current_Pos_Z - Prev_Pos_Z)**2))}
XYZ: {math.sqrt(((Current_Pos_X - Prev_Pos_X)**2) + ((Current_Pos_Y - Prev_Pos_Y)**2) + ((Current_Pos_Z - Prev_Pos_Z)**2))}\n""")

            print(f"Quaternions\nX: {Quat_X}\nY: {Quat_Y}\nZ: {Quat_Z}\nW: {Quat_W}\n")

            print(f"Previous Position\nX: {Prev_Pos_X} Y: {Prev_Pos_Y} Z: {Prev_Pos_Z}\n")

            print(f"Current Position\nX: {Current_Pos_X} Y: {Current_Pos_Y} Z: {Current_Pos_Z}\n")

        t1 = time_ns() / (10 ** 9)

        if t1 - t0 > max_runtime:
            max_runtime = t1 - t0

        if Print_Text:
            print(f"Executed in {t1 - t0} milliseconds.")
            print(f"Highest execute time: {max_runtime} milliseconds.")
        sleep(0.1)
        os.system('cls')
