# USER TODO:
# Install the correct requirements.
# Substitute      /home/nikoscf/PycharmProjects/  => your directory
# pip install -r '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/requirements.txt'

import pandas as pd
import os.path
from ProcessDatasetInterface import FormalProcessDatasetInterface as DataIface

files_path = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/raw'
path_storing = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal'
txt_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal/txt/'

datasets_name_list = ['Projects_datasets.xlsx', 'Projects2.xlsx']


def _xslx_to_csv_and_store(datasets_name_list):
    for file_name in datasets_name_list:
        xl_file = os.path.join(files_path, file_name)
        read_file = pd.read_excel(xl_file)
        prefix_name = os.path.splitext(file_name)[0]
        csv_path = os.path.join(path_storing, prefix_name + '.csv')
        read_file.to_csv(csv_path, index=None, header=True)
    return


class ProcessDatasetProject(DataIface):

    def __init__(self, datasets_name_list, files_path, path_storing):
        self.datasets_name_list = datasets_name_list
        self.files_path = files_path
        self.path_storing = path_storing
        self._df_merged_columns = None

    # a client to implement the product interface
    def client_process(self, datasets_name_list, data_format):
        dataset_type = self._get_dataset_type(format)
        return dataset_type(datasets_name_list)

    # creator
    def _get_dataset_type(self, data_format):
        if data_format == 'xlsx':
            return self.dump_data
        else:
            raise ValueError(format)

    '''Create a dictionary of dataframes reading all the csv files.
        Return the dictionary.'''

    # @load_data_source.setter
    # def load_data_source(self, path, file_name):

    def _read_CSVs(self, store_path, datasets_name_list):
        d = {}
        for file_name in datasets_name_list:
            prefix_name = os.path.splitext(file_name)[0]
            stored_csv = os.path.join(store_path, prefix_name + '.csv')
            df_name = 'df_' + file_name
            d[df_name] = pd.read_csv(stored_csv)
            assert isinstance(d[df_name], pd.DataFrame)
            assert d[df_name].empty == False
        return d

    '''
    Now we want to take as much as useful data in a form of text as possible. 
    This method from a selection of columns concatenates their text into one column, 
    then stores the merged text along with the project id in a new dataframe
    and extracts to a txt file.
    
    Input:
        dic_data: is the dictionary with the dataframes, one dataframe per file
        proj_id: the unique id per project
        keep_columns: a tuple with the columns from the files that we want to concatenate their texts. 
                    Texts separeted with '. '.  
    Output: 
        a data frame: id, column names concatenated on first five letters.
        example: 'title', 'objective' -> 'title_objec'
    '''

    @property
    def filter_data(self):
        return self._df_merged_columns

    @filter_data.setter
    def filter_data(self, proj_id='id', keep_columns=['title', 'objective']):
        short_header = [first_n[0:5] for first_n in keep_columns]  # create header:concat first 5 letters of each column
        column_name = '_'.join(short_header)
        all_columns = [proj_id] + [column_name]
        self._df_merged_columns = pd.DataFrame(columns=all_columns)
        create_data = [proj_id] + keep_columns

        dic_project = ProcessDatasetProject._read_CSVs(self, self.datasets_name_list, self.path_storing)

        for key, value in dic_project.items():
            df = dic_project[key][create_data]
            self._df_merged_columns[column_name] = df[keep_columns].agg('. '.join, axis=1)
            self._df_merged_columns.to_csv(txt_dir + 'merged_project_text')
            self._df_merged_columns[proj_id] = df[proj_id]

    ''' Convert all the xslx to csv and store them to 'internal' directory '''

    def _df_to_txt(self):
        for file_name in os.listdir(txt_dir):
            if file_name is not None:
                file_dir = os.path.join(txt_dir, file_name)
                with open(file_dir + '.txt', "w") as file:
                    file.write(self._df_merged_columns)
            else:
                pass
        if os.listdir(self.path_storing) is None:
            print("Not acceptable file format for data processing.")
        else:
            print("CSV columns stored to txt files.")

    """ store csv to txt """

    def dump_data(self, full_file_path):
        return _xslx_to_csv_and_store, self._df_to_txt
