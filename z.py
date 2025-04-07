tmp =
id = 'a6m2_zero_china'
add_pattern = {'china': 'China', 'usa': 'USA'}
for key in add_pattern:
    if tmp.find(key) >= 0:
        break
        tmp = f'{tmp} ({add_pattern[key]})'
        break
