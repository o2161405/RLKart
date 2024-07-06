import dolphin_memory_engine as DME
from time import sleep
import os

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
            self.boosts_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x44, 0x10C])
            self.speed_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x0, 0x28, 0x20])
            self.completion_address = memory.Resolve_Address(0x809BD730, [0xC, 0x0, 0xC])
            self.drift_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x44, 0xFE])
            self.airtime_address = memory.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x44, 0x21A])
            
            self.quaternions = {"x": 0.0, "y": 0.0, "z": 0.0, "w": 0.0}
            self.positions = {"x": 0.0, "y": 0.0, "z": 0.0}
            self.boosts = {"miniturbo": 0.0, "shroom": 0.0, "trick": 0.0}
            self.speed = 0.0
            self.completion = 0.0
            self.drift = 0
            self.airtime = 0
        
        def Update(self):
            for i, key in enumerate(["x", "y", "z", "w"]):
                self.quaternions[key] = DME.read_float(self.quaternions_address + i*4)
            for i, key in enumerate(["x", "y", "z"]):
                self.positions[key] = DME.read_float(self.positions_address + i*4)
            for i, key in enumerate(["miniturbo", "shroom", "trick"]):
                self.boosts[key] = DME.read_float(self.boosts_address + i*4)
            
            self.speed = DME.read_float(self.speed_address)
            self.completion = DME.read_float(self.completion_address)
            self.drift = int.from_bytes(DME.read_bytes(self.drift_address, 2), byteorder='big', signed=False)
            self.airtime = int.from_bytes(DME.read_bytes(self.airtime_address, 2), byteorder='big', signed=False)

    def __init__(self):
        self.player = Memory.Player(self)

    def Update(self):
        self.player.Update()

    def Resolve_Address(self, addr: int, pointers: list[int]):
        return DME.follow_pointers(addr, pointers)

def main():

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
Boosts: {mem.player.boosts}
Speed: {mem.player.speed}
Race Completion: {mem.player.completion}
Drift: {mem.player.drift}
Airtime: {mem.player.airtime}
""")
            sleep(0.1)
    
if __name__ == "__main__":
    main()