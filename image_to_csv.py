import os, pandas as pd

url = 'http://35.216.58.5:5000/static/img'

folder_list = os.listdir('./data/image')
if '.DS_Store' in folder_list:
    folder_list.remove('.DS_Store')

for folder in folder_list: # idx, furniture_idx, files, file_cnt, status
    print(f"folder name : {folder}")

    tmp = []

    file_list = os.listdir(f'./data/image/{folder}')
    if '.DS_Store' in file_list:
        file_list.remove('.DS_Store')

    # furniture_idx, files, file_cnt
    for file in file_list:
        file_name = file.split('.')
        if file_name[1] == 'csv':
            continue
        file_name_split = file_name[0].split('-')

        furniture_idx = file_name_split[0]
        files = f'{url}/{file}' # http://35.216.58.5:5000/static/img/10-1.jpg
        file_cnt = file_name_split[1]

        tmp.append([furniture_idx, files, file_cnt])

    tmp.sort()
    pd.DataFrame(tmp).to_csv(f'./data/image/{folder}/{folder}.csv', index=False, header=False)

