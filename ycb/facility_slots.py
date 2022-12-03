from __future__ import annotations

import datetime
from dataclasses import dataclass


@dataclass
class FacilitySlot:
    timeRangeId: str
    timeRangeName: str
    startTime: datetime.datetime
    endTime: datetime.datetime
    availabilityStatus: str
    isAvailable: bool
    isPeak: bool

    def __post_init__(self):
        if isinstance(self.startTime, str):
            self.startTime = datetime.datetime.strptime(self.startTime, "%Y-%m-%dT%H:%M")
        if isinstance(self.endTime, str):
            self.startTime = datetime.datetime.strptime(self.endTime, "%Y-%m-%dT%H:%M")

    def get_booking_URL(self, facilityId: str):
        return f"https://www.onepa.gov.sg/facilities/availability?facilityId={facilityId}&date={self.startTime.strftime('%d/%m/%Y')}&time=all"

