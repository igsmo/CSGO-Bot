# ---- CONFIGURE THRESHOLDS FOR CANNY -------
# if cv2.waitKey(25) & 0xFF == ord('n'):
#     canny_threshold1 -= 50
# elif cv2.waitKey(25) & 0xFF == ord('m'):
#     canny_threshold1 += 50
# elif cv2.waitKey(25) & 0xFF == ord('j'):
#     canny_threshold2 -= 50
# elif cv2.waitKey(25) & 0xFF == ord('k'):
#     canny_threshold2 += 50
# print(f"Current t={canny_threshold1} and {canny_threshold2}")


# ---- STATS EXTRACT USING CHEAT ENGINE -------
# def extract_stats_pymem():
# 
#     client = pymem.process.module_from_name(pm.process_handle, 'client.dll')
#     address = client.lpBaseOfDll
# 
#     print(str(pm.read_int(getPointerAddress(pm.base_address + address, offsets=[0x00FC]))))
    
# def getPointerAddress(base, offsets):
#     remote_pointer = RemotePointer(pm.process_handle, base)
#     for offset in offsets:
#         if offset != offsets[-1]:
#             remote_pointer = RemotePointer(pm.process_handle, remote_pointer.value + offset)
#         else:
#             return remote_pointer.value + offset
# 
# if __name__ == '__main__':
#     pm = pymem.Pymem("csgo.exe")
#     extract_stats_pymem()

import pymem
import pymem.process
import time

pm = pymem.Pymem("csgo.exe")

DWLOCALPLAYER = (0xDC04CC)

PLAYER_STATS_PTRS = {
    "HP": [0x100, "int"],
    "Armor": [0x117CC, "int"],
    "Helmet": [0x117C0, 'bool'],
    "IsReloading": [0x32B5, 'bool'],
    "EyeAngleX": [0x117D0, "float"],
    "EyeAngleY": [0x117D4, "float"]
}

GAMEINFO_PTRS = {

}

def extract_gameinfo():
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    player = pm.read_int(client + DWLOCALPLAYER)

    result = {}


def extract_player_stats():
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    player = pm.read_int(client + DWLOCALPLAYER)

    result = {}

    for stat in PLAYER_STATS_PTRS:
        try:
            match PLAYER_STATS_PTRS[stat][1]:
                case 'float':
                    result[stat] = pm.read_float(player + PLAYER_STATS_PTRS[stat][0])
                case 'int':
                    result[stat] = pm.read_int(player + PLAYER_STATS_PTRS[stat][0])
                case 'bool':
                    result[stat] = pm.read_bool(player + PLAYER_STATS_PTRS[stat][0])
        except Exception as e:
            print(e)
            continue

    return result

if __name__ == '__main__':
    while True:
        print(extract_player_stats())
        time.sleep(0.5)