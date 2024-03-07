import dolphin_memory_engine as DME

"""
['MemWatch', '__all__', '__builtins__', '__cached__',
'__doc__', '__file__', '__loader__', '__name__', '__package__',
'__path__', '__spec__', '_dolphin_memory_engine', 'assert_hooked',
'follow_pointers', 'hook', 'is_hooked', 'read_byte', 'read_bytes',
'read_double', 'read_float', 'read_word', 'un_hook', 'write_byte',
'write_bytes', 'write_double', 'write_float', 'write_word']
"""

# WE CAN RETURN THE FUNCTION'S VALUES INSIDE THE TRY BLOCK BUT IT WORKS FOR THE MOMENT.
# THIS SAVES A VARIABLE. DO IT LATER.

# Also, could save time by reusing the pointers from Prev_Pos_Pointers and just adding 0x4 to get the current pointers.

cache = {}
Quaternion_Pointers = [0x20, 0x0, 0x24, 0x90, 0x4]
Prev_Pos_Pointers = [0xC, 0x10, 0x0, 0x0, 0x8, 0x90]
Current_Pos_Pointers = [0xC, 0x10, 0x0, 0x0, 0x8, 0x90, 0x4]
Race_Completion_Pointers = [0xC, 0x0]

def Get_Quaternion_Values():

    def Get_Quaternion_Region_Address():
        if not cache.get("quat_region_address"):
            match str(DME.read_bytes(int(0x80000000), 6))[5]:
                case "P":
                    #print("PAL Version - Using 0x809C18F8")
                    cache["quat_region_address"] = 0x809C18F8
                case "E":
                    #print("NA Version - Using 0x809BD110")
                    cache["quat_region_address"] = 0x809BD110
                case other:
                    return -1

        return cache["quat_region_address"]

    quat_region_offset = Get_Quaternion_Region_Address()
    
    # In Menus check
    try:
        quaternions_addr = DME.follow_pointers(int(quat_region_offset), Quaternion_Pointers)
    except RuntimeError:
        return ""

    return [DME.read_float(DME.follow_pointers(int(quaternions_addr), [0xF0])),
            DME.read_float(DME.follow_pointers(int(quaternions_addr), [0xF4])),
            DME.read_float(DME.follow_pointers(int(quaternions_addr), [0xF8])),
            DME.read_float(DME.follow_pointers(int(quaternions_addr), [0xFC]))]

def Get_Pos_Values():

    def Get_Pos_Region_Address():
            if not cache.get("prev_pos"):
                match str(DME.read_bytes(int(0x80000000), 6))[5]:
                    case "P":
                        cache["prev_pos"] = 0x809C18F8
                    case "E":
                        cache["prev_pos"] = 0x809BD110
                    case other:
                        return -1

            return cache["prev_pos"]

    pos_region_address = Get_Pos_Region_Address()
    
    # In Menus check
    try:
        prev_pos_addr = DME.follow_pointers(int(pos_region_address), Prev_Pos_Pointers)
        current_pos_addr = DME.follow_pointers(int(pos_region_address), Current_Pos_Pointers)
    except RuntimeError:
        return ""

    return [DME.read_float(DME.follow_pointers(int(prev_pos_addr), [0x18])),
            DME.read_float(DME.follow_pointers(int(prev_pos_addr), [0x1C])),
            DME.read_float(DME.follow_pointers(int(prev_pos_addr), [0x20])),
            DME.read_float(DME.follow_pointers(int(current_pos_addr), [0x68])),
            DME.read_float(DME.follow_pointers(int(current_pos_addr), [0x6C])),
            DME.read_float(DME.follow_pointers(int(current_pos_addr), [0x70]))]

def Get_Race_Completion():

    def Get_Race_Completion_Region_Address():
        if not cache.get("race_completion"):
            match str(DME.read_bytes(int(0x80000000), 6))[5]:
                case "P":
                    #print("PAL Version - Using 0x809C18F8")
                    cache["race_completion"] = 0x809BD730
                case "E":
                    #print("NA Version - Using 0x809BD110")
                    cache["race_completion"] = 0x809B8F70
                case other:
                    return -1

        return cache["race_completion"]

    race_completion_offset = Get_Race_Completion_Region_Address()
    
    # In Menus check
    try:
        race_completion_addr = DME.follow_pointers(int(race_completion_offset), Race_Completion_Pointers)
    except RuntimeError:
        return ""

    return DME.read_float(DME.follow_pointers(int(race_completion_addr), [0xC]))