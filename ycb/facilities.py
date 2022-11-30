from __future__ import annotations

from dataclasses import dataclass

import httpx


# Getting facility list
# Essentially these are community centres
# curl 'https://www.onepa.gov.sg/pacesapi/FacilitySearch/GetFacilityOutlets'


@dataclass
class Product:
    id: str
    value: str


@dataclass
class Facility:
    id: str
    label: str
    lat: float
    lng: float
    categories: object  # Ignored
    productList: list[Product]

    # Convert to actual class
    # Add for all non-base types
    def __post_init__(self):
        l = []
        for product in self.productList:
            if isinstance(product, dict):
                l.append(Product(**product))
            else:
                l.append(product)
        self.productList = l


def get_facilities():
    request = httpx.get("https://www.onepa.gov.sg/pacesapi/FacilitySearch/GetFacilityOutlets")
    if request.status_code != 200:
        raise Exception(f"bad status code: {request.status_code}")
    facilities: list[Facility] = []
    try:
        data = request.json()
        data = data["data"]
        data = data["data"]
        outlets = data["outlets"]

        for outlet in outlets:
            for facility in outlet['ccList']:
                facilities.append(Facility(**facility))

    except KeyError as e:
        raise Exception(f"unable to parse facilities query: {str(e)}")

    return facilities
