import dolphin_memory_engine as DME
from time import sleep
import os, csv, math
import trimesh
import numpy as np
from trimesh.ray.ray_pyembree import RayMeshIntersector

clear = lambda: os.system('cls' if os.name=='nt' else 'clear')

class RayCaster:
    def __init__(self, mesh_path, ray_amount):
        self.mesh = trimesh.load(mesh_path, force='mesh')
        self.collisionTester = trimesh.ray.ray_pyembree.RayMeshIntersector(self.mesh)
        self.ray_amount = ray_amount
        self.base_rays = self.generate_rays()

    def generate_rays(self):
        angles = np.linspace(0, 2*np.pi, self.ray_amount, endpoint=False)
        x = np.cos(angles)
        z = np.sin(angles)
        return np.stack((x, np.zeros_like(angles), z), axis=-1)

    def raycast(self, player_position, rotation):
        player_position_divided = np.array(player_position) / 100
        origin = player_position_divided.reshape(1, 3)
        ray_origins = np.tile(origin, (self.ray_amount, 1))

        # Rotate the rays
        rotation_rad = np.radians(-rotation + 90)
        cos_rot, sin_rot = np.cos(rotation_rad), np.sin(rotation_rad)
        
        rotated_x = self.base_rays[:, 0] * cos_rot - self.base_rays[:, 2] * sin_rot
        rotated_z = self.base_rays[:, 0] * sin_rot + self.base_rays[:, 2] * cos_rot
        
        rotated_rays = self.base_rays.copy()
        rotated_rays[:, 0] = rotated_x
        rotated_rays[:, 2] = rotated_z

        # https://trimesh.org/trimesh.ray.ray_pyembree.html#trimesh.ray.ray_pyembree.RayMeshIntersector.intersects_location
        ray_intersect_locations = self.collisionTester.intersects_location(ray_origins, rotated_rays, multiple_hits=False)[0]
        
        distances = np.linalg.norm(ray_intersect_locations - player_position_divided, axis=1)
        
        return distances

class RaceManager:
    def isInRace():
        return DME.read_word(0x809BD730) != 0
    
    def getStateNormalized(mem):
        game_state = {
            "posX": round((mem.player.positions[0] + 17700) / 41200, 4),
            "posZ": round((mem.player.positions[2] + 19100) / 37700, 4),
            "yaw": round((mem.player.eular_yaw + 180) / 360, 4),
            "mtCharge": round(mem.player.m_mtCharge / 270, 4),
            "speed": round(mem.player.m_speed / 120, 4),
            "raceCompletion": round(mem.player.m_raceCompletion / 4, 4),
            "driftState": mem.player.m_driftState / 2,
            "realTurn": round((mem.player.m_realTurn + 1) / 2, 4),
            "hopPosY": round(mem.player.m_hopPosY / 35, 4),
            "isAboveOffroad": int(mem.player.isAboveOffroad),
            "isTouchingOffroad": int(mem.player.isTouchingOffroad),
            "shroomCount": mem.player.mushroom_count,
            "shroomTimer": round(mem.player.m_mushroomTimer/ 90, 4),
            "isWheelie": int(mem.player.isWheelie),
            "offroadInvincibility": int(mem.player.m_offroadInvincibility)
            }
        
        return game_state

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
            self.positions = [0.0, 0.0, 0.0]
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
            for i in range(3):
                self.positions[i] = DME.read_float(self.positions_address + i*4)
            
            self.eular_yaw = self.get_yaw(self.quaternions)
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
            
        def get_yaw(self, quat):
            x = quat["x"]
            y = quat["y"]
            z = quat["w"]
            w = quat["z"]

            yaw = math.degrees(math.atan2(2.0 * (y * z + w * x), w * w - x * x - y * y + z * z))

            return yaw
            
    def __init__(self):
        self.player = Memory.Player(self)

    def Update(self):
        self.player.Update()

    def Resolve_Address(self, addr: int, pointers: list[int]):
        return DME.follow_pointers(addr, pointers)

def main():

    raycaster = RayCaster('model/full_mesh.obj', 360)
    
    while not DME.is_hooked():
        clear()
        print("Not hooked.")
        DME.hook()
        sleep(1)

    mem = Memory()
        
    while True:
        
        while not RaceManager.isInRace():
            clear()
            print("Waiting for race...")
            sleep(1)
        
        while RaceManager.isInRace():
            
            mem.Update()
            raycastOutput = raycaster.raycast(mem.player.positions, mem.player.eular_yaw)
            
            clear()
            print(RaceManager.getStateNormalized(mem))
            print(raycastOutput)
            
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