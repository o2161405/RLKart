import dolphin_memory_engine as DME
from time import sleep
import os

"""
['MemWatch', '__all__', '__builtins__', '__cached__', '__doc__',
'__file__', '__loader__', '__name__', '__package__', '__path__',
'__spec__', '_dolphin_memory_engine', 'assert_hooked', 'follow_pointers',
'get_status', 'hook', 'is_hooked', 'read_byte', 'read_bytes', 'read_double',
'read_float', 'read_word', 'un_hook', 'write_byte', 'write_bytes', 'write_double', 'write_float', 'write_word']
"""

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

class RaceManager:
	def isInRace():
		return DME.read_word(0X809BD730) != 0

class Memory:
	def __init__(self):
		self.quaternions_address: int = self.Resolve_Address(0x809C18F8, [0x20, 0x0, 0x24, 0x90, 0x4, 0xF0])
		self.quaternions = {"x": 0.0, "y": 0.0, "z": 0.0, "w": 0.0}

		self.boosts_address: int = self.Resolve_Address(0x809C18F8, [0xC, 0x10, 0x0, 0x10, 0x10, 0x10C])
		self.boosts = {"miniturbo": 0.0, "shroom": 0.0, "trick": 0.0}

		self.completion_address: int = self.Resolve_Address(0x809BD730, [0xC, 0x0, 0xC])
		self.completion = 0.0

		self.drift_address: int = self.Resolve_Address(0x809C18F8, [0xC, 0x10, 0x0, 0x10, 0x10, 0xFE])
		self.drift = 0

		self.airtime_address: int = self.Resolve_Address(0x809C18F8, [0xC, 0x10, 0x0, 0x10, 0x10, 0x21A])
		self.airtime = 0

	def Update(self):
		for i, key in enumerate(["x", "y", "z", "w"]):
			self.quaternions[key] = DME.read_float(self.boosts_address + i*4)

		for i, key in enumerate(["miniturbo", "shroom", "trick"]):
			self.boosts[key] = DME.read_float(self.boosts_address + i*4)

		self.completion = DME.read_float(self.completion_address)
		self.drift = int.from_bytes(DME.read_bytes(self.drift_address, 2), byteorder='big', signed=False)
		self.airtime = int.from_bytes(DME.read_bytes(self.airtime_address, 2), byteorder='big', signed=False)

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
			print(mem.drift, mem.airtime)
	
if __name__ == "__main__":
	main()