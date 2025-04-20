import csv
import json
import logging
import os

root_dir = '.\\War-Thunder-Datamine-master\\'
lang_dir = f'{root_dir}\\lang.vromfs.bin_u\\lang\\'
flightmodels_path = f'{root_dir}\\aces.vromfs.bin_u\\gamedata\\flightmodels\\'

class WTUnitsName:
    r"""Класс позволяет получить по ID техники ее наименование.
    Формат использования wt_units_name[<ID техники>]
    Данные считываются из файла units.csv, обычно он находится в каталоге:.\War-Thunder-Datamine-master\lang.vromfs.bin_u\lang\
    Если пути отличны от стандартных то можно вызвать конструктор и передать ему полный путь.
    """

    list_plane_name = []

    def __init__(self,file_name=r"".join([lang_dir, "\\", r'units.csv'])):
        r"""Загружает данные из файла units.csv, если файла нет, будет ошибка
        :param file_name: путь до файла units.csv, по умолчанию .\War-Thunder-Datamine-master\lang.vromfs.bin_u\lang\units.csv
        """
        # Все из за этой херни
        # SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 785-786: truncated \uXXXX escape
        with open(file_name, newline='', encoding='utf-8') as csvfile:
            cvs_reader = csv.reader(csvfile, delimiter=';')
            # Пропустили заголовок
            next(cvs_reader)
            for row in cvs_reader:
                self.list_plane_name.append(row)

    def __getitem__(self, key):
        # Проверяем, есть ли ключ в списке
        result = None
        for row in self.list_plane_name:
            if key == row[0]:
                result = row[1]
                break
        if result is not None:
            return result
        else:
            raise KeyError(f"Ключ '{key}' не найден.")

