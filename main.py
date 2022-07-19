import pandas as pd
import os
import glob

pd.set_option('display.max_columns', None)
account_folder = os.environ.get('FITBIT_ACC_FOLDER', '')
output_folder = os.environ.get('HOME', '')

if __name__ == '__main__':
    if not os.path.exists(account_folder):
        exit()
    json_pattern = os.path.join(account_folder, '*.json')
    file_list = glob.glob(json_pattern)
    dfs = []  # an empty list to store the data frames
    for file in file_list:
        data = pd.read_json(file)  # read data frame from json file
        dfs.append(data)  # append the data frame to the list
    temp = pd.concat(dfs, ignore_index=True)  # concatenate all the data frames in the list.
    temp = temp[['date', 'weight', 'fat']]
    temp['weight'] = temp['weight']*0.45359237
    temp['fat'] = temp['fat']/100*temp['weight']
    temp = temp.rename(columns={'date': "Date", 'weight': 'Weight', 'fat': 'Fat mass'})
    temp = temp.sort_values('Date')
    temp.to_csv(f'{output_folder}/out.csv', index=False)
