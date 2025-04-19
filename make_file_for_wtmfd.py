import wt_datamine
import json
import glob
import csv
import wt_datamine

# Список самолетов который нам интересен, если пусто, то обработаем все
list_plane = [
    'a-20g'
    ]

if __name__ == "__main__":

    for plane_id in list_plane:
        plane_datamine = wt_datamine.WTPlaneFullInfo(plane_id)
        print(plane_datamine.get_all())
