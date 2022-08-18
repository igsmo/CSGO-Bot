import pymem
import pymem.process
import time

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

class GameinfoExtractor():
    def __init__(self) -> None:
        self.pm = pymem.Pymem("csgo.exe")
        self.client = None
        self.player = None

        self._connectToDll()
    
    def _connectToDll(self):
        self.client = pymem.process.module_from_name(self.pm.process_handle, "client.dll").lpBaseOfDll
        self.player = self.pm.read_int(self.client + DWLOCALPLAYER)


    def getPlayerStats(self):
        #playerRes = pm.read_int(client + 0x2ECCF0C)
        #print(pm.read_int(playerRes + 0x161C))
        #print(pm.read_bool(playerRes + 0x161C))
        result = {}

        for stat in PLAYER_STATS_PTRS:
            try:
                match PLAYER_STATS_PTRS[stat][1]:
                    case 'float':
                        result[stat] = self.pm.read_float(self.player + PLAYER_STATS_PTRS[stat][0])
                    case 'int':
                        temp_result = self.pm.read_int(self.player + PLAYER_STATS_PTRS[stat][0])
                        # Assign Team name to TeamID
                        if stat == "Team": result[stat] = TEAM_IDS[temp_result]
                        else: result[stat] = temp_result
                    case 'bool':
                        result[stat] = self.pm.read_bool(self.player + PLAYER_STATS_PTRS[stat][0])
            except Exception as e:
                print(e)
                continue

        return result
