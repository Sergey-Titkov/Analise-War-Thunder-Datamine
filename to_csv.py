import json
import glob
import csv

# Каталог откуда считываем основные модели
dir_path = '.\\flightmodels\\'

# Список самолетов который нам интересен, если пусто, то обработаем все
list_plane = [
    'tornado_adv',
    'su-7bmk',
    'mirage_f1c_200',

]

# Тело cvs файла, пока пустое
cvs_body = []

# Получить список файлов с расширением blkx из каталога dir_path
res = glob.glob('{}*.blkx'.format(dir_path))
# Список файлов есть, пошли по нему
for file in res:
    # Нам нужно как короткое так и полное имя, дальше будет понятно зачем
    full_file_name = file
    short_file_name = file.replace('.\\flightmodels\\', '')

    # Признак того, что надо обработать файл, если массив is_process_file пустой то всегда истина
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
        cvs_row = {}
        # Открываем его, насчет закрытия не паримся, его закроет магия выхода за область видимиости
        with open(full_file_name, 'r') as file:
            main_data = json.load(file)
            # Добавлям в нашу строку для  CSV модель самолета
            cvs_row['Самолет'] = main_data['model']
            # Читаем из основго файла имя файла флайт модели, но меням расширение на blkx, вот я хз почему так.
            fm_file_name = '{}{}'.format(dir_path, main_data['fmFile'].replace('blk', 'blkx'))
            with open(fm_file_name, 'r') as fm_file:
                # Прочитали данные из флайт модели
                fm_data = json.load(fm_file)
                # Вынули АССОЦИАТИВНЫЙ масив с данными по массе. Там их много
                mass = fm_data['Mass']
                # Выкинули нафиг .0 и занесли в нашу строку
                cvs_row['Сухая масса, кг'] = int(mass['EmptyMass'])

        # Добавили строку к нашему тельцу cvs файла
        cvs_body.append(cvs_row)

# Сеанс записи в cvs файл.
with open('names.csv', 'w', newline='') as csvfile:
    # Это заголовки, они совпадают с ключами в нашем ассоциативном массиве с информацией о самолетоах
    fieldnames = ['Самолет', 'Сухая масса, кг']
    # Магия что бы excel открыл файл нормально
    writer = csv.DictWriter(csvfile, dialect='excel', delimiter=';', fieldnames=fieldnames)
    # Записываем заголовок
    writer.writeheader()
    # Записываем тело
    for row in cvs_body:
        writer.writerow(row)
