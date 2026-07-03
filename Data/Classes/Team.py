########################################################################################################################
#   #Author: Devin Millage
#   #Class: Team
#   #Date:6/10/2026
#
# Team that has an amount of points and a roster of players
#######################################################################################################################
from Data.Classes.Player import *
from dataclasses import dataclass, field

#Team class
@dataclass
class Team:
    roster: list[Player] = field(default_factory=list)
    teamName: str = ""

    def __post_init__(self):
        self.roster = [Player(**item) if isinstance(item, dict) else item for item in self.roster]

