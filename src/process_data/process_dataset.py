# USER TODO:
# Install the correct requirements.
# Substitute      /home/nikoscf/PycharmProjects/  => your directory
# pip install -r '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/requirements.txt'

import pandas as pd
import os.path

files_path = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/raw'
store_path = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal'
txt_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal/txt/'

datasets_name = ['Projects_datasets.xlsx', 'Projects2.xlsx']


class ProcessDatasetProject:
    ''' Convert all the xslx to csv and store them to 'internal' directory '''

    def xslx_to_csv_and_store(self, datasets_name, files_path, store_path):
        for file_name in datasets_name:
            xl_file = os.path.join(files_path, file_name)
            read_file = pd.read_excel(xl_file)
            prefix_name = os.path.splitext(file_name)[0]
            store_csv = os.path.join(store_path, prefix_name + '.csv')
            read_file.to_csv(store_csv, index=None, header=True)

    '''Create a dictionary of dataframes reading all the csv files.
        Return the dictionary.'''

    def _read_CSVs(self, datasets_name, store_path):
        d = {}
        for file_name in datasets_name:
            prefix_name = os.path.splitext(file_name)[0]
            stored_csv = os.path.join(store_path, prefix_name + '.csv')
            df_name = 'df_' + file_name
            d[df_name] = pd.read_csv(stored_csv)
            assert isinstance(d[df_name], pd.DataFrame)
            assert d[df_name].empty == False
        return d

    def csv_to_txt(self, txt_direc, data):
        for file_name in os.listdir(txt_direc):
            if file_name is None:
                file_dir = os.path.join(txt_direc, file_name)
                with open(file_dir + '.txt', "w") as file:
                    file.write(data)
            else:
                pass
        if os.listdir(store_path) is None:
            print("Not acceptable file format for data processing.")
        else:
            print("CSV columns stored to txt files.")

    '''
    Now we want to take as much as useful data in a form of text as possible. 
    This method from a selection of columns concatenates their text into one column, 
    then stores the merged text along with the project id in a new dataframe
    and extracts to txt file.
    
    Input:
        dic_data: is the dictionary with the dataframes, one dataframe per file
        proj_id: the unique id per project
        t_columns: a tuple with the columns from the files that we want to concatenate their texts. 
                    Texts separeted with '. '.  
    Output: 
        a data frame: id, column names concatenated on first five letters.
        example: 'title', 'objective' -> 'title_objec'
    '''

    def process_projects_data(self, proj_id='id', t_columns=['title', 'objective']):
        short_header = [first_n[0:5] for first_n in t_columns]
        column_name = '_'.join(short_header)
        all_columns = [proj_id] + [column_name]
        df_text = pd.DataFrame(columns=all_columns)
        create_data = [proj_id] + t_columns

        dic_project = ProcessDatasetProject._read_CSVs(self, datasets_name, store_path)

        for key, value in dic_project.items():
            df = dic_project[key][create_data]
            df_text[column_name] = df[t_columns].agg('. '.join, axis=1)
            df_text.to_csv(txt_dir + 'merged_project_text')
            df_text[proj_id] = df[proj_id]

        return df_text
