import json
import glob
import csv

# Каталог откуда считываем основные модели
dir_path = '.\\flightmodels\\'

# Список самолетов который нам интересен, если пусто, то обработаем все
list_plane = [
    'su_27sm',
    'su_30sm',
    'f-4s'
]

# Тело cvs файла fm_names_db.csv
cvs_name = []
# Тело cvs файла fm_data_db.csv
cvs_data = []

# Получить список файлов с расширением blkx из каталога dir_path
res = glob.glob('{}*.blkx'.format(dir_path))
# Список файлов есть, пошли по нему
for file in res:
    # Нам нужно как короткое так и полное имя, дальше будет понятно зачем
    full_file_name = file
    short_file_name = file.replace('.\\flightmodels\\', '')

    # Признак того, что надо обратботать файл, если массив is_process_file пустой то всегда истина
    is_process_file = not list_plane

    # Если массив не пуст то ищем имя файла без расширения в списке самолетов
    if not is_process_file:
        for plane in list_plane:
            is_process_file = short_file_name == '{}.blkx'.format(plane)
            if is_process_file:
                break

    # Если надо обработать файл
    if is_process_file:
        # Готовим для него строку
        cvs_row_name = {}
        cvs_row_data = {}
        # Открываем его, насчет закрытия не паримся, его закроет магия выхода за область видимиости
        with open(full_file_name, 'r') as file:
            main_data = json.load(file)

            # Заполняем информацию по наименованию самолета
            cvs_row_name['Name'] = main_data['model']
            cvs_row_name['FmName'] = main_data['fmFile'].replace('fm/','').replace('.blk','')
            #cvs_name['Type'] =
            # cvs_name['English'] =

            # Добавлям в нашу строку для  CSV модель самолета
            cvs_row_data['Name'] = main_data['model']
            # Читаем из основго файла имя файла флайт модели, но меням расширение на blkx, вот я хз почему так.
            fm_file_name = '{}{}'.format(dir_path, main_data['fmFile'].replace('blk', 'blkx'))
            with open(fm_file_name, 'r') as fm_file:
                # Прочитали данные из флайт модели
                fm_data = json.load(fm_file)
                cvs_row_data['Length'] = fm_data['Length']

                if 'Aerodynamics' in fm_data and 'WingPlane' in fm_data['Aerodynamics'] and 'Span' in fm_data['Aerodynamics']['WingPlane']:
                    cvs_row_data['WingSpan'] = fm_data['Aerodynamics']['WingPlane']['Span']
                else:
                    cvs_row_data['WingSpan'] = fm_data['Wingspan']

                if 'Aerodynamics' in fm_data and 'WingPlane' in fm_data['Aerodynamics'] and 'Areas' in fm_data['Aerodynamics']['WingPlane']:
                    cvs_row_data['WingArea'] = fm_data['Aerodynamics']['WingPlane']["Areas"]["LeftIn"] + \
                                           fm_data['Aerodynamics']['WingPlane']["Areas"]["LeftMid"] + \
                                           fm_data['Aerodynamics']['WingPlane']["Areas"]["LeftOut"] + \
                                           fm_data['Aerodynamics']['WingPlane']["Areas"]["RightIn"] + \
                                           fm_data['Aerodynamics']['WingPlane']["Areas"]["RightMid"] + \
                                           fm_data['Aerodynamics']['WingPlane']["Areas"]["RightOut"]
                else:
                    cvs_row_data['WingArea'] = fm_data["Areas"]["WingLeftIn"] + \
                                           fm_data["Areas"]["WingLeftMid"] + \
                                           fm_data["Areas"]["WingLeftOut"] + \
                                           fm_data["Areas"]["WingRightIn"] + \
                                           fm_data["Areas"]["WingRightMid"] + \
                                           fm_data["Areas"]["WingRightOut"]

                cvs_row_data['EmptyMass'] = int(fm_data['Mass']['EmptyMass'])
                cvs_row_data['MaxFuelMass'] = int(fm_data['Mass']['MaxFuelMass0'])

                if 'Aerodynamics' in fm_data and 'WingPlane' in fm_data['Aerodynamics'] and 'Strength' in fm_data['Aerodynamics']['WingPlane']:
                    cvs_row_data['CritAirSpd'] = int(fm_data['Aerodynamics']['WingPlane']['Strength']['VNE'])
                    cvs_row_data['CritAirSpdMach'] = (fm_data['Aerodynamics']['WingPlane']['Strength']['MNE'])
                else:
                    cvs_row_data['CritAirSpd'] = int(fm_data['Vne'])
                    cvs_row_data['CritAirSpdMach'] = (fm_data['VneMach'])


                cvs_row_data['CritGearSpd'] = int(fm_data['Mass']['GearDestructionIndSpeed'])

                ## Вынули АССОЦИАТИВНЫЙ масив с данными по массе. Там их много
                # mass = fm_data['Mass']
                # Выкинули нафиг .0 и занесли в нашу строку
                # cvs_row['Length'] = int(mass['Length'])

        # Добавили строку к нашему тельцу cvs файла
        cvs_name.append(cvs_row_name)
        cvs_data.append(cvs_row_data)


# Сохраняем все в файлы
with open('fm_names_db.csv', 'w', newline='') as csvfile:
    # Это заголовки, они совпадают с ключами в нашем ассоциативном массиве с информацией о самолетоах
    fieldnames = ['Name','FmName','Type','English']
    # Магия что бы excel открыл файл нормально
    writer = csv.DictWriter(csvfile, dialect='excel', delimiter=';', fieldnames=fieldnames)
    # Записываем заголовок
    writer.writeheader()
    # Записываем тело
    for row in cvs_name:
        writer.writerow(row)

with open('fm_data_db.csv', 'w', newline='') as csvfile:
    # Это заголовки, они совпадают с ключами в нашем ассоциативном массиве с информацией о самолетоах
    fieldnames = ['Name', 'Length', 'WingSpan', 'WingArea', 'EmptyMass', 'MaxFuelMass', 'CritAirSpd', 'CritAirSpdMach',
                  'CritGearSpd']
    # Магия что бы excel открыл файл нормально
    writer = csv.DictWriter(csvfile, dialect='excel', delimiter=';', fieldnames=fieldnames)
    # Записываем заголовок
    writer.writeheader()
    # Записываем тело
    for row in cvs_data:
        writer.writerow(row)
