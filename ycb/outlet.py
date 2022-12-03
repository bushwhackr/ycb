from __future__ import annotations

import datetime
from dataclasses import dataclass

import httpx

from ycb.facility_slots import FacilitySlot


# Getting facility list
# Essentially these are community centres
# curl 'https://www.onepa.gov.sg/pacesapi/FacilitySearch/GetFacilityOutlets'

# Getting availability list
# curl 'https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots?selectedFacility=BishanCC_BADMINTONCOURTS&selectedDate=18/12/2022'

@dataclass
class Product:
    id: str
    value: str


@dataclass
class CommunityCentre:
    id: str
    label: str
    lat: float
    lng: float
    categories: any
    productList: list[Product]

    def __post_init__(self):
        l = []
        for product in self.productList:
            if isinstance(product, dict):
                l.append(Product(**product))
            else:
                l.append(product)
        self.productList = l

    def lookup(self, facility: str, date: datetime.date) -> list[FacilitySlot]:
        # Cannot be the previous day
        if date < (datetime.datetime.now().date()):
            return []

        # Cannot be more than 15 days in advance
        if date > (datetime.datetime.now() + datetime.timedelta(15)).date():
            return []

        product_id = ""
        for product in self.productList:
            if product.value == facility:
                product_id = product.id
                break

        # CommunityCentre does not have facility
        if product_id == "":
            return []

        request = httpx.get("https://www.onepa.gov.sg/pacesapi/facilityavailability/GetFacilitySlots", params={
            "selectedFacility": "BishanCC_BADMINTONCOURTS",
            "selectedDate": date.strftime("%d/%m/%Y")
        })

        if request.status_code != 200:
            raise Exception(f"bad status code: {request.status_code}")

        slots = []
        raw_slots = request.json()["response"]["resourceList"][0]["slotList"]
        for raw_slot in raw_slots:
            slots.append(FacilitySlot(**raw_slot))

        return slots


@dataclass
class Outlet:
    ccList: list[CommunityCentre]
    neighbourhood: str

    def __post_init__(self):
        l = []
        for cc in self.ccList:
            if isinstance(cc, dict):
                l.append(CommunityCentre(**cc))
            else:
                l.append(cc)
        self.ccList = l


def get_outlets():
    request = httpx.get("https://www.onepa.gov.sg/pacesapi/FacilitySearch/GetFacilityOutlets")
    if request.status_code != 200:
        raise Exception(f"bad status code: {request.status_code}")
    outlets: list[Outlet] = []

    try:
        data = request.json()
        raw_outlets = data["data"]["data"]["outlets"]

        for raw_outlet in raw_outlets:
            outlets.append(Outlet(**raw_outlet))

    except KeyError as e:
        raise Exception(f"unable to parse outlets query: {str(e)}")

    return outlets
