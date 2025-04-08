import csv
import json
import logging

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

# Класс возрващает иформацию о самолете
class plane_datamine:
    # Определям тип самолета
    def _get_type(self, json_data):
        result = ''
        # тут начались танцы с бубном
        # if 'type' in json_data:
        #             types = json_data['type']
        #   for item in types:
        #       if item == 'typeBomber':
        #           result = 'bomber'
        #           break
        #   if result == '':
        #        logging.warning(f'Самолет:{self.id} - тип самолета не найден')
        # else:
        if 'fightAiBehaviour' in json_data:
           if isinstance(json_data['fightAiBehaviour'], list):
              result = json_data['fightAiBehaviour'][0].replace('assault', 'strike')
           else:
              result = json_data['fightAiBehaviour'].replace('assault', 'strike')
        else:
            logging.warning(f'Самолет:{self.id} - тип самолета не найден')
            result = 'fighter'
        return result

    # Получаем флайт модель самолета
    def _get_flight_model(self, json_data):
        result = ''
        # Внезапно ключа с записью про флайт модель может не быть
        if 'fmFile' in json_data:
            # Может быть несколько флайт моделей, но беру последнею, потому что для последней есть файл, по идее надо
            # перебрать все файлы, но мне лень.
            if isinstance(json_data['fmFile'], list):
                result = json_data['fmFile'][1].replace('fm/', '').replace('.blk', '')
            else:
                result = json_data['fmFile'].replace('fm/', '').replace('.blk', '')
        else:
            logging.info(f'Самолет:{self.id} - файл флайт модели не найден')
            result = self.id
        return result

    def __init__(self, plane_name):
        self.id = plane_name
        full_file_name = f'{flightmodels_path}\\{self.id}.blkx'
        # Открываем его, насчет закрытия не паримся, его закроет магия выхода за область видимиости
        with open(full_file_name, 'r') as file:
            main_data = json.load(file)
            self.flight_model = self._get_flight_model(main_data)
            self.name = {'English':units_name[f'{self.id}_0']}
            self.type = self. _get_type(main_data)