class WTFlightModel:
    """Класс набор параметров из флайт модели самолета
    Формат использования WTFlightModel[<Имя параметра>]
    """
    def _get_length(self, json_data):
        """Метод возвращает длину самолета, если атрибут не найден возвращает 0
        """
        result = 0
        if 'Length' in json_data:
            result = json_data['Length']
        else:
            logging.warning(f'Самолет:{self._data['FmID']} - длину не нашли')
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
                    logging.warning(f'Самолет:{self._data['FmID']} - размах крыла не нашли')

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
                    logging.warning(f'Самолет:{self._data['FmID']} - площадь крыла не нашли')
        return result

    def _empty_mass(self, json_data):
        """Метод возвращает сухую массу самолета, если не удалось посчитать то возвращаем 0
        """
        result = 0
        if 'Mass' in json_data and 'EmptyMass' in json_data['Mass']:
            result = int(json_data['Mass']['EmptyMass'])
        else:
            logging.warning(f'Самолет:{self._data['FmID']} - сухую массу не нашли')
        return result

    def _max_fuel_mass(self, json_data):
        """Метод возвращает максимальное количество топлива.
        Если определить параметр не удалось, то возвращаем 0
        """
        result = 0
        if 'Mass' in json_data and 'MaxFuelMass0' in json_data['Mass']:
            result = json_data['Mass']['MaxFuelMass0']
        else:
            logging.warning(f'Самолет:{self._data['FmID']} - максимальную массу топлива не нашли')
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
                    logging.warning(f'Самолет:{self._data['FmID']} - критическую скорость в км/час не нашли')
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
                    logging.warning(f'Самолет:{self._data['FmID']} - критическую скорость в махах не нашли')
        return result

    def _crit_gear_spd(self, json_data):
        """Метод возвращает критическую скорость ВЫПУСКА шасси
        Если определить параметр не удалось, то возвращаем 0
        """
        result = 0
        if 'Mass' in json_data and 'GearDestructionIndSpeed' in json_data['Mass']:
            result = json_data['Mass']['GearDestructionIndSpeed']
        else:
            logging.warning(f'Самолет:{self._data['FmID']} - скорость разрушения шасси не нашли')
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
            return result

        if 'AvailableControls' in json_data:
            if "hasCombatFlapsPosition" in json_data['AvailableControls'] and json_data['AvailableControls']["hasCombatFlapsPosition"]:
                result['Combat'] = 20

            if "hasTakeoffFlapsPosition" in json_data['AvailableControls'] and json_data['AvailableControls']["hasTakeoffFlapsPosition"]:
                result['Takeoff'] = 33
            return result

        logging.warning(f'Самолет:{self._data['FmID']} - позиций закрылок не нашли')
        return result

    def _crit_flaps_spd(self, json_data):
        """Метод возвращает массив пар значений [<процент выпуска закрыло>, <критическая скорость км/ч>]
        Если ничего не нашли, то пустой массив
        """
        result = []
        # Сначала проверяем есть ли вообще управление закрылками
        value = self._get_value_from_node(json_data, ["AvailableControls", "hasFlapsControl"])
        if value is not None:
            # Управления нет, возвращаем пустой массив и без разницы какие там значения в ФМ модели
            if not value:
                return result

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
            list_fds = json_data["Mass"]['FlapsDestructionIndSpeedP']
            while i < len(list_fds):
                row = [0,0]
                row[0] = list_fds[i]
                row[1] = list_fds[i+1]
                i = i+2
                result.append(row)
        if len(result)==0:
            logging.warning(f'Самолет:{self._data['FmID']} - требуется уточнение по критическим скоростям закрылок')
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
                result.append(default)
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
                    logging.warning(f'Самолет:{self._data['FmID']} - скорость слома крыла не нашли')
        return result

    def _num_engines(self, json_data):
        """Метод возвращает количество двигателей в самолете, это просто квест какой то
        Если определить параметр не удалось, то возвращаем 0
        """
        result = int(0)
        for i in range(0,8):
            if f"Engine{i}" in json_data:
                engine = json_data[f"Engine{i}"]

                # Проверям тип двигателя, он должен быть внешним
                if "External" in engine:
                    if not engine["External"]:
                        result += 1
                        continue

                # Тогда смотрим тип его по типу двигателя
                if "Type" in engine:
                    if not json_data[f"EngineType{engine["Type"]}"]["External"]:
                        result += 1
                        continue

                # Ну хоть пропеллер, то есть
                if "Propellor" in engine:
                    result += 1
                    continue

            else:
                break

        return result

    def _rpm(self, json_data):
        """Метод возвращает набор максимальных значений оборота двигателя, параметры читаются по первому двигателю
        Если определить параметр не удалось, то возвращаем 0
        """
        result = {}
        if "EngineType0" in json_data:
            result['RPMMin']         = int(json_data["EngineType0"]["Main"]["RPMMin"])
            result['RPMMax'] = int(json_data["EngineType0"]["Main"]["RPMMax"])
            result['RPMMaxAllowed']  = int(json_data["EngineType0"]["Main"]["RPMMaxAllowed"])
            return result

        if "Engine0" in json_data and "Main" in json_data["Engine0"]:
            node = json_data["Engine0"]["Main"]
            if "RPMMin" in node:
                result['RPMMin']         = int(json_data["Engine0"]["Main"]["RPMMin"])

            # Это бывает массивом... Например: do_17z_2
            if "RPMAfterburner" in json_data["Engine0"]["Main"]:
                node = json_data["Engine0"]["Main"]["RPMMax"]
                if isinstance(node, list):
                    result['RPMMax'] = int(node[0])
                else:
                    result['RPMMax'] = int(node)

            if "RPMMaxAllowed" in json_data["Engine0"]["Main"]:
                result['RPMMaxAllowed']  = int(json_data["Engine0"]["Main"]["RPMMaxAllowed"])
            return result

        logging.warning(f'Самолет:{self._data['FmID']} - обороты двигателя не нашли')
        return result

    def _max_nitro(self, json_data):
        """Метод возвращает хрен его знает
        Если определить параметр не удалось, то возвращаем 0
        """
        result = 0
        if "Mass" in json_data and "MaxNitro" in json_data["Mass"]:
            result = json_data["Mass"]["MaxNitro"]
        else:
            logging.warning(f'Самолет:{self._data['FmID']} - нитро не нашли')
        return result

    def _get_value_from_node(self,node,path):
        """Метод возвращает значение ноды указанной в пути
        Если нода не существует, то возвращается: None
        Пример вызова: get_value_from_node(json_data,["Engine0","Afterburner","NitroConsumption"])
        """
        result = node
        for node_name in path:
            if node_name in result:
                result = result[node_name]
            else:
                result = None
                break
        return result

    def _nitro_consum(self, json_data):
        """Метод возвращает хрен его знает
        Если определить параметр не удалось, то возвращаем 0
        """
        result = 0
        if "EngineType0" in json_data:
            result = json_data["EngineType0"]["Afterburner"]["NitroConsumption"]
            return result

        value = self._get_value_from_node(json_data,["Engine0","Afterburner","NitroConsumption"])
        if value is not None:
            result = value
            return result

        logging.warning(f'Самолет:{self._data['FmID']} - форсаж на закисии озота не нашли')
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
                        logging.warning(f'Самолет:{self._data['FmID']} - критические углы не нашли')
        return result

    def __init__(self,file_name):
        self._data = {}  # Внутренний словарь для хранения свойств
        # Читаем данные из файла флайт модели для самолета.
        with open(file_name, 'r') as fm_file:
            # Прочитали данные из флайт модели
            fm_data = json.load(fm_file)
            self._data['FmID'] = os.path.basename(file_name).replace('.blkx', '')
            self._data['Length'] = self._get_length(fm_data)
            self._data['WingSpan'] = self._wing_span(fm_data)
            self._data['WingArea'] = self._wing_area(fm_data)
            self._data['EmptyMass'] = self._empty_mass(fm_data)
            self._data['MaxFuelMass'] = self._max_fuel_mass(fm_data)
            self._data['VNE'] = self._crit_air_spd(fm_data)
            self._data['MNE'] = self._crit_air_spd_mach(fm_data)
            self._data['VLO'] = self._crit_gear_spd(fm_data)
            self._data['Flaps'] = self._flaps(fm_data)
            self._data['VFE'] = self._crit_flaps_spd(fm_data)
            self._data['CritWingOverload'] = self._crit_wing_overload(fm_data)
            self._data['NumEngines'] = self._num_engines(fm_data)
            self._data['RPM'] = self._rpm(fm_data)
            self._data['MaxNitro'] = self._max_nitro(fm_data)
            self._data['NitroConsum'] = self._nitro_consum(fm_data)
            self._data['CritAoA'] = self._crit_aoa(fm_data)

    def __getitem__(self, key):
        """Вернуть значение по ключу."""
        return self._data[key]

    def __iter__(self):
        """Итерация по ключам."""
        return iter(self._data)

    def keys(self):
        """Возвращает список ключей (аналогично dict.keys())."""
        return self._data.keys()

    def values(self):
        """Возвращает список значений (аналогично dict.values())."""
        return self._data.values()

    def get(self, key, default=None):
        """Возвращает значение по ключу или default, если ключа нет."""
        return self._data.get(key, default)

    def get_all(self):
        """Возвращает все значения флайт модели"""
        return self._data.copy()

