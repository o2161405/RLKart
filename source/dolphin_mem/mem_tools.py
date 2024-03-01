import dolphin_memory_engine as DME

"""
['MemWatch', '__all__', '__builtins__', '__cached__',
'__doc__', '__file__', '__loader__', '__name__', '__package__',
'__path__', '__spec__', '_dolphin_memory_engine', 'assert_hooked',
'follow_pointers', 'hook', 'is_hooked', 'read_byte', 'read_bytes',
'read_double', 'read_float', 'read_word', 'un_hook', 'write_byte',
'write_bytes', 'write_double', 'write_float', 'write_word']
"""

cache = {}
Quaternion_Pointers = [0x20, 0x0, 0x24, 0x90, 0x4]
Prev_Pos_Pointers = [0xC, 0x10, 0x0, 0x0, 0x8, 0x90]
Current_Pos_Pointers = [0xC, 0x10, 0x0, 0x0, 0x8, 0x90, 0x4]

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
                case "J":
                    #print("JP Version - Using 0x809C0958")
                    cache["quat_region_address"] = 0x809C0958
                case "K":
                    #print("KR Version - Using 0x809AFF3")
                    cache["quat_region_address"] = 0x809AFF38
                case other:
                    #print("Cannot detect game version, defaulting to PAL..")
                    cache["quat_region_address"] = 0x809C18F8

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
                    case "J":
                        cache["prev_pos"] = 0x809C0958
                    case "K":
                        cache["prev_pos"] = 0x809AFF38
                    case other:
                        # Defaulting to PAL
                        cache["prev_pos"] = 0x809C18F8

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
