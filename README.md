# War Thunder Plane Info

Библиотека предназначена для получения параметров самолетов из файлов датамайна.
Это нужно например для сравнения изменений которые вносит разработчик.
Как использовать, посмотрим на простом примере:
1. Скачать репозиторий вот отсюда: https://github.com/gszabi99/War-Thunder-Datamine/tree/master 
Спасибо gszabi99 огромное за офигенную работу!
2. Разархивировать в каталог где собираетесь работать.
Выглядеть это будет вот так:
```
Ваш каталог/
└── War-Thunder-Datamine-master
    ├── .github
    ├── aces.vromfs.bin_u
    ├── atlases.vromfs.bin_u
    ├── char.vromfs.bin_u
    ├── game.vromfs.bin_u
    ├── gui.vromfs.bin_u
    ├── images.vromfs.bin_u
    ├── lang.vromfs.bin_u
    ├── mis.vromfs.bin_u
    ├── raw
    ├── regional.vromfs.bin_u
    ├── tex.vromfs.bin_u
    ├── webUi.vromfs.bin_u
    ├── wwdata.vromfs.bin_u
    ├── .gitattributes
    ├── README.md
    └──  version
```
Все как положено, инициализируем окружение, питон нужен не ниже 3.13.2
Устанавливаем пакет: ```pip install war-thunder-plane-info```
Создаем в корне файл: test.py
```
Ваш каталог/
├── War-Thunder-Datamine-master
│    ├── .github/
│    ├── aces.vromfs.bin_u/
│    ├── atlases.vromfs.bin_u/
│    ├── char.vromfs.bin_u/
│    ├── game.vromfs.bin_u/
│    ├── gui.vromfs.bin_u/
│    ├── images.vromfs.bin_u/
│    ├── lang.vromfs.bin_u/
│    ├── mis.vromfs.bin_u/
│    ├── raw/
│    ├── regional.vromfs.bin_u/
│    ├── tex.vromfs.bin_u/
│    ├── webUi.vromfs.bin_u/
│    ├── wwdata.vromfs.bin_u/
│    ├── .gitattributes
│    ├── README.md
│    └──  version
└── test.py
```
Добавляем в test.py следующий код:
``` python
import war_thunder_plane_info.wt as wt

list_plane = [
    'er-2_m105_tat'
    ]

if __name__ == "__main__":
    for plane_id in list_plane:
        plane_datamine = wt.WTPlaneFullInfo(plane_id)
        print(plane_datamine.get_all())
```
Запускаем, получаем:
``` json
{'PlaneID': 'er-2_m105_tat', 'Name': {'English': 'Yer-2\xa0(M-105)\xa0TAT-BT'}, 'fmFile': 'fm/er-2_m105_mv3.blkx', 'Type': 'bomber', 'FmID': 'er-2_m105_mv3', 'Length': 16.4, 'WingSpan': [[0, 21.686]], 'WingArea': [[0, 73.156]], 'EmptyMass': 7236, 'MaxFuelMass': 3500.0, 'VNE': [[0, 556]], 'MNE': [[0, 0.68]], 'VLO': 300.0, 'Flaps': {'Combat': 20.0, 'Takeoff': 33.0}, 'VFE': [[0.1, 470.0], [1.0, 270.0]], 'CritWingOverload': [[0, -148000.0, 222000.0]], 'NumEngines': 2, 'RPM': {'RPMMin': 450, 'RPMMax': 2700, 'RPMMaxAllowed': 2850}, 'MaxNitro': 0.0, 'NitroConsum': 0.0, 'CritAoA': [[0, 13.5, -10.0, 12.5, -10.0]]}
```
Пожалуйста :)