class WTPlaneModel:
    """Класс набор параметров из модели самолета
    Формат использования WTPlaneModel[<Имя параметра>]
    """
    _units_name = None

    # Определяем тип самолета.
    def _get_type(self, json_data):
        """
        Функция возвращает тип самолета, зачем он нужен не очень понятно
        :param json_data: Данные считанные из файла модели самолета
        :return: тип самолета
        """
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
            logging.warning(f'Самолет:{self._data['PlaneID']} - тип самолета не найден')
        return result

    # Получаем флайт модель самолета
    def _get_flight_model(self, json_data):
        """
        Функция возвращает относительный путь до файла флайт модели, технически они все лежат в каталоге fm, но разве что-нибудь может пойти не так
        :param json_data: Данные считанные из файла модели самолета
        :return: относительный путь до флайт модели и файл флайт модели
        """
        result = ''
        # Внезапно ключа с записью про флайт модель может не быть
        if 'fmFile' in json_data:
            # Может быть несколько флайт моделей, но беру последнею, потому что для последней есть файл, по идее надо
            # перебрать все файлы, но мне лень.
            if isinstance(json_data['fmFile'], list):
                result = json_data['fmFile'][1]
            else:
                result = json_data['fmFile']
            #result = os.path.basename(result).replace('.blk', '')
        else:
            logging.info(f'Самолет:{self._data['PlaneID']} - файл флайт модели не найден')
            result = f'fm/{self._data['PlaneID']}'

        # Вот эта фигня объяснятся просто, в некоторых файлах забыли добавить .blk поэтому мне приходится все выглаживать гадая на шанике
        result = f'{result.replace('.blk', '')}.blkx'
        return result

    def __init__(self, plane_id = '', file_name = '', units_name = WTUnitsName()):
        """Загружает данные из модели самолета
        :param plane_id: ID самолета, совпадает с именем файла(без расширения) модели самолета. Используется в том случае если расположение данных по умолчанию
        :param file_name: Путь до файла с моделью самолета, если задано то будет использоваться оно.
        :param units_name: Используется в том случае если расположение данных отличается от рекомендованных, тогда должно иметь вид: WTUnitsName(<Путь до файла units.csv>)
        """
        self._data = {}  # Внутренний словарь для хранения свойств
        if WTPlaneModel._units_name is None:
            WTPlaneModel._units_name = units_name
            pass

        full_file_name = f'{flightmodels_path}\\{plane_id}.blkx'
        if file_name != '':
            full_file_name = file_name
            plane_id = os.path.basename(full_file_name).replace('.blk', '')

        self._data['PlaneID'] = plane_id

        # Открываем его, насчет закрытия не паримся, его закроет магия выхода за область видимиости
        with open(full_file_name, 'r') as file:
            main_data = json.load(file)
            self.flight_model = self._get_flight_model(main_data)
            try:
                self._data['Name'] = {'English': WTPlaneModel._units_name[f'{plane_id}_0']}
            except KeyError:
                self._data['Name'] = {'English': f'{plane_id}_0'}
            self._data['fmFile'] = self._get_flight_model(main_data)
            self._data['Type'] = self._get_type(main_data)

    def __getitem__(self, key):
        """Вернуть значение по ключу."""
        return self._data[key]

    def __iter__(self):
        """Итерация по ключам."""
        return iter(self._data)

    def keys(self):
        """Возвращает список ключей (аналогично dict.keys())."""
        return self._data.keys()

    def values(self):
        """Возвращает список значений (аналогично dict.values())."""
        return self._data.values()

    def get(self, key, default=None):
        """Возвращает значение по ключу или default, если ключа нет."""
        return self._data.get(key, default)

    def get_all(self):
        """Возвращает все значения флайт модели"""
        return self._data.copy()

