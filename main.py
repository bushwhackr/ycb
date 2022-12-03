import datetime

from ycb.outlet import get_outlets

if __name__ == '__main__':
    outlets = get_outlets()
    test = outlets[4].ccList[0].lookup("BADMINTON COURTS", date=datetime.date(2022, 12, 18))
    pass
