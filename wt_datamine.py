import csv
import json
import logging
import os

root_dir = '.\\War-Thunder-Datamine-master\\'
lang_dir = f'{root_dir}\\lang.vromfs.bin_u\\lang\\'
flightmodels_path = f'{root_dir}\\aces.vromfs.bin_u\\gamedata\\flightmodels\\'


class units_name:
    list_plane_name = []

    def __init__(self):
        with open(f'{lang_dir}\\units.csv', newline='', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';')
            is_header = True;
            for row in spamreader:
                if is_header:
                    self.header = row
                    is_header = False;
                else:
                    self.list_plane_name.append(row)

    def __getitem__(self, key):
        # Проверяем, есть ли ключ в списке
        result = None
        for row in self.list_plane_name:
            if key == row[0]:
                result = row[1]
                break;
        if result is not None:
            return result
        else:
            raise KeyError(f"Ключ '{key}' не найден.")


units_name = units_name()


# Класс возвращает информацию о самолете
class plane_datamine:

    # Определяем тип самолета.
    def _get_type(self, json_data):
        result = ''
        # тут начались танцы с бубном, е...кие.
        etalon_types = ['bomber', 'assault', 'fighter', 'helicopter']
        json_types = ['typeBomber', 'typeAssault', 'typeFighter']
        # Тип самолета это еще та угадайка

        # Тип смотрим на то как себя ведет он по аишному, причем может вести себя сильно по разному :) списочком
        if 'fightAiBehaviour' in json_data:
            if isinstance(json_data['fightAiBehaviour'], list):
                for item in json_data['fightAiBehaviour']:
                    if item in json_types:
                        result = item.replace('type', '').lower()
                        break
            else:
                result = json_data['fightAiBehaviour']

        # Продолжаем искать
        if result not in etalon_types:
            if 'type' in json_data:
                if isinstance(json_data['type'], list):
                    for item in json_data['type']:
                        if item in json_types:
                            result = item.replace('type', '').lower()
                            break
                else:
                    result = json_data['type'].replace('type', '').lower()

        # Проверям финальный вариант
        if result not in etalon_types:
            logging.warning(f'Самолет:{self.id} - тип самолета не найден')
        return result

    # Получаем флайт модель самолета
    def _get_flight_model(self, json_data):
        result = ''
        # Внезапно ключа с записью про флайт модель может не быть
        if 'fmFile' in json_data:
            # Может быть несколько флайт моделей, но беру последнею, потому что для последней есть файл, по идее надо
            # перебрать все файлы, но мне лень.
            if isinstance(json_data['fmFile'], list):
                result = json_data['fmFile'][1]
            else:
                result = json_data['fmFile']
            result = os.path.basename(result).replace('.blk', '')
        else:
            logging.info(f'Самолет:{self.id} - файл флайт модели не найден')
            result = self.id
        return result

    def _get_length(self, json_data):
        """Метод возвращает длину самолета, если атрибут не найден возвращает 0
        """
        result = 0
        if 'Length' in json_data:
            result = json_data['Length']
        else:
            logging.warning(f'Самолет:{self.id} - длину не нашли')
        return result

    def _wing_span(self, json_data):
        """Метод возвращает массив пар значений в которых записан размах крыла самолета в зависимости от того насколько у него разложено крыло.
        Для обычных самолетов возвращается массив вида [[0,<размах крыла>]], получить значение wing_span[0][1]
        Для самолетов с изменяемой стреловидностью массив будет иметь вид: [[0,<размах крыла>], [<стреловидность от 0 до 1>, <размах крыла>]]
        """
        result = []
        default = [0, 0]
        if 'Aerodynamics' in json_data and 'WingPlane' in json_data['Aerodynamics'] and 'Span' in json_data['Aerodynamics']['WingPlane']:
            default[1] = json_data['Aerodynamics']['WingPlane']['Span']
            result.append(default)
        else:
            if 'Wingspan' in json_data:
                default[1] = json_data['Wingspan']
                result.append(default)
            else:
                # Бывает и изменяемая стреловидность
                if 'Aerodynamics' in json_data and 'WingPlaneSweep0' in json_data['Aerodynamics']:
                    for i in range(0, 5):
                        row = [0, 0]
                        if f'WingPlaneSweep{i}' in json_data["Aerodynamics"]:
                            row[0] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Sweep']
                            row[1] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Span']
                            result.append(row)
                else:
                    logging.warning(f'Самолет:{self.id} - размах крыла не нашли')

        return result

    def _wing_area(self, json_data):
        """Метод возвращает массив пар значений в которых записан площадь крыла самолета в зависимости от того насколько у него разложено крыло.
        Для обычных самолетов возвращается массив вида [[0,<площадь крыла>]], получить значение wing_span[0][1]
        Для самолетов с изменяемой стреловидностью массив будет иметь вид: [[0,<площадь крыла>], [<стреловидность от 0 до 1>, <площадь крыла>]]
        """
        result = []
        default = [0, 0]
        if 'Aerodynamics' in json_data and 'WingPlane' in json_data['Aerodynamics'] and 'Areas' in json_data['Aerodynamics']['WingPlane']:
            default[1] = json_data['Aerodynamics']['WingPlane']["Areas"]["LeftIn"] + json_data['Aerodynamics']['WingPlane']["Areas"]["LeftMid"] + \
                         json_data['Aerodynamics']['WingPlane']["Areas"]["LeftOut"] + json_data['Aerodynamics']['WingPlane']["Areas"]["RightIn"] + \
                         json_data['Aerodynamics']['WingPlane']["Areas"]["RightMid"] + json_data['Aerodynamics']['WingPlane']["Areas"]["RightOut"]
            result.append(default)
        else:
            if 'Areas' in json_data:
                default[1] = json_data["Areas"]["WingLeftIn"] + json_data["Areas"]["WingLeftMid"] + json_data["Areas"]["WingLeftOut"] + json_data["Areas"][
                    "WingRightIn"] + json_data["Areas"]["WingRightMid"] + json_data["Areas"]["WingRightOut"]
                result.append(default)
            else:
                # Бывает и изменяемая стреловидность
                if 'Aerodynamics' in json_data and 'WingPlaneSweep0' in json_data['Aerodynamics']:
                    for i in range(0, 5):
                        row = [0, 0]
                        if f'WingPlaneSweep{i}' in json_data["Aerodynamics"]:
                            node = json_data["Aerodynamics"][f'WingPlaneSweep{i}']["Areas"]
                            row[0] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Sweep']
                            row[1] = node["LeftIn"] + node["LeftMid"] + node["LeftOut"] + node["RightIn"] + node["RightMid"] + node["RightOut"]
                            result.append(row)
                else:
                    logging.warning(f'Самолет:{self.id} - площадь крыла не нашли')
        return result

    def _empty_mass(self, json_data):
        """Метод возвращает сухую массу самолета, если не удалось посчитать то возвращаем 0
        """
        result = 0
        if 'Mass' in json_data and 'EmptyMass' in json_data['Mass']:
            result = int(json_data['Mass']['EmptyMass'])
        else:
            logging.warning(f'Самолет:{self.id} - сухую массу не нашли')
        return result

    def _max_fuel_mass(self, json_data):
        """Метод возвращает максимальное количество топлива.
        Если определить параметр не удалось, то возвращаем 0
        """
        result = 0
        if 'Mass' in json_data and 'MaxFuelMass0' in json_data['Mass']:
            result = json_data['Mass']['MaxFuelMass0']
        else:
            logging.warning(f'Самолет:{self.id} - максимальную массу топлива не нашли')
        return result

    def _crit_air_spd(self, json_data):
        """Метод возвращает массив пар значений в которых записан критические скорости в км/ч в зависимости от того насколько у него разложено крыло.
        Для обычных самолетов возвращается массив вида [[0,<критическая скорость>]], получить значение wing_span[0][1]
        Для самолетов с изменяемой стреловидностью массив будет иметь вид: [[0,<критическая скорость>], [<стреловидность от 0 до 1>, <критическая скорость>]]
        """
        result = []
        default = [0, 0]
        if 'Aerodynamics' in json_data and 'WingPlane' in json_data['Aerodynamics'] and 'Strength' in json_data['Aerodynamics']['WingPlane']:
            default[1] = int(json_data['Aerodynamics']['WingPlane']['Strength']['VNE'])
            result.append(default)
        else:
            if 'Vne' in json_data:
                default[1] = int(json_data['Vne'])
                result.append(default)
            else:
                # Бывает и изменяемая стреловидность
                if 'Aerodynamics' in json_data and 'WingPlaneSweep0' in json_data['Aerodynamics']:
                    for i in range(0, 5):
                        row = [0, 0]
                        if f'WingPlaneSweep{i}' in json_data["Aerodynamics"]:
                            row[0] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Sweep']
                            row[1] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Strength']['VNE']
                            result.append(row)
                else:
                    logging.warning(f'Самолет:{self.id} - критическую скорость в км/час не нашли')
        return result

    def _crit_air_spd_mach(self, json_data):
        """Метод возвращает массив пар значений в которых записан критические скорости в махах в зависимости от того насколько у него разложено крыло.
        Для обычных самолетов возвращается массив вида [[0,<критическая скорость>]], получить значение wing_span[0][1]
        Для самолетов с изменяемой стреловидностью массив будет иметь вид: [[0,<критическая скорость>], [<стреловидность от 0 до 1>, <критическая скорость>]]
        """
        result = []
        default = [0, 0]
        if 'Aerodynamics' in json_data and 'WingPlane' in json_data['Aerodynamics'] and 'Strength' in json_data['Aerodynamics']['WingPlane']:
            default[1] = (json_data['Aerodynamics']['WingPlane']['Strength']['MNE'])
            result.append(default)
        else:
            if 'VneMach' in json_data:
                default[1] = (json_data['VneMach'])
                result.append(default)
            else:
                # Бывает и изменяемая стреловидность
                if 'Aerodynamics' in json_data and 'WingPlaneSweep0' in json_data['Aerodynamics']:
                    for i in range(0, 5):
                        row = [0, 0]
                        if f'WingPlaneSweep{i}' in json_data["Aerodynamics"]:
                            row[0] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Sweep']
                            row[1] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Strength']['MNE']
                            result.append(row)
                else:
                    logging.warning(f'Самолет:{self.id} - критическую скорость в махах не нашли')
        return result

    def _crit_gear_spd(self, json_data):
        """Метод возвращает критическую скорость ВЫПУСКА шасси
        Если определить параметр не удалось, то возвращаем 0
        """
        result = 0
        if 'Mass' in json_data and 'GearDestructionIndSpeed' in json_data['Mass']:
            result = json_data['Mass']['GearDestructionIndSpeed']
        else:
            logging.warning(f'Самолет:{self.id} - скорость разрушения шасси не нашли')
        return result

    def _flaps(self, json_data):
        """Метод возвращает позицию закрылок для самолета в процентах
        Словарь имеет вид: {'Combat':16, 'Takeoff':19}
        Если определить параметр не удалось, то возвращаем пустой словарь
        """
        result = {}
        if 'Aerodynamics' in json_data and "FlapsAxis" in json_data['Aerodynamics']:
            if json_data['Aerodynamics']["FlapsAxis"]["Combat"]["Presents"]:
                result['Combat'] = json_data['Aerodynamics']["FlapsAxis"]["Combat"]["Flaps"] * 100

            if json_data['Aerodynamics']["FlapsAxis"]["Takeoff"]["Presents"]:
                result['Takeoff'] = json_data['Aerodynamics']["FlapsAxis"]["Takeoff"]["Flaps"] * 100
        else:
            logging.warning(f'Самолет:{self.id} - позиций закрылок не нашли')
        return result

    def _crit_flaps_spd(self, json_data):
        """Метод возвращает массив пар значений [<процент выпуска закрыло>, <критическая скорость км/ч>]
        Если ничего не нашли, то пустой массив
        """
        result = []
        for i in range(0, 5):
            if "Mass" in json_data and f'FlapsDestructionIndSpeedP{i}' in json_data["Mass"]:
                crt_spped = json_data["Mass"][f'FlapsDestructionIndSpeedP{i}']
                if isinstance(crt_spped[0], float):
                    row = json_data["Mass"][f'FlapsDestructionIndSpeedP{i}']
                    result.append(row)
                else:
                    for item in crt_spped:
                        row = item
                        result.append(row)

        if "Mass" in json_data and 'FlapsDestructionIndSpeedP' in json_data["Mass"]:
            i = 0
            list = json_data["Mass"]['FlapsDestructionIndSpeedP']
            while i < len(list):
                row = [0,0]
                row[0] = list[i]
                row[1] = list[i+1]
                i = i+2
                result.append(row)
        else:
            logging.warning(f'Самолет:{self.id} - требуется уточнение по критическим скоростям закрылок')
        return result

    def _crit_wing_overload(self, json_data):
        """Метод возвращает параметры критического перегруза крыла в зависимости от угла раскрытия крыла
        Для обычных самолетов возвращается массив вида [[0,<параметр 1>, <параметр 2>]]
        Для самолетов с изменяемой стреловидностью массив будет иметь вид: [[0,<параметр 1>, <параметр 2>], [<стреловидность от 0 до 1>, <параметр 1>, <параметр 2>]]
        """
        result = []
        default = [0, 0, 0]
        if 'Aerodynamics' in json_data and 'WingPlane' in json_data['Aerodynamics'] and 'Strength' in json_data['Aerodynamics']['WingPlane']:
            default[1] = json_data["Aerodynamics"]["WingPlane"]["Strength"]["CritOverload"][0]
            default[2] = json_data["Aerodynamics"]["WingPlane"]["Strength"]["CritOverload"][1]
            result.append(default)
        else:
            if 'Mass' in json_data and "WingCritOverload" in json_data["Mass"]:
                default[1] = json_data["Mass"]["WingCritOverload"][0]
                default[2] = json_data["Mass"]["WingCritOverload"][1]
            else:
                # Бывает и изменяемая стреловидность
                if 'Aerodynamics' in json_data and 'WingPlaneSweep0' in json_data['Aerodynamics']:
                    for i in range(0, 5):
                        row = [0, 0, 0]
                        if f'WingPlaneSweep{i}' in json_data["Aerodynamics"]:
                            row[0] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Sweep']
                            row[1] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Strength']['CritOverload'][0]
                            row[2] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Strength']['CritOverload'][1]
                            result.append(row)
                else:
                    logging.warning(f'Самолет:{self.id} - скорость слома крыла не нашли')
        return result

    def _num_engines(self, json_data):
        """Метод возвращает количество двигателей в самолете
        Если определить параметр не удалось, то возвращаем 0
        """
        result = int(0)
        if "Engine0" in json_data:
            result += 1

        if "Engine1" in json_data:
            result += 1

        return result

    def _rpm(self, json_data):
        """Метод возвращает набор максимальных значений оборота двигателя, параметры читаюстся по первому двигателю :)
        Если определить параметр не удалось, то возвращаем 0
        """
        result = {}
        if "EngineType0" in json_data:
            result['RPMMin'] = int(json_data["EngineType0"]["Main"]["RPMMin"])
            result['RPMAfterburner'] = int(json_data["EngineType0"]["Main"]["RPMAfterburner"])
            result['RPMMaxAllowed'] = int(json_data["EngineType0"]["Main"]["RPMMaxAllowed"])
        else:
            logging.warning(f'Самолет:{self.id} - обороты двигателя не нашли')
        return result

    def _max_nitro(self, json_data):
        """Метод возвращает хрен его знает
        Если определить параметр не удалось, то возвращаем 0
        """
        result = 0
        if "Mass" in json_data and "MaxNitro" in json_data["Mass"]:
            result = json_data["Mass"]["MaxNitro"]
        else:
            logging.warning(f'Самолет:{self.id} - нитро не нашли')
        return result

    def _nitro_consum(self, json_data):
        """Метод возвращает хрен его знает
        Если определить параметр не удалось, то возвращаем 0
        """
        result = 0
        if "EngineType0" in json_data:
            result = json_data["EngineType0"]["Afterburner"]["NitroConsumption"]
        else:
            logging.warning(f'Самолет:{self.id} - форсаж на закисии озота не нашли')
        return result

    def _crit_aoa(self, json_data):
        """Метод возвращает массив словарей с критическими перегрузками. Тот кто понял почему массив, тому респект
        Для обычных самолетов возвращается массив вида [[0,<значение>, <значение>, <значение>, <значение>]]
        Для самолетов с изменяемой стреловидностью массив будет иметь вид: [[0,<значение>, <значение>, <значение>, <значение>], [<стреловидность от 0 до 1>, <значение>, <значение>, <значение>, <значение>]]
        """
        result = []
        default = [0, 0, 0, 0, 0]
        if 'Aerodynamics' in json_data and 'WingPlane' in json_data['Aerodynamics'] and 'FlapsPolar0' in json_data['Aerodynamics']['WingPlane'] and 'Aerodynamics' in json_data and 'WingPlane' in json_data['Aerodynamics'] and 'FlapsPolar1' in json_data['Aerodynamics']['WingPlane']:
            default[1] = json_data["Aerodynamics"]["WingPlane"]["FlapsPolar0"]["alphaCritHigh"]
            default[2] = json_data["Aerodynamics"]["WingPlane"]["FlapsPolar0"]["alphaCritLow"]
            default[3] = json_data["Aerodynamics"]["WingPlane"]["FlapsPolar1"]["alphaCritHigh"]
            default[4] = json_data["Aerodynamics"]["WingPlane"]["FlapsPolar1"]["alphaCritLow"]
            result.append(default)
        else:
            if 'Aerodynamics' in json_data and 'NoFlaps' in json_data['Aerodynamics']:
                default[1] = json_data["Aerodynamics"]["NoFlaps"]["alphaCritHigh"]
                default[2] = json_data["Aerodynamics"]["NoFlaps"]["alphaCritLow"]
                default[3] = json_data["Aerodynamics"]["FullFlaps"]["alphaCritHigh"]
                default[4] = json_data["Aerodynamics"]["FullFlaps"]["alphaCritLow"]
                result.append(default)
            else:
                if 'Aerodynamics' in json_data and 'WingPlane' in json_data['Aerodynamics'] and "Polar" in json_data["Aerodynamics"]["WingPlane"]:
                    default[1] = json_data["Aerodynamics"]["WingPlane"]["Polar"]["NoFlaps"]["alphaCritHigh"]
                    default[2] = json_data["Aerodynamics"]["WingPlane"]["Polar"]["NoFlaps"]["alphaCritLow"]
                    default[3] = json_data["Aerodynamics"]["WingPlane"]["Polar"]["FullFlaps"]["alphaCritLow"]
                    default[4] = json_data["Aerodynamics"]["WingPlane"]["Polar"]["FullFlaps"]["alphaCritHigh"]
                    result.append(default)
                else:
                    # Бывает и изменяемая стреловидность
                    if 'Aerodynamics' in json_data and 'WingPlaneSweep0' in json_data['Aerodynamics']:
                        for i in range(0, 5):
                            row = [0, 0, 0, 0, 0]
                            if f'WingPlaneSweep{i}' in json_data["Aerodynamics"]:
                                row[0] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['Sweep']
                                row[1] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['FlapsPolar0']["alphaCritHigh"]
                                row[2] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['FlapsPolar0']["alphaCritLow"]
                                row[3] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['FlapsPolar1']["alphaCritHigh"]
                                row[4] = json_data["Aerodynamics"][f'WingPlaneSweep{i}']['FlapsPolar1']["alphaCritLow"]
                                result.append(row)
                    else:
                        logging.warning(f'Самолет:{self.id} - критические углы не нашли')
        return result

    # Загружаем данные из флайт модели при создании объекта
    def __init__(self, plane_name):
        self.id = plane_name
        full_file_name = f'{flightmodels_path}\\{self.id}.blkx'
        # Открываем его, насчет закрытия не паримся, его закроет магия выхода за область видимиости
        with open(full_file_name, 'r') as file:
            main_data = json.load(file)
            self.flight_model = self._get_flight_model(main_data)
            self.name = {'English': units_name[f'{self.id}_0']}
            self.type = self._get_type(main_data)

            # Читаем данные из конкретной флайт модели для самолета.
            fm_file_name = f'{flightmodels_path}\\fm\\{self.flight_model}.blkx'
            with open(fm_file_name, 'r') as fm_file:
                # Прочитали данные из флайт модели
                fm_data = json.load(fm_file)
                self.length = self._get_length(fm_data)
                self.wing_span = self._wing_span(fm_data)
                self.wing_area = self._wing_area(fm_data)
                self.empty_mass = self._empty_mass(fm_data)
                self.max_fuel_mass = self._max_fuel_mass(fm_data)
                self.crit_air_spd = self._crit_air_spd(fm_data)
                self.crit_air_spd_mach = self._crit_air_spd_mach(fm_data)
                self.crit_gear_spd = self._crit_gear_spd(fm_data)
                self.flaps = self._flaps(fm_data)
                self.crit_flaps_spd = self._crit_flaps_spd(fm_data)
                self.crit_wing_overload = self._crit_wing_overload(fm_data)
                self.num_engines = self._num_engines(fm_data)
                self.rpm = self._rpm(fm_data)
                self.max_nitro = self._max_nitro(fm_data)
                self.nitro_consum = self._nitro_consum(fm_data)
                self.crit_aoa = self._crit_aoa(fm_data)
