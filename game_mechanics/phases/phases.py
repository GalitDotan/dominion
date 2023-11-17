from enum import Enum


class Phase(Enum, int):
    ActionPhase: 1
    BuyPhase: 2
    NightPhase: 3
    CleanUpPhase: 4
