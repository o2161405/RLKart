from email import message_from_string
import dolphin_memory_engine as DME
from time import sleep
import os, csv

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

class RaceManager:
    def isInRace():
        return DME.read_word(0x809BD730) != 0

class Memory:
    class Player:
        def __init__(self, memory):
            self.memory = memory
            self.quaternions_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x24, 0x90, 0x4, 0xF0])
            self.positions_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x8, 0x90, 0x18])
            self.m_mushroomTimer_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x28, 0x188])
            self.m_speed_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x28, 0x20])
            self.m_raceCompletion_address = memory.Resolve_Address(0x809BD730, [0xC, 0x0, 0xC])
            self.m_mtCharge_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x44, 0xFE])
            self.m_hopPosY_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x44, 0x22C])
            self.m_countdownTimer_address = memory.Resolve_Address(0x809BD730, [0x22])
            self.m_surfaceFlags_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x18, 0x18, 0x2C])
            self.mushroom_count_address = memory.Resolve_Address(0x809C3618, [0x14, 0x90])
            
            self.quaternions = {"x": 0.0, "y": 0.0, "z": 0.0, "w": 0.0}
            self.positions = {"x": 0.0, "y": 0.0, "z": 0.0}
            self.m_mushroomTimer = 0
            self.m_speed = 0.0
            self.m_raceCompletion = 0.0
            self.m_mtCharge = 0
            self.m_hopPosY = 0.0
            self.m_countdownTimer = 0
            self.m_surfaceFlags = 0
            self.isAboveOffroad = False
            self.isTouchingOffroad = False
            self.mushroom_count = 0
        
        def Update(self):
            for i, key in enumerate(["x", "y", "z", "w"]):
                self.quaternions[key] = DME.read_float(self.quaternions_address + i*4)
            for i, key in enumerate(["x", "y", "z"]):
                self.positions[key] = DME.read_float(self.positions_address + i*4)
            
            self.m_speed = DME.read_float(self.m_speed_address)
            self.m_raceCompletion = DME.read_float(self.m_raceCompletion_address)
            self.m_mushroomTimer = int.from_bytes(DME.read_bytes(self.m_mushroomTimer_address, 2), byteorder='big', signed=False)
            self.m_mtCharge = int.from_bytes(DME.read_bytes(self.m_mtCharge_address, 2), byteorder='big', signed=False)
            self.m_hopPosY = DME.read_float(self.m_hopPosY_address)
            self.m_countdownTimer = int.from_bytes(DME.read_bytes(self.m_countdownTimer_address, 2), byteorder='big', signed=False)
            self.m_surfaceFlags = int.from_bytes(DME.read_bytes(self.m_surfaceFlags_address, 4), byteorder='big', signed=False)
            self.isAboveOffroad = self.m_surfaceFlags & (1 << (6 - 1)) != 0
            self.isTouchingOffroad = self.m_surfaceFlags & (1 << (7 - 1)) != 0
            self.mushroom_count = int.from_bytes(DME.read_bytes(self.mushroom_count_address, 4), byteorder='big', signed=False)
            
    def __init__(self):
        self.player = Memory.Player(self)

    def Update(self):
        self.player.Update()

    def Resolve_Address(self, addr: int, pointers: list[int]):
        return DME.follow_pointers(addr, pointers)

def main():

    previous_time = 0
    
    while not DME.is_hooked():
        clear()
        print("Not hooked.")
        DME.hook()
        sleep(1)
        
    while True:
        
        while not RaceManager.isInRace():
            clear()
            print("Waiting for race...")
            sleep(1)
        
        mem = Memory()
        
        while RaceManager.isInRace():
            
            mem.Update()
            
            print(mem.player.m_surfaceFlags_address, mem.player.mushroom_count)
            
            """
            print(f"Started Capture to race_data.csv")

            with open("race_data.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["m_countdownTimer","quaternions_x", "quaternions_y", "quaternions_z", "quaternions_w",
                                 "positions_x", "positions_y", "positions_z",
                                 "m_mushroomTimer", "m_speed", "m_raceCompletion", "m_mtCharge", "m_hopPosY"])
                
                while mem.player.m_raceCompletion < 4.0:    
                    
                    mem.Update()
                    
                    # Combine dictionary values and variables into a single list
                    data_row = [mem.player.m_raceCompletion] + [mem.player.quaternions[key] for key in ["x", "y", "z", "w"]] + \
                        [mem.player.positions[key] for key in ["x", "y", "z"]] + \
                        [mem.player.m_mushroomTimer, mem.player.m_speed, mem.player.m_raceCompletion,
                            mem.player.m_mtCharge, mem.player.m_hopPosY]
                    
                    writer.writerow(data_row)
               
            print(f"Finished writing data, exiting...")

            exit()
            """
    
if __name__ == "__main__":
    main()