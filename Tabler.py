import json
import os
import pandas

# Funcao para separacao dos jsons de acordo com data
def date_split(file_name):
    file_type = '.json'

    data_file = open(file_name + file_type)
    data = json.load(data_file)
    data_file.close()

    data_sorted = []
    num_days = 0

    for item in data:
        date_complete = item["datetime"]
        date = date_complete[0:10]

        has_place = False
        for day in range(num_days):
            if (date == data_sorted[day][0]):
                data_sorted[day][1].append(item)
                has_place = True
                break

        if (has_place == False):
            num_days += 1
            data_sorted.append([date, []])
            data_sorted[num_days - 1][1].append(item)

    for day in range(num_days):
        new_file_name = data_sorted[day][0] + '_' + file_name + file_type
        new_file = open(new_file_name, 'w')
        json.dump(data_sorted[day][1], new_file, indent=4)
        new_file.close()

def tabler(json_files, path):
    for file_name in json_files:
        data_file = open(file_name + '.json')
        data = json.load(data_file)
        data_file.close()
        pandas.DataFrame(data).to_excel(file_name + '.xlsx')


# Aqui comeca a execucao
# Separa jsons de acordo com a data
path = os.getcwd()
files_list = os.listdir(path)
json_files = []

for item in files_list:
    if (item.endswith('.json')):
        json_files.append(item.split('.')[0])

for item in json_files:
    date_split(item)
    os.remove(path + '/' + item + '.json')

# Transforma em tabelas
files_list = os.listdir(path)
json_files = []

for item in files_list:
    if (item.endswith('.json')):
        json_files.append(item.split('.')[0])

tabler(json_files, path)