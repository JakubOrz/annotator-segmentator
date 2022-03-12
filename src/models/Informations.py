from .Tier import Tier
from typing import List


class Informations:
    tiers: List[Tier]

    def __init__(self):
        self.tiers = list()

    def addTier(self, tier: Tier) -> 'Informations':
        self.tiers.append(tier)
        return self

    def getTiers(self) -> List['Tier']:
        return self.tiers

    def pepare_time_order(self) -> dict:
        time_stamps: list = list()
        # Collect time stamps from all annotations
        for tier in self.tiers:
            for annotation in tier.annotations:
                time_stamps.append(annotation.start_time)
                time_stamps.append(annotation.end_time)
        return {time: "ts"+str(i+1) for i, time in enumerate(sorted(time_stamps))}

    def print(self):
        print("Liczba tierów: {}".format(len(self.tiers)))
