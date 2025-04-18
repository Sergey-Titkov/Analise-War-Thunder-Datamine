a = -1000

if a is None:
    print(1)
else:
    print(2)

# import csv
#
#
# import csv
#
# # Пример данных
# data = [
#     [0.1234, 2.56789, 3.0],
#     [4.5, 5.678, 6.9999],
#     [7.123456, 8.9, 9.1111],
#     [14, 15.0, 16.0001]  # Пример с целыми числами
# ]
#
# with open('numbers.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     for row in data:
#         formatted_row = []
#         for num in row:
#             # Форматируем число с тремя знаками после запятой
#             s = f"{num:.3f}"
#             # Убираем .000 для целых чисел
#             if s.endswith('.000'):
#                 s = s[:-4]
#             formatted_row.append(s)
#         writer.writerow(formatted_row)
#
# print("Данные успешно записаны в numbers.csv")
#
# list_row = []
# header = []
# with open(f'fm_data_db_etalon.csv', newline='', encoding='utf-8') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=';')
#     is_header = True;
#     for row in spamreader:
#         if is_header:
#             header = row
#             is_header = False;
#         else:
#             list_row.append(row)
#
# with open(f'fm_data_db_etalon_.csv', 'w', newline='', encoding='utf-8') as csvfile:
#     # Магия что бы excel открыл файл нормально
#     writer = csv.writer(csvfile, dialect='excel', delimiter=';')
#     writer.writerow(header)
#     # Записываем тело
#     for row in list_row:
#         row[1] = f"{float(row[1]):.5f}"
#
#         if row[2].find(',') ==-1:
#             row[2] = f"{float(row[2]):.5f}"
#         else:
#             lists = row[2].split(',')
#             result = ''
#             for item in lists:
#                 result = f'{result},{float(item):.1f}'
#             row[2] = result[1:]
#
#         if row[3].find(',') ==-1:
#             row[3] = f"{float(row[3]):.5f}"
#         else:
#             lists = row[3].split(',')
#             result = ''
#             for item in lists:
#                 result = f'{result},{float(item):.1f}'
#             row[3] = result[1:]
#
#         row[4] = f"{float(row[4]):.5f}"
#         row[5] = f"{float(row[5]):.5f}"
#
#         if row[6].find(',') ==-1:
#             row[6] = f"{float(row[6]):.5f}"
#         else:
#             lists = row[6].split(',')
#             result = ''
#             for item in lists:
#                 result = f'{result},{float(item):.1f}'
#             row[6] = result[1:]
#
#         if row[7].find(',') ==-1:
#             row[7] = f"{float(row[7]):.5f}"
#         else:
#             lists = row[7].split(',')
#             result = ''
#             for item in lists:
#                 result = f'{result},{float(item):.1f}'
#             row[7] = result[1:]
#
#         row[8] = f"{float(row[8]):.5f}"
#         row[9] = f"{float(row[9]):.5f}"
#         row[10] = f"{float(row[10]):.5f}"
#
#         if row[11] != '':
#             if row[11].find(',') ==-1:
#                 row[11] = f"{float(row[11]):.5f}"
#             else:
#                 lists = row[11].split(',')
#                 result = ''
#                 for item in lists:
#                     result = f'{result},{float(item):.1f}'
#                 row[11] = result[1:]
#
#         if row[12].find(',') ==-1:
#             row[12] = f"{float(row[12]):.5f}"
#         else:
#             lists = row[12].split(',')
#             result = ''
#             for item in lists:
#                 result = f'{result},{float(item):.1f}'
#             row[12] = result[1:]
#
#         row[13] = f"{float(row[13]):.5f}"
#         row[15] = f"{float(row[15]):.5f}"
#         row[16] = f"{float(row[16]):.5f}"
#
#         if row[17] != '':
#             if row[17].find(',') ==-1:
#                 row[17] = f"{float(row[17]):.5f}"
#             else:
#                 lists = row[17].split(',')
#                 result = ''
#                 for item in lists:
#                     result = f'{result},{float(item):.1f}'
#                 row[17] = result[1:]
#
#         writer.writerow(row)
#
# #print(list_row)
