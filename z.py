import csv

# Пример данных для записи
cvs_name = [
    {'Name': 'il-2m_mstitel', 'FmName': 'il-2m_mstitel', 'Type': 'strike', 'English': 'IL-2M "Avenger"'}
]

# Сохраняем все в файлы
with open('fm_names_db.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'FmName', 'Type', 'English']

    # Создаем объект writer
    writer = csv.DictWriter(csvfile, dialect='excel', delimiter=';', fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)

    # Записываем заголовок
    writer.writeheader()

    # Записываем тело, обходя кавычки
    for row in cvs_name:
        # Выбираем значения, не экранируя кавычки, для нужного формата
        writer.writerow({
            'Name': row['Name'],
            'FmName': row['FmName'],
            'Type': row['Type'],
            'English': row['English']  # Здесь кавычки уже находятся как нужно
        })

# Для проверки содержимого файла
with open('fm_names_db.csv', 'r', encoding='utf-8') as csvfile:
    print(csvfile.read())

