########################################################################################################################
#   #Author: Devin Millage
#   #Class: Player
#   #Date:6/10/2026
#
# This is the class for the players that will take the field and play. Players will be assigned a team, position (maybe
# given by the player because I like the idea of letting the player decide each team members
# position like in super sluggers), Name, batting order position, number, and some stats that
# will make each player different from another.
########################################################################################################################
from dataclasses import dataclass
from enum import StrEnum

class Position(StrEnum):
    FIRST = "first"
    SECOND = "second"
    SHORT = "short"
    THIRD = "third"
    CATCH = "catch"
    PITCH = "pitch"
    LF = "LF"
    CF = "CF"
    RF = "RF"
    LEFTBENCH = "" # used for unset position

#Player Class
@dataclass
class Player:
    name: str = ''
    num: int = 0
    position: Position = Position.LEFTBENCH
    order: int = -1
    bStat: int = 0
    pStat: int = 0
    fStat: int = 0
    sStat: int = 0
    team: str = ''

    def getInitials(self):
       return  f"{self.name[0]}.{self.name.split(" ", 1)[1][0]}"

########################################################################################################################