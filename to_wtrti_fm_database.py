import json
import glob
import csv

# Каталог откуда считываем основные модели
root_dir = '.\\War-Thunder-Datamine-master\\'
lang_dir = f'{root_dir}\\lang.vromfs.bin_u\\lang\\'
flightmodels_path = f'{root_dir}\\aces.vromfs.bin_u\\gamedata\\flightmodels\\'
# \War-Thunder-Datamine-master\lang.vromfs.bin_u\lang\units.csv
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
res = glob.glob('{}*.blkx'.format(flightmodels_path))
# Список файлов есть, пошли по нему
for file in res:
    # Нам нужно как короткое так и полное имя, дальше будет понятно зачем
    full_file_name = file
    short_file_name = file.replace(flightmodels_path, '')

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
            cvs_row_name['Name'] = short_file_name.replace('.blkx', '')
            cvs_row_name['FmName'] = main_data['fmFile'].replace('fm/', '').replace('.blk', '')
            cvs_row_name['Type'] = main_data['fightAiBehaviour'].replace('assault', 'strike')

            with open(f'{lang_dir}\\units.csv', newline='', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';')
                for row in spamreader:
                    if row[0] == f'{cvs_row_name['Name']}_shop':
                        cvs_row_name['English'] = row[1]
                        break

            # Добавлям в нашу строку для  CSV модель самолета
            cvs_row_data['Name'] = main_data['model']
            # Читаем из основго файла имя файла флайт модели, но меням расширение на blkx, вот я хз почему так.
            fm_file_name = '{}{}'.format(flightmodels_path, main_data['fmFile'].replace('blk', 'blkx'))
            with open(fm_file_name, 'r') as fm_file:
                # Прочитали данные из флайт модели
                fm_data = json.load(fm_file)
                cvs_row_data['Length'] = fm_data['Length']

                if 'Aerodynamics' in fm_data and 'WingPlane' in fm_data['Aerodynamics'] and 'Span' in \
                        fm_data['Aerodynamics']['WingPlane']:
                    cvs_row_data['WingSpan'] = fm_data['Aerodynamics']['WingPlane']['Span']
                else:
                    cvs_row_data['WingSpan'] = fm_data['Wingspan']

                if 'Aerodynamics' in fm_data and 'WingPlane' in fm_data['Aerodynamics'] and 'Areas' in \
                        fm_data['Aerodynamics']['WingPlane']:
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

                if 'Aerodynamics' in fm_data and 'WingPlane' in fm_data['Aerodynamics'] and 'Strength' in \
                        fm_data['Aerodynamics']['WingPlane']:
                    cvs_row_data['CritAirSpd'] = int(fm_data['Aerodynamics']['WingPlane']['Strength']['VNE'])
                    cvs_row_data['CritAirSpdMach'] = (fm_data['Aerodynamics']['WingPlane']['Strength']['MNE'])
                else:
                    cvs_row_data['CritAirSpd'] = int(fm_data['Vne'])
                    cvs_row_data['CritAirSpdMach'] = (fm_data['VneMach'])

                cvs_row_data['CritGearSpd'] = int(fm_data['Mass']['GearDestructionIndSpeed'])

                if fm_data['Aerodynamics']["FlapsAxis"]["Combat"]["Presents"]:
                    cvs_row_data['CombatFlaps'] = int(fm_data['Aerodynamics']["FlapsAxis"]["Combat"]["Flaps"] * 100)
                else:
                    cvs_row_data['CombatFlaps'] = int(0)

                if fm_data['Aerodynamics']["FlapsAxis"]["Takeoff"]["Presents"]:
                    cvs_row_data['TakeoffFlaps'] = int(fm_data['Aerodynamics']["FlapsAxis"]["Takeoff"]["Flaps"] * 100)
                else:
                    cvs_row_data['TakeoffFlaps'] = int(0)
                CritFlapsSpd = ''
                for i in range(0, 4):
                    if f'FlapsDestructionIndSpeedP{i}' in fm_data["Mass"]:
                        CritFlapsSpd = f'{CritFlapsSpd},{fm_data["Mass"][f'FlapsDestructionIndSpeedP{i}'][0]},{int(fm_data["Mass"][f'FlapsDestructionIndSpeedP{i}'][1])}'
                cvs_row_data['CritFlapsSpd'] = CritFlapsSpd

                if 'Aerodynamics' in fm_data and 'WingPlane' in fm_data['Aerodynamics'] and 'Strength' in \
                        fm_data['Aerodynamics']['WingPlane']:
                    cvs_row_data[
                        'CritWingOverload'] = f'{fm_data["Aerodynamics"]["WingPlane"]["Strength"]["CritOverload"][0]},{fm_data["Aerodynamics"]["WingPlane"]["Strength"]["CritOverload"][1]}'
                else:
                    cvs_row_data[
                        'CritWingOverload'] = f'{fm_data["Mass"]["WingCritOverload"][0]},{fm_data["Mass"]["WingCritOverload"][1]}'

                cvs_row_data['NumEngines'] = int(0)
                if "Engine0" in fm_data:
                    cvs_row_data['NumEngines'] = cvs_row_data['NumEngines'] + 1

                if "Engine1" in fm_data:
                    cvs_row_data['NumEngines'] = cvs_row_data['NumEngines'] + 1

                cvs_row_data['RPM'] = f'{int(fm_data["EngineType0"]["Main"]["RPMMin"])},{int(fm_data["EngineType0"]["Main"]["RPMAfterburner"])},{int(fm_data["EngineType0"]["Main"]["RPMMaxAllowed"])}'

                cvs_row_data['MaxNitro'] = fm_data["Mass"]["MaxNitro"]

                cvs_row_data['NitroConsum'] = fm_data["EngineType0"]["Afterburner"]["NitroConsumption"]


                if 'Aerodynamics' in fm_data and 'WingPlane' in fm_data['Aerodynamics'] and 'FlapsPolar0' in fm_data['Aerodynamics']['WingPlane']:
                    cvs_row_data['CritAoA'] = f'{int(fm_data["Aerodynamics"]["WingPlane"]["FlapsPolar0"]["alphaCritLow"])},{int(fm_data["Aerodynamics"]["WingPlane"]["FlapsPolar1"]["alphaCritHigh"])},{int(fm_data["Aerodynamics"]["WingPlane"]["FlapsPolar1"]["alphaCritLow"])}'
                else:
                    cvs_row_data['CritAoA'] = f'{int(fm_data["Aerodynamics"]["NoFlaps"]["alphaCritLow"])},{int(fm_data["Aerodynamics"]["FullFlaps"]["alphaCritHigh"])},{int(fm_data["Aerodynamics"]["FullFlaps"]["alphaCritLow"])}'
#
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
    fieldnames = ['Name', 'FmName', 'Type', 'English']
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
                  'CritGearSpd', 'CombatFlaps', 'TakeoffFlaps', 'CritFlapsSpd','CritWingOverload','NumEngines','RPM','MaxNitro','NitroConsum','CritAoA']
    # Магия что бы excel открыл файл нормально
    writer = csv.DictWriter(csvfile, dialect='excel', delimiter=';', fieldnames=fieldnames)
    # Записываем заголовок
    writer.writeheader()
    # Записываем тело
    for row in cvs_data:
        writer.writerow(row)