# Класс возвращает информацию о самолете
class WTPlaneFullInfo:
    """ Класс возвращает полную информацию о самолете
    Формат использования WTPlaneModel[<Имя параметра>]
    """

    def __init__(self, plane_id = '', file_name = '', units_name = WTUnitsName()):
        """Загружает данные из модели самолета
        :param plane_id: ID самолета, совпадает с именем файла(без расширения) модели самолета. Используется в том случае если расположение данных по умолчанию
        :param file_name: Путь до файла с моделью самолета, если задано то будет использоваться оно.
        :param units_name: Используется в том случае если расположение данных отличается от рекомендованных, тогда должно иметь вид: WTUnitsName(<Путь до файла units.csv>)
        """
        self._data = {}  # Внутренний словарь для хранения свойств

        plane_model  = WTPlaneModel(plane_id = plane_id, file_name = file_name, units_name = units_name)
        self._data = plane_model.get_all()

        fm_file_path = f'{flightmodels_path}'
        if file_name != '':
            fm_file_path = os.path.dirname(file_name)

        fm_file_path = f'{fm_file_path}\\{self._data['fmFile']}'
        flight_model = WTFlightModel(fm_file_path)
        self._data.update(flight_model.get_all())

    def __getitem__(self, key):
        """Вернуть значение по ключу."""
        return self._data[key]

    def __iter__(self):
        """Итерация по ключам."""
        return iter(self._data)

    def keys(self):
        """Возвращает список ключей (аналогично dict.keys())."""
        return self._data.keys()

    def values(self):
        """Возвращает список значений (аналогично dict.values())."""
        return self._data.values()

    def get(self, key, default=None):
        """Возвращает значение по ключу или default, если ключа нет."""
        return self._data.get(key, default)

    def get_all(self):
        """Возвращает все значения флайт модели"""
        return self._data.copy()