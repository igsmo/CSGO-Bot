import pymem
import pymem.process
import time

pm = pymem.Pymem("csgo.exe")

TEAM_IDS = {
    1: "SPECTATOR",
    2: "T",
    3: "CT"
}

DWLOCALPLAYER = (0xDC04CC)

PLAYER_STATS_PTRS = {
    "HP": [0x100, "int"],
    "Armor": [0x117CC, "int"],
    "Helmet": [0x117C0, 'bool'],
    "Weapon": [12040, "int"],
    "Team": [0xF4, "int"],
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
    playerRes = pm.read_int(client + 0x2ECCF0C)
    print(pm.read_int(playerRes + 0x161C))
    #print(pm.read_bool(playerRes + 0x161C))
    result = {}

    for stat in PLAYER_STATS_PTRS:
        try:
            match PLAYER_STATS_PTRS[stat][1]:
                case 'float':
                    result[stat] = pm.read_float(player + PLAYER_STATS_PTRS[stat][0])
                case 'int':
                    temp_result = pm.read_int(player + PLAYER_STATS_PTRS[stat][0])
                    # Assign Team name to TeamID
                    if stat == "Team": result[stat] = TEAM_IDS[temp_result]
                    else: result[stat] = temp_result
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