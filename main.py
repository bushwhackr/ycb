from ycb.console import console
from ycb.facilities import get_facilities

# Getting facility list
# curl 'https://www.onepa.gov.sg/pacesapi/FacilitySearch/GetFacilityOutlets'


if __name__ == '__main__':
    facilities = get_facilities()
    pass
