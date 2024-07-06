import dolphin_memory_engine as DME
from time import sleep
import os, csv, math

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

def get_yaw(quat):
    x = quat["x"]
    y = quat["y"]
    z = quat["w"]
    w = quat["z"]

    yaw = math.degrees(math.atan2(2.0 * (y * z + w * x), w * w - x * x - y * y + z * z))

    return yaw


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
            self.m_driftState_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x28, 0xFC])
            self.m_realTurn_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x28, 0x158])
            self.m_hopPosY_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x44, 0x22C])
            self.m_countdownTimer_address = memory.Resolve_Address(0x809BD730, [0x22])
            self.m_surfaceFlags_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x18, 0x18, 0x2C])
            self.mushroom_count_address = memory.Resolve_Address(0x809C3618, [0x14, 0x90])
            self.m_bitfield2_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x4, 0xC])
            self.m_offroadInvincibility_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x28, 0x148])
            
            self.quaternions = {"x": 0.0, "y": 0.0, "z": 0.0, "w": 0.0}
            self.eular_yaw = 0
            self.positions = {"x": 0.0, "y": 0.0, "z": 0.0}
            self.m_mushroomTimer = 0
            self.m_speed = 0.0
            self.m_raceCompletion = 0.0
            self.m_mtCharge = 0
            self.m_driftState = 0
            self.m_realTurn = 0.0
            self.m_hopPosY = 0.0
            self.m_countdownTimer = 0
            self.m_surfaceFlags = 0
            self.isAboveOffroad = False
            self.isTouchingOffroad = False
            self.mushroom_count = 0
            self.m_bitfield2 = 0
            self.isWheelie = False
            self.m_offroadInvincibility = False
        
        def Update(self):
            for i, key in enumerate(["x", "y", "z", "w"]):
                self.quaternions[key] = DME.read_float(self.quaternions_address + i*4)
            for i, key in enumerate(["x", "y", "z"]):
                self.positions[key] = DME.read_float(self.positions_address + i*4)
            
            self.eular_yaw = get_yaw(self.quaternions)
            self.m_speed = DME.read_float(self.m_speed_address)
            self.m_raceCompletion = DME.read_float(self.m_raceCompletion_address)
            self.m_mushroomTimer = int.from_bytes(DME.read_bytes(self.m_mushroomTimer_address, 2), byteorder='big', signed=False)
            self.m_mtCharge = int.from_bytes(DME.read_bytes(self.m_mtCharge_address, 2), byteorder='big', signed=False)
            self.m_driftState = int.from_bytes(DME.read_bytes(self.m_driftState_address, 2), byteorder='big', signed=False)
            self.m_realTurn = DME.read_float(self.m_realTurn_address)
            self.m_hopPosY = DME.read_float(self.m_hopPosY_address)
            self.m_countdownTimer = int.from_bytes(DME.read_bytes(self.m_countdownTimer_address, 2), byteorder='big', signed=False)
            self.m_surfaceFlags = int.from_bytes(DME.read_bytes(self.m_surfaceFlags_address, 4), byteorder='big', signed=False)
            self.isAboveOffroad = self.m_surfaceFlags & (1 << (6 - 1)) != 0
            self.isTouchingOffroad = self.m_surfaceFlags & (1 << (7 - 1)) != 0
            self.mushroom_count = int.from_bytes(DME.read_bytes(self.mushroom_count_address, 4), byteorder='big', signed=False)
            self.m_bitfield2 = int.from_bytes(DME.read_bytes(self.m_bitfield2_address, 4), byteorder='big', signed=False)
            self.isWheelie = self.m_bitfield2 & (1 << (5 - 1)) != 0
            self.m_offroadInvincibility = int.from_bytes(DME.read_bytes(self.m_offroadInvincibility_address, 2), byteorder='big', signed=False) != 0
            
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
            
            clear()
            print(f"""Quaternions: {mem.player.quaternions}  
Positions: {mem.player.positions}
eular_yaw: {mem.player.eular_yaw}
m_speed: {mem.player.m_speed}
m_raceCompletion: {mem.player.m_raceCompletion}
m_mtCharge: {mem.player.m_mtCharge}
m_driftState: {mem.player.m_driftState}
m_realTurn: {mem.player.m_realTurn}
m_hopPosY: {mem.player.m_hopPosY}
m_countdownTimer: {mem.player.m_countdownTimer}
isAboveOffroad: {mem.player.isAboveOffroad}
isTouchingOffroad: {mem.player.isTouchingOffroad}
Mushroom Count: {mem.player.mushroom_count}
m_mushroomTimer: {mem.player.m_mushroomTimer}
isWheelie: {mem.player.isWheelie}
m_offroadInvincibility: {mem.player.m_offroadInvincibility}
""")
            
            sleep(0.2)
            
